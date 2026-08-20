from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from .. import schemas, models
from ..dependencies import get_db, get_current_user
from ..services import history_service, extraction_service
import json
import pathlib
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

MAX_STYLE_GUIDE_SIZE = 50 * 1024 * 1024  # 50 MB — same limit as Source Material

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
            api_key = os.getenv("GEMINI_API_KEY")
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


@router.post("/{project_id}/style-guide")
async def upload_style_guide_pdf(
    project_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Upload a PDF style guide for a project.
    Extracts text and stores it inside the project's intake_data JSON
    under the keys 'style_guide_pdf_text' and 'style_guide_pdf_name'.
    Does NOT replace or modify any other intake fields.
    """
    # Validate file type
    ext = pathlib.Path(file.filename).suffix.lower()
    if ext != ".pdf":
        raise HTTPException(status_code=400, detail="Style guide must be a PDF file.")

    project = history_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Read file content and enforce size limit
    content = await file.read()
    if len(content) > MAX_STYLE_GUIDE_SIZE:
        raise HTTPException(status_code=400, detail="Style guide PDF exceeds the 50 MB size limit.")

    # Write to a temp file so PyPDF2 can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            extracted_text = extraction_service.extract_text_from_pdf(f)

        # extraction_service returns "Error ..." strings on failure
        if extracted_text.startswith("Error"):
            raise HTTPException(status_code=400, detail=f"Could not extract text from PDF: {extracted_text}")

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="The uploaded PDF appears to contain no readable text.")

        # Merge into existing intake_data JSON — do not overwrite other fields
        existing_intake = {}
        if project.intake_data:
            try:
                existing_intake = json.loads(project.intake_data)
            except json.JSONDecodeError:
                pass

        existing_intake["style_guide_pdf_text"] = extracted_text
        existing_intake["style_guide_pdf_name"] = file.filename

        history_service.update_project_data(
            db, project_id, current_user.id,
            {"intake_data": json.dumps(existing_intake)}
        )

        return {
            "message": "Style guide uploaded and processed successfully.",
            "filename": file.filename,
            "extracted_length": len(extracted_text)
        }
    finally:
        os.remove(tmp_path)

