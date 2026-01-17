from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/notes", tags=["notes"])

# Get all root notes/folders (no parent)
@router.get("/", response_model=List[schemas.NoteResponse])
def get_root_notes(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    notes = db.query(models.Note).filter(
        models.Note.parent_id == None,
        models.Note.owner_id == current_user.id
    ).all()
    return notes

# Get specific note by ID with its children
@router.get("/{note_id}", response_model=schemas.NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# Get children of a specific folder
@router.get("/{note_id}/children", response_model=List[schemas.NoteResponse])
def get_note_children(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Verify parent exists and is a folder
    parent = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == current_user.id
    ).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent note not found")
    if not parent.is_folder:
        raise HTTPException(status_code=400, detail="Note is not a folder")
    
    children = db.query(models.Note).filter(models.Note.parent_id == note_id).all()
    return children

# Global Search
@router.get("/search", response_model=List[schemas.NoteResponse])
def search_notes(q: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    notes = db.query(models.Note).filter(
        models.Note.owner_id == current_user.id,
        (models.Note.title.ilike(f"%{q}%")) | (models.Note.content.ilike(f"%{q}%"))
    ).limit(10).all()
    return notes

# Create new note or folder
@router.post("/", response_model=schemas.NoteResponse)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # If parent_id is provided, verify it exists and is a folder
    if note.parent_id:
        parent = db.query(models.Note).filter(
            models.Note.id == note.parent_id,
            models.Note.owner_id == current_user.id
        ).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent note not found")
        if not parent.is_folder:
            raise HTTPException(status_code=400, detail="Parent must be a folder")
    
    db_note = models.Note(**note.model_dump(), owner_id=current_user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# Update note or folder
@router.put("/{note_id}", response_model=schemas.NoteResponse)
def update_note(note_id: int, note_update: schemas.NoteUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == current_user.id
    ).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Update only provided fields
    update_data = note_update.model_dump(exclude_unset=True)
    
    # If moving to a new parent, verify it exists and is a folder
    if "parent_id" in update_data and update_data["parent_id"]:
        parent = db.query(models.Note).filter(
            models.Note.id == update_data["parent_id"],
            models.Note.owner_id == current_user.id
        ).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent note not found")
        if not parent.is_folder:
            raise HTTPException(status_code=400, detail="Parent must be a folder")
    
    for key, value in update_data.items():
        setattr(db_note, key, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

# Delete note or folder
@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == current_user.id
    ).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # If it's a folder, delete all children recursively (this respects current_user implicitally as children have same owner)
    if db_note.is_folder:
        delete_children_recursive(db, note_id)
    
    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"}

def delete_children_recursive(db: Session, parent_id: int):
    """Recursively delete all children of a folder"""
    children = db.query(models.Note).filter(models.Note.parent_id == parent_id).all()
    for child in children:
        if child.is_folder:
            delete_children_recursive(db, child.id)
        db.delete(child)

# Code Execution Proxy (Piston API)
import requests

@router.post("/execute")
def execute_code(request: schemas.ExecuteRequest, current_user: models.User = Depends(auth.get_current_user)):
    piston_url = "https://emkc.org/api/v2/piston/execute"
    payload = request.dict()
    
    try:
        response = requests.post(piston_url, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Piston API Error: {e}")
        error_detail = "Execution Failed"
        if hasattr(e, 'response') and e.response is not None:
             error_detail = f"Piston Error: {e.response.text}"
        
        raise HTTPException(status_code=502, detail=error_detail)
