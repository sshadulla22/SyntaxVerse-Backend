import sys
import os
from sqlalchemy.orm import Session
from datetime import datetime

# Add the parent directory to sys.path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app import models, auth

def seed():
    db = SessionLocal()
    try:
        # 1. Ensure we have at least one user
        user = db.query(models.User).first()
        if not user:
            print("Creating default voyager user...")
            hashed_pw = auth.get_password_hash("voyager123")
            user = models.User(
                email="voyager@anctext.com",
                hashed_password=hashed_pw,
                full_name="Cosmic Voyager",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        print(f"Seeding data for user: {user.email}")

        # 2. Define Professional Topics
        seed_data = [
            {
                "title": "AI & Neural Architectures",
                "cover": "https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=2000&auto=format&fit=crop",
                "notes": [
                    {
                        "title": "Large Language Models (LLMs)",
                        "content": "# LLM Research\n\nLLMs are trained on massive datasets and use transformer architectures to predict the next token in a sequence.\n\n### Key Components:\n- **Attention Mechanism**: Allows the model to focus on relevant parts of the input.\n- **Positional Encoding**: Helps the model understand the order of words.\n- **Tokenization**: Breaking down text into smaller units.",
                        "cover": "https://images.unsplash.com/photo-1620712943543-bcc4638ef808?q=80&w=2000&auto=format&fit=crop"
                    },
                    {
                        "title": "Diffusion Models for Image Gen",
                        "content": "# Diffusion Models\n\nThese models work by slowly adding noise to an image and then learning to reverse the process.\n\n```javascript\n// Pseudo-code for diffusion step\nfunction reverseStep(x_t, t) {\n  const predictedNoise = model.predict(x_t, t);\n  return x_t - predictedNoise;\n}\n```",
                        "cover": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2000&auto=format&fit=crop"
                    }
                ]
            },
            {
                "title": "Cloud Native Systems",
                "cover": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2000&auto=format&fit=crop",
                "notes": [
                    {
                        "title": "Kubernetes Orchestration",
                        "content": "# Kubernetes (K8s) Overview\n\nK8s is an open-source system for automating deployment, scaling, and management of containerized applications.\n\n- **Pods**: Smallest deployable units.\n- **Services**: Abstract way to expose applications.\n- **Deployments**: Declarative updates for Pods.",
                        "cover": "https://images.unsplash.com/photo-1667372333374-0d3c06639806?q=80&w=2000&auto=format&fit=crop"
                    }
                ]
            },
            {
                "title": "Advanced React Patterns",
                "cover": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?q=80&w=2000&auto=format&fit=crop",
                "notes": [
                    {
                        "title": "Compound Components",
                        "content": "# Compound Components\n\nThis pattern allows you to create components that work together but have a flexible structure.\n\n```javascript\n<Tabs>\n  <Tabs.List>\n    <Tabs.Trigger value='tab1'>Tab 1</Tabs.Trigger>\n  </Tabs.List>\n  <Tabs.Content value='tab1'>Content 1</Tabs.Content>\n</Tabs>\n```",
                        "cover": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=2000&auto=format&fit=crop"
                    }
                ]
            }
        ]

        # 3. Create Folders and Nested Notes
        for folder_data in seed_data:
            # Check if folder already exists
            db_folder = db.query(models.Note).filter(
                models.Note.title == folder_data["title"],
                models.Note.is_folder == True,
                models.Note.owner_id == user.id
            ).first()

            if not db_folder:
                print(f"Adding folder: {folder_data['title']}")
                db_folder = models.Note(
                    title=folder_data["title"],
                    is_folder=True,
                    cover_image=folder_data["cover"],
                    owner_id=user.id
                )
                db.add(db_folder)
                db.commit()
                db.refresh(db_folder)

            for note_data in folder_data["notes"]:
                # Check if note already exists in this folder
                db_note = db.query(models.Note).filter(
                    models.Note.title == note_data["title"],
                    models.Note.parent_id == db_folder.id,
                    models.Note.owner_id == user.id
                ).first()

                if not db_note:
                    print(f"  Adding note: {note_data['title']}")
                    db_note = models.Note(
                        title=note_data["title"],
                        content=note_data["content"],
                        cover_image=note_data.get("cover"),
                        is_folder=False,
                        parent_id=db_folder.id,
                        owner_id=user.id
                    )
                    db.add(db_note)
        
        db.commit()
        print("Done seeding professional data!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
