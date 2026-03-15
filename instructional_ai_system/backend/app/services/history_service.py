from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from .. import models, schemas
import uuid

def create_project(db: Session, user_id: int, project: schemas.ProjectCreate) -> models.Project:
    db_project = models.Project(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title=project.title,
        business_unit=project.business_unit
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project_data(db: Session, project_id: str, user_id: int, update_data: Dict[str, Any]) -> Optional[models.Project]:
    project = db.query(models.Project).filter(models.Project.id == project_id, models.Project.user_id == user_id).first()
    if not project:
        return None
        
    for key, value in update_data.items():
        if hasattr(project, key):
             setattr(project, key, value)
             
    db.commit()
    db.refresh(project)
    return project

def get_user_projects(db: Session, user_id: int):
    return db.query(models.Project).filter(models.Project.user_id == user_id).order_by(models.Project.updated_at.desc()).all()

def get_project(db: Session, project_id: str, user_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id, models.Project.user_id == user_id).first()
