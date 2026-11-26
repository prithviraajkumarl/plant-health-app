"""Connection info and QR code router."""

import io
from pathlib import Path
from fastapi import APIRouter, Response
import qrcode
import qrcode.image.svg

from app.backend.config import get_connection_info, SAMPLES_DIR
from app.backend.schemas import ConnectionInfo

router = APIRouter(prefix="/api", tags=["connection"])


@router.get("/connection-info", response_model=ConnectionInfo)
def connection_info():
    """Return active connection mode, IP, port, and URL for phone scanning."""
    info = get_connection_info()
    return ConnectionInfo(
        mode=info.get("mode", "local"),
        url=info.get("url", f"http://localhost:{info.get('port', 8000)}"),
        local_url=info.get("local_url", f"http://localhost:{info.get('port', 8000)}"),
        ip=info.get("ip"),
        port=info.get("port", 8000),
        qr_svg_url="/api/qr.svg"
    )


@router.get("/qr.svg")
def generate_qr_svg():
    """Generate SVG QR code for the current connection URL."""
    info = get_connection_info()
    target_url = info.get("url", "http://localhost:8000")

    factory = qrcode.image.svg.SvgPathImage
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=2,
        image_factory=factory
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    img = qr.make_image(attrib={"class": "qr-svg"})
    stream = io.BytesIO()
    img.save(stream)
    svg_data = stream.getvalue()

    return Response(content=svg_data, media_type="image/svg+xml")


@router.get("/qr.png")
def generate_qr_png():
    """Generate PNG QR code for the current connection URL."""
    info = get_connection_info()
    target_url = info.get("url", "http://localhost:8000")

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=2
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#1b4332", back_color="#ffffff")
    stream = io.BytesIO()
    img.save(stream, format="PNG")
    png_data = stream.getvalue()

    return Response(content=png_data, media_type="image/png")


@router.get("/samples")
def list_samples():
    """List bundled sample images for testing and AutoSim."""
    if not SAMPLES_DIR.exists():
        return {"samples": []}

    samples = []
    for p in SAMPLES_DIR.glob("*.*"):
        if p.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            samples.append({
                "name": p.name,
                "url": f"/samples/{p.name}",
                "size_bytes": p.stat().st_size
            })
    return {"samples": samples}
