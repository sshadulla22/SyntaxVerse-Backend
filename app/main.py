import logging
import time
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.database import engine, Base
from app import routes, auth_routes
from .config import settings

# Structured Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("anctext")

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# CORS Middleware - Normalized origins
origins = settings.parsed_origins
# Add common variations
if "https://syntaxverse-frontend.onrender.com" in origins:
    origins.append("https://syntaxverse-frontend.onrender.com/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please contact support."},
    )

# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}ms".format(process_time)
    logger.info(
        f"RID: {request.scope.get('root_path')} | Path: {request.url.path} | Method: {request.method} | Status: {response.status_code} | Time: {formatted_process_time}"
    )
    return response

# Include routers
app.include_router(auth_routes.router)
app.include_router(routes.router)

@app.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} is running 🚀",
        "status": "productive",
        "version": "1.0.0"
    }
