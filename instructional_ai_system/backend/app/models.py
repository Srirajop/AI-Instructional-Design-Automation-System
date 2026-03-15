from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, index=True) # UUID
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255), nullable=False)
    business_unit = Column(String(150), nullable=True)
    
    # Needs to hold extremely long stringified JSON or markdown
    intake_data = Column(LONGTEXT, nullable=True)
    extracted_content = Column(LONGTEXT, nullable=True)
    design_doc = Column(LONGTEXT, nullable=True)
    storyboard = Column(LONGTEXT, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="projects")
    messages = relationship("ChatMessage", back_populates="project", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"))
    type = Column(String(50)) # "design" or "storyboard"
    role = Column(String(50)) # "user" or "assistant"
    content = Column(LONGTEXT)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="messages")

class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    files = relationship("UserFile", back_populates="folder", cascade="all, delete-orphan")
    subfolders = relationship("Folder", backref=backref("parent", remote_side=[id]), cascade="all, delete-orphan")

class UserFile(Base):
    __tablename__ = "user_files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_type = Column(String(100))
    file_path = Column(String(500))
    file_size = Column(Integer, nullable=True) # in bytes
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    folder = relationship("Folder", back_populates="files")
