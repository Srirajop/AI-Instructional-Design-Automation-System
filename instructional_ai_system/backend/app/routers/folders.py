from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models
from ..dependencies import get_db, get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.FolderResponse])
def get_folders(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Folder).filter(models.Folder.user_id == current_user.id, models.Folder.parent_id == None).all()

@router.get("/{folder_id}", response_model=schemas.FolderDetailResponse)
def get_folder_detail(folder_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    folder = db.query(models.Folder).filter(models.Folder.id == folder_id, models.Folder.user_id == current_user.id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder

@router.post("/", response_model=schemas.FolderResponse)
def create_folder(folder_in: schemas.FolderCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Security: Verify parent_id belongs to current_user
    if folder_in.parent_id:
        parent = db.query(models.Folder).filter(models.Folder.id == folder_in.parent_id, models.Folder.user_id == current_user.id).first()
        if not parent:
            raise HTTPException(status_code=403, detail="Unauthorized access to parent folder")

    folder = models.Folder(
        name=folder_in.name,
        parent_id=folder_in.parent_id,
        user_id=current_user.id
    )
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder

@router.delete("/{folder_id}")
def delete_folder(folder_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    folder = db.query(models.Folder).filter(models.Folder.id == folder_id, models.Folder.user_id == current_user.id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    db.delete(folder)
    db.commit()
    return {"message": "Folder deleted successfully"}
