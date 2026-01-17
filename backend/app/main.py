from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import routes

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ANCText Notes API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router)

@app.get("/")
def root():
    return {"message": "ANCText Notes API is running 🚀"}
