from fastapi.responses import FileResponse
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models
from ..dependencies import get_db, get_current_user

router = APIRouter()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload", response_model=schemas.UserFileResponse)
async def upload_file(
    folder_id: Optional[int] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Security: Verify folder_id belongs to current_user
    if folder_id:
        folder = db.query(models.Folder).filter(models.Folder.id == folder_id, models.Folder.user_id == current_user.id).first()
        if not folder:
            raise HTTPException(status_code=403, detail="Unauthorized access to folder")

    user_dir = os.path.join(UPLOAD_DIR, str(current_user.id))
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    
    file_path = os.path.join(user_dir, file.filename)
    
    # Save file and calculate size
    content = await file.read()
    file_size = len(content)
    with open(file_path, "wb") as buffer:
        buffer.write(content)
        
    user_file = models.UserFile(
        name=file.filename,
        folder_id=folder_id,
        user_id=current_user.id,
        file_type=file.content_type,
        file_path=file_path,
        file_size=file_size
    )
    db.add(user_file)
    db.commit()
    db.refresh(user_file)
    return user_file

@router.get("/", response_model=List[schemas.UserFileResponse])
def get_files(folder_id: Optional[int] = None, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = db.query(models.UserFile).filter(models.UserFile.user_id == current_user.id)
    if folder_id:
        query = query.filter(models.UserFile.folder_id == folder_id)
    else:
        # Crucial fix: return ONLY root files when folder_id is not specified
        query = query.filter(models.UserFile.folder_id == None)
    return query.all()

@router.get("/{file_id}/download")
def download_file(
    file_id: int, 
    db: Session = Depends(get_db), 
    token: Optional[str] = None,
    current_user: models.User = Depends(get_current_user)
):
    # Note: get_current_user already handles token validation if present in header.
    # If using window.open, we might pass it as a query param.
    
    user_file = db.query(models.UserFile).filter(models.UserFile.id == file_id, models.UserFile.user_id == current_user.id).first()
    if not user_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if not os.path.exists(user_file.file_path):
        raise HTTPException(status_code=404, detail="File content missing on server")
        
    return FileResponse(
        path=user_file.file_path,
        filename=user_file.name,
        media_type=user_file.file_type
    )

@router.delete("/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user_file = db.query(models.UserFile).filter(models.UserFile.id == file_id, models.UserFile.user_id == current_user.id).first()
    if not user_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if os.path.exists(user_file.file_path):
        try:
            os.remove(user_file.file_path)
        except:
            pass
        
    db.delete(user_file)
    db.commit()
    return {"message": "File deleted successfully"}
