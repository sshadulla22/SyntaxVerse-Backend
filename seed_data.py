import sys
import os

# Add the current directory to the python path so imports work
sys.path.append(os.getcwd())

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from app.auth import get_password_hash

# Initialize Database Session
db = SessionLocal()

def seed_content():
    print("🌱 Starting Comprehensive Data Seeding...")

    # 1. Ensure a Default User Exists
    user = db.query(models.User).filter(models.User.email == "demo@anctext.com").first()
    if not user:
        print("Creating demo user...")
        user = models.User(
            email="demo@anctext.com",
            full_name="Cosmic Architect",
            hashed_password=get_password_hash("password123")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    print(f"👤 Seeding data for user: {user.full_name}")

    # --- REACT SECTION ---
    print("... Seeding React Content")
    react_folder = models.Note(
        title="⚛️ React Mastery",
        content="Comprehensive guide to modern React development.",
        is_folder=True,
        owner_id=user.id,
        cover_image="https://images.unsplash.com/photo-1633356122544-f134324a6cee?q=80&w=2070&auto=format&fit=crop"
    )
    db.add(react_folder)
    db.commit()
    db.refresh(react_folder)

    # React Notes
    react_notes = [
        {
            "title": "Understanding Hooks",
            "content": """# Deep Dive into React Hooks

Hooks allow you to use state and other React features without writing a class.

## The Rules of Hooks
1. **Only Call Hooks at the Top Level**: Don't call Hooks inside loops, conditions, or nested functions.
2. **Only Call Hooks from React Functions**: Call Hooks from React function components or custom Hooks.

## `useEffect` Dependency Array
The dependency array is the second argument to `useEffect`.

```javascript
// Run once on mount
useEffect(() => {
  console.log("Mounted!");
}, []);

// Run on every render
useEffect(() => {
  console.log("Rendered!");
});

// Run when 'count' changes
useEffect(() => {
  console.log("Count changed:", count);
}, [count]);
```
""",
            "cover_image": "https://images.unsplash.com/photo-1555099962-4199c345e5dd?q=80&w=2070&auto=format&fit=crop"
        },
        {
            "title": "React Server Components",
            "content": """# React Server Components (RSC)

RSCs allow you to render components on the server, reducing the amount of JavaScript sent to the client.

## Key Benefits
- **Zero Bundle Size**: Server components' code isn't included in the client bundle.
- **Direct Backend Access**: access your database directly from your components.
- **Automatic Code Splitting**: Client components imported by server components are automatically split.

```javascript
// Note.server.js
import db from 'db';

async function Note({ id }) {
  const note = await db.notes.get(id);
  return (
    <div>
      <h1>{note.title}</h1>
      <section>{note.body}</section>
    </div>
  );
}
```
""",
             "cover_image": "https://images.unsplash.com/photo-1618477247222-ac59e698eb54?q=80&w=2070&auto=format&fit=crop"
        },
        {
            "title": "Advanced State Management",
            "content": """# State Management Beyond `useState`

When your application grows, `useState` might not be enough.

## `useReducer`
Prefer `useReducer` when you have complex state logic or when the next state depends on the previous one.

```javascript
const initialState = {count: 0};

function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return {count: state.count + 1};
    case 'decrement':
      return {count: state.count - 1};
    default:
      throw new Error();
  }
}
```

## Context API
Context provides a way to pass data through the component tree without having to pass props down manually at every level.
""",
            "cover_image": "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?q=80&w=2070&auto=format&fit=crop"
        }
    ]

    for note_data in react_notes:
        note = models.Note(
            title=note_data["title"],
            content=note_data["content"],
            is_folder=False,
            parent_id=react_folder.id,
            owner_id=user.id,
            cover_image=note_data["cover_image"]
        )
        db.add(note)
    
    db.commit()


    # --- JAVASCRIPT SECTION ---
    print("... Seeding JavaScript Content")
    js_folder = models.Note(
        title="⚡ JavaScript Internals",
        content="Mastering the core of the web.",
        is_folder=True,
        owner_id=user.id,
        cover_image="https://images.unsplash.com/photo-1627398242450-2c3d1f9d4538?q=80&w=2070&auto=format&fit=crop"
    )
    db.add(js_folder)
    db.commit()
    db.refresh(js_folder)

    js_notes = [
        {
            "title": "The Event Loop",
            "content": """# The JavaScript Event Loop

JavaScript is single-threaded, but it handles concurrency using the **Event Loop**.

## Key Components
1. **Call Stack**: Where your code executes. LIFO (Last In, First Out).
2. **Web APIs**: Browser provided APIs (DOM, setTimeout, fetch).
3. **Callback Queue**: Where callbacks wait to be executed.
4. **Event Loop**: Checks if the Call Stack is empty. If so, it moves items from the Queue to the Stack.

```javascript
console.log('Start');

setTimeout(() => {
  console.log('Timeout');
}, 0);

console.log('End');

// Output:
// Start
// End
// Timeout
```
""",
            "cover_image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070&auto=format&fit=crop"
        },
        {
            "title": "Closures & Scope",
            "content": """# Power of Closures

A closure is the combination of a function bundled together (enclosed) with references to its surrounding state (the lexical environment).

```javascript
function makeAdder(x) {
  return function(y) {
    return x + y;
  };
}

const add5 = makeAdder(5);
const add10 = makeAdder(10);

console.log(add5(2));  // 7
console.log(add10(2)); // 12
```

In other words, a closure gives you access to an outer function’s scope from an inner function.
""",
            "cover_image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=2070&auto=format&fit=crop"
        }
    ]

    for note_data in js_notes:
        note = models.Note(
            title=note_data["title"],
            content=note_data["content"],
            is_folder=False,
            parent_id=js_folder.id,
            owner_id=user.id,
            cover_image=note_data["cover_image"]
        )
        db.add(note)
    
    db.commit()


    # --- PYTHON SECTION ---
    print("... Seeding Python Content")
    python_folder = models.Note(
        title="🐍 Python Architecture",
        content="Backend engineering with Python and FastAPI.",
        is_folder=True,
        owner_id=user.id,
        cover_image="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=2070&auto=format&fit=crop"
    )
    db.add(python_folder)
    db.commit()
    db.refresh(python_folder)

    python_notes = [
        {
            "title": "FastAPI: The Modern Standard",
            "content": """# Why FastAPI?

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Key Features
- **Fast**: Very high performance, on par with NodeJS and Go.
- **Fast to code**: Increase the speed to develop features by about 200% to 300%.
- **Fewer bugs**: Reduce about 40% of human (developer) induced errors.

```python
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```
""",
            "cover_image": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=2070&auto=format&fit=crop"
        },
        {
            "title": "SQLAlchemy ORM 2.0",
            "content": """# SQLAlchemy 2.0 Style

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

## Declaring Models

```python
class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
```
""",
            "cover_image": "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?q=80&w=2070&auto=format&fit=crop"
        }
    ]

    for note_data in python_notes:
        note = models.Note(
            title=note_data["title"],
            content=note_data["content"],
            is_folder=False,
            parent_id=python_folder.id,
            owner_id=user.id,
            cover_image=note_data["cover_image"]
        )
        db.add(note)
    
    db.commit()

    print("✨ Seeding Completed Successfully! The cosmos is populated.")
    db.close()

if __name__ == "__main__":
    seed_content()
