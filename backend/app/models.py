from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True, default="")
    is_folder = Column(Boolean, default=False)
    parent_id = Column(Integer, ForeignKey("notes.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Self-referential relationship
    parent = relationship("Note", remote_side=[id], backref="children")

    def __repr__(self):
        return f"<Note(id={self.id}, title='{self.title}', is_folder={self.is_folder})>"
