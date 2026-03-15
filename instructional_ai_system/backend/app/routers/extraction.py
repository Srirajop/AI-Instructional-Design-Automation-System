import tempfile
import pathlib
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from .. import models
from ..dependencies import get_db, get_current_user
from ..services import extraction_service, history_service

router = APIRouter()

@router.post("/{project_id}/upload")
async def extract_content_upload(
    project_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = history_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    ext = pathlib.Path(file.filename).suffix.lower()
    text = ""
    
    # Save temporarily to parse for some libs that need file paths
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
        elif ext in ['.txt']:
            text = extraction_service.extract_text_from_txt(open(temp_path, 'rb'))
        elif ext in ['.pptx']:
            text = extraction_service.extract_text_from_pptx(temp_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        if "Error" in text and text.startswith("Error"):
             raise HTTPException(status_code=400, detail=text)

        # Append to existing
        existing = project.extracted_content or ""
        new_content = existing + f"\n\n--- SOURCE: {file.filename} ---\n" + text
        
        history_service.update_project_data(db, project_id, current_user.id, {"extracted_content": new_content})
        
        return {"message": "Extracted successfully", "extracted_length": len(text)}
    finally:
        os.remove(temp_path)

@router.post("/{project_id}/url")
def extract_content_url(
    project_id: str,
    url: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = history_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if 'youtube.com' in url or 'youtu.be' in url:
        text = extraction_service.extract_youtube_transcript(url)
    else:
        text = extraction_service.extract_text_from_url(url)
        
    if "Error" in text and text.startswith("Error"):
        raise HTTPException(status_code=400, detail=text)
        
    existing = project.extracted_content or ""
    new_content = existing + f"\n\n--- SOURCE: {url} ---\n" + text
    history_service.update_project_data(db, project_id, current_user.id, {"extracted_content": new_content})
    
    return {"message": "Extracted successfully", "extracted_length": len(text)}

@router.post("/{project_id}/remote")
def extract_content_remote(
    project_id: str,
    file_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = history_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    user_file = db.query(models.UserFile).filter(models.UserFile.id == file_id, models.UserFile.user_id == current_user.id).first()
    if not user_file:
        raise HTTPException(status_code=404, detail="File not found")

    ext = pathlib.Path(user_file.name).suffix.lower()
    text = ""
    
    try:
        if ext == '.pdf':
            with open(user_file.file_path, 'rb') as f:
                text = extraction_service.extract_text_from_pdf(f)
        elif ext in ['.docx']:
            text = extraction_service.extract_text_from_docx(user_file.file_path)
        elif ext in ['.xlsx']:
            text = extraction_service.extract_text_from_xlsx(user_file.file_path)
        elif ext in ['.txt']:
            text = extraction_service.extract_text_from_txt(open(user_file.file_path, 'rb'))
        elif ext in ['.pptx']:
            text = extraction_service.extract_text_from_pptx(user_file.file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        if "Error" in text and text.startswith("Error"):
             raise HTTPException(status_code=400, detail=text)

        # Append to existing
        existing = project.extracted_content or ""
        new_content = existing + f"\n\n--- SOURCE (FOLDER): {user_file.name} ---\n" + text
        
        history_service.update_project_data(db, project_id, current_user.id, {"extracted_content": new_content})
        
        return {"message": "Extracted successfully", "extracted_length": len(text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
