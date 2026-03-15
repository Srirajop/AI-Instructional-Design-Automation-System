from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models
from ..dependencies import get_db, get_current_user
from ..services import history_service

router = APIRouter()

@router.get("/", response_model=List[schemas.ProjectResponse])
def get_history(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    projects = history_service.get_user_projects(db, current_user.id)
    return projects

@router.get("/{project_id}", response_model=schemas.ProjectDetailResponse)
def get_project_detail(project_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project = history_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}")
def delete_project(project_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    project = history_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}
