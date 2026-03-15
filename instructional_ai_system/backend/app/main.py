from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from . import models
from .database import engine

from .routers import auth, intake, extraction, design, storyboard, edit, history, export, folders, files

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Instructional Design API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(intake.router, prefix="/api/intake", tags=["intake"])
app.include_router(extraction.router, prefix="/api/extraction", tags=["extraction"])
app.include_router(design.router, prefix="/api/design", tags=["design"])
app.include_router(storyboard.router, prefix="/api/storyboard", tags=["storyboard"])
app.include_router(edit.router, prefix="/api/edit", tags=["edit"])
app.include_router(history.router, prefix="/api/history", tags=["history"])
app.include_router(export.router, prefix="/api/export", tags=["export"])
app.include_router(folders.router, prefix="/api/folders", tags=["folders"])
app.include_router(files.router, prefix="/api/files", tags=["files"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Instructional Design API"}

# Trigger reload
