from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from .. import schemas, models
from ..dependencies import get_db, get_current_user
from ..services import history_service
import json
import pathlib
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.post("/", response_model=schemas.ProjectResponse)
def create_project_intake(intake_data: dict, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Creates a new project with the provided intake form data."""
    try:
        title = intake_data.get('course_title', 'Untitled Course')
        business_unit = intake_data.get('business_unit', '')
        
        project_create = schemas.ProjectCreate(title=title, business_unit=business_unit)
        project = history_service.create_project(db, current_user.id, project_create)
        
        # Save intake data
        updated_project = history_service.update_project_data(
            db, project.id, current_user.id, {"intake_data": json.dumps(intake_data)}
        )
        return updated_project
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_project(
    file: UploadFile = File(...),
    type: str = Form(...), # "design_doc" or "storyboard"
    title: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        # 1. Create Project
        project_create = schemas.ProjectCreate(title=title)
        project = history_service.create_project(db, current_user.id, project_create)
        
        # 2. Extract Text
        ext = pathlib.Path(file.filename).suffix.lower()
        import tempfile, os
        from ..services import extraction_service
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
            
        try:
            if ext == '.pdf':
                with open(temp_path, 'rb') as f:
                    text = extraction_service.extract_text_from_pdf(f)
            elif ext in ['.docx']:
                text = extraction_service.extract_text_from_docx(temp_path)
            elif ext in ['.xlsx']:
                text = extraction_service.extract_text_from_xlsx(temp_path)
            elif ext in ['.pptx']:
                text = extraction_service.extract_text_from_pptx(temp_path)
            elif ext in ['.txt']:
                text = extraction_service.extract_text_from_txt(open(temp_path, 'rb'))
            else:
                text = "Unsupported format"
                
            # 3. Beautify Content with AI
            api_key = os.getenv("GROQ_API_KEY")
            beautified_text = text
            if api_key:
                try:
                    from ..services import ai_generation
                    beautified_text = ai_generation.beautify_uploaded_content(api_key, text, type)
                except Exception as beau_err:
                    print(f"Beautification failed, falling back to raw: {beau_err}")
                    # Keep raw text if AI fails

            # 4. Save to project
            update_data = {
                "extracted_content": text, # Always save the RAW extracted text here
                type: beautified_text # Set the document field (design_doc or storyboard) to the beautified version
            }
            history_service.update_project_data(db, project.id, current_user.id, update_data)
            
            return {"id": project.id, "message": "Project imported successfully"}
        finally:
            os.remove(temp_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
