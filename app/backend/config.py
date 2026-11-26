"""Configuration and directory paths for PlantHealthApp."""

from pathlib import Path
import os
import json
import socket

# Paths
BACKEND_DIR = Path(__file__).resolve().parent
APP_DIR = BACKEND_DIR.parent
ROOT_DIR = APP_DIR.parent

MODELS_DIR = APP_DIR / "models"
DB_DIR = APP_DIR / "db"
DB_PATH = DB_DIR / "plant_health.db"
UPLOADS_DIR = APP_DIR / "uploads"
SAMPLES_DIR = APP_DIR / "samples"
RUNTIME_DIR = APP_DIR / "runtime"
TOOLS_DIR = APP_DIR / "tools"
FRONTEND_DIR = APP_DIR / "frontend"
CONNECTION_FILE = RUNTIME_DIR / "connection.json"

MODEL_FILE = MODELS_DIR / "plant_disease_model.tflite"
CATEGORIES_FILE = MODELS_DIR / "categories.json"
METADATA_FILE = MODELS_DIR / "metadata.json"

# Settings
DEFAULT_PORT = int(os.environ.get("PORT", 8000))
CONFIDENCE_THRESHOLD = 0.60
MAX_UPLOAD_BYTES = 15 * 1024 * 1024  # 15 MB
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/bmp"}


def get_lan_ip() -> str:
    """Detect LAN IPv4 address reachable on local network."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Does not actually send packets
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def get_connection_info() -> dict:
    """Read connection info written by START scripts or generate fallback."""
    if CONNECTION_FILE.exists():
        try:
            with open(CONNECTION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception:
            pass

    # Check if running in cloud hosting environment (Hugging Face Spaces, Render, Railway)
    public_url = os.environ.get("PUBLIC_URL")
    if not public_url and os.environ.get("SPACE_HOST"):
        public_url = f"https://{os.environ['SPACE_HOST']}"
    if not public_url and os.environ.get("RENDER_EXTERNAL_URL"):
        public_url = os.environ["RENDER_EXTERNAL_URL"]

    if public_url:
        return {
            "mode": "online",
            "url": public_url,
            "local_url": f"http://localhost:{DEFAULT_PORT}",
            "ip": None,
            "port": DEFAULT_PORT,
        }

    lan_ip = get_lan_ip()
    return {
        "mode": "local",
        "url": f"http://{lan_ip}:{DEFAULT_PORT}",
        "local_url": f"http://localhost:{DEFAULT_PORT}",
        "ip": lan_ip,
        "port": DEFAULT_PORT,
    }
