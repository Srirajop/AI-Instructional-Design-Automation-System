import os
import json
import time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from .. import models
from ..dependencies import get_db, get_current_user
from ..services import history_service, ai_generation

router = APIRouter()


@router.post("/{project_id}/generate")
def generate_storyboard_stream(project_id: str, storyboard_type: str = "Type 1", db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Generate storyboard module-by-module, streaming progress via SSE."""
    project = history_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Server misconfiguration: missing Groq API Key")

    intake_data = json.loads(project.intake_data) if project.intake_data else {}
    content = project.extracted_content or ""
    design_doc = project.design_doc or ""

    # Check if this is an uploaded project regeneration
    # We detect this if there's extracted_content but NO design_doc (meaning it wasn't AI-generated from scratch)
    is_uploaded_regen = bool(content and not design_doc)

    if not design_doc and not is_uploaded_regen:
        raise HTTPException(status_code=400, detail="Cannot generate storyboard without an approved Design Document.")

    if is_uploaded_regen:
        # For uploaded content, "Generate" means "Re-beautify" with the requested format
        def upload_event_stream():
            yield f"data: {json.dumps({'type': 'progress', 'current': 1, 'total': 1, 'status': 'Re-formatting uploaded storyboard...'})}\n\n"
            try:
                new_sb = ai_generation.beautify_uploaded_content(api_key, content, "storyboard", storyboard_type)
                history_service.update_project_data(db, project_id, current_user.id, {"storyboard": new_sb})
                yield f"data: {json.dumps({'type': 'complete', 'storyboard': new_sb})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        
        return StreamingResponse(upload_event_stream(), media_type="text/event-stream")

    # Standard module-by-module generation for AI-generated projects
    from groq import Groq
    client = Groq(api_key=api_key)
    strategies = ai_generation.get_strategy_for_level(intake_data.get('interactivity_level', ''))
    num_modules = int(intake_data.get('num_modules', 3))
    generate_fn = ai_generation._generate_single_module_type1 if storyboard_type == "Type 1" else ai_generation._generate_single_module_type2

    def event_stream():
        course_title = intake_data.get('course_title', 'Untitled Course')
        all_modules = [f"# STORYBOARD — {course_title}\n"]

        for i in range(1, num_modules + 1):
            # Send progress event
            progress_data = json.dumps({"type": "progress", "current": i, "total": num_modules, "status": f"Generating Module {i} of {num_modules}..."})
            yield f"data: {progress_data}\n\n"

            try:
                module_content = ai_generation._call_module_with_retry(
                    generate_fn, client, i, num_modules, design_doc, intake_data, content, strategies
                )
                all_modules.append(module_content)

                # Send module-complete event
                complete_data = json.dumps({"type": "module_done", "current": i, "total": num_modules, "status": f"Module {i} of {num_modules} complete ✓"})
                yield f"data: {complete_data}\n\n"

            except Exception as e:
                error_data = json.dumps({"type": "error", "message": f"Error generating module {i}: {str(e)}"})
                yield f"data: {error_data}\n\n"
                return

            # Rate limit delay — only between modules (not after last)
            if i < num_modules:
                time.sleep(2)

        # Assemble final storyboard
        full_storyboard = "\n\n---\n\n".join(all_modules)

        # Save to database
        history_service.update_project_data(db, project_id, current_user.id, {"storyboard": full_storyboard})

        # Send final result
        final_data = json.dumps({"type": "complete", "storyboard": full_storyboard})
        yield f"data: {final_data}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
