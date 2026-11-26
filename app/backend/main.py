"""FastAPI main application for PlantHealthApp."""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.backend.config import (
    UPLOADS_DIR,
    SAMPLES_DIR,
    FRONTEND_DIR,
    get_connection_info,
    CATEGORIES_FILE
)
from app.backend.database import init_db, get_db_connection
from app.backend.inference import get_interpreter, _CATEGORIES
from app.backend.schemas import HealthResponse
from app.backend.routers import analyze, history, diseases, connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: database initialization and model loading."""
    # Ensure all directories exist
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    (UPLOADS_DIR / "thumbs").mkdir(parents=True, exist_ok=True)
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize SQLite database schema and seed data
    init_db()

    # Pre-warm TFLite model
    try:
        get_interpreter()
        print("TFLite model loaded successfully.")
    except Exception as e:
        print(f"Warning: Model preloading failed: {e}")

    yield
    print("Application shutting down.")


app = FastAPI(
    title="Plant Health Detection API",
    description="Real-time crop disease diagnosis using MobileNet TFLite and SQLite database",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for all origins (LAN devices, mobile browsers, tunnel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(analyze.router)
app.include_router(history.router)
app.include_router(diseases.router)
app.include_router(connection.router)


@app.get("/api/health", response_model=HealthResponse, tags=["health"])
def health_check():
    """Health check endpoint to verify database and ML model readiness."""
    model_loaded = False
    count = 0
    try:
        interp = get_interpreter()
        model_loaded = interp is not None
        from app.backend.inference import _CATEGORIES
        count = len(_CATEGORIES)
    except Exception:
        model_loaded = False

    db_ok = False
    try:
        with get_db_connection() as conn:
            conn.execute("SELECT 1")
            db_ok = True
    except Exception:
        db_ok = False

    conn_info = get_connection_info()

    return HealthResponse(
        status="ok" if (model_loaded and db_ok) else "degraded",
        model_loaded=model_loaded,
        classes_count=count,
        database_ok=db_ok,
        connection_mode=conn_info.get("mode", "local")
    )


# Mount static assets
if UPLOADS_DIR.exists():
    app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

if SAMPLES_DIR.exists():
    app.mount("/samples", StaticFiles(directory=str(SAMPLES_DIR)), name="samples")


# Serve frontend SPA
@app.get("/")
async def serve_index():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    raise HTTPException(status_code=404, detail="Frontend index.html not found.")


@app.get("/{full_path:path}")
async def serve_frontend_assets(full_path: str):
    # Exclude API endpoints
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Endpoint not found")

    file_path = FRONTEND_DIR / full_path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)

    # SPA fallback: return index.html
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)

    raise HTTPException(status_code=404, detail="File not found")
