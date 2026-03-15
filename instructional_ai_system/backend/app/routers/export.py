from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from .. import models
from ..dependencies import get_db, get_current_user
from ..services import history_service, export_service
import json

router = APIRouter()

@router.get("/{project_id}/design-doc")
def export_design_doc(project_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project = history_service.get_project(db, project_id, current_user.id)
    if not project or not project.design_doc:
        raise HTTPException(status_code=404, detail="Design Doc not found")
        
    intake_data = json.loads(project.intake_data) if project.intake_data else {}
    file_bytes = export_service.export_design_doc_to_xlsx(project.design_doc, intake_data)
    
    if not file_bytes:
        raise HTTPException(status_code=500, detail="Failed to generate Excel file")
        
    return StreamingResponse(
        file_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=Design_Document_{project_id}.xlsx"
        }
    )

@router.get("/{project_id}/storyboard")
def export_storyboard(project_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project = history_service.get_project(db, project_id, current_user.id)
    if not project or not project.storyboard:
        raise HTTPException(status_code=404, detail="Storyboard not found")
        
    intake_data = json.loads(project.intake_data) if project.intake_data else {}
    file_bytes = export_service.export_storyboard_to_docx(project.storyboard, intake_data)
    
    if not file_bytes:
        raise HTTPException(status_code=500, detail="Failed to generate Word file")
        
    return StreamingResponse(
        file_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename=Storyboard_{project_id}.docx"
        }
    )
