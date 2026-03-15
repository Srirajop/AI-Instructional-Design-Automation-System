import os
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..dependencies import get_db, get_current_user
from ..services import history_service, ai_generation

router = APIRouter()

@router.post("/{project_id}/generate")
def generate_design_doc(project_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project = history_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Server misconfiguration: missing Groq API Key")
        
    try:
        intake_data = json.loads(project.intake_data) if project.intake_data else {}
    except json.JSONDecodeError:
        intake_data = {}
    content = project.extracted_content or ""
    design_doc = project.design_doc or ""
    
    if not content:
        raise HTTPException(status_code=400, detail="Cannot generate design doc without extracted source content.")
        
    # Check if this is an uploaded project regeneration
    # If there's content and design_doc already exists, it might be an upload
    # We'll use beautify_uploaded_content for uploaded projects if they don't have a structured intake
    # but for now generate_design_document is fine as it's more comprehensive.
    
    generated_doc = ai_generation.generate_design_document(api_key, intake_data, content)
    
    # If it was an upload and the AI-generated one is better/professional, we save it.
    history_service.update_project_data(db, project_id, current_user.id, {"design_doc": generated_doc})
    
    return {"message": "Success", "design_doc": generated_doc}

@router.post("/{project_id}/approve")
def approve_design_doc(project_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project = history_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    # In a more advanced setup we might want to flag this boolean in DB, but just returning OK 
    return {"message": "Design Doc approved for storyboard generation"}
