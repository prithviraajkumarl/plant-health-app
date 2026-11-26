"""Analysis and AutoSim router."""

import io
import random
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from PIL import Image

from app.backend.config import (
    MAX_UPLOAD_BYTES,
    ALLOWED_MIME_TYPES,
    SAMPLES_DIR,
    get_connection_info
)
from app.backend.schemas import AnalysisResponse, DiseaseInfo, TopPrediction
from app.backend.inference import run_inference, save_image_and_thumbnail
from app.backend.database import save_analysis, get_disease_record

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(
    file: UploadFile = File(...),
    source: str = Form("upload")
):
    """Analyze leaf image from upload or live camera capture."""
    # Validate content type
    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image type: {file.content_type}. Please upload a JPEG, PNG, or WebP image."
        )

    # Read bytes and validate size
    contents = await file.read()
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Image file too large. Maximum allowed size is 15 MB."
        )

    if len(contents) < 100:
        raise HTTPException(
            status_code=400,
            detail="File is empty or corrupted."
        )

    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()  # Verify valid image data
        image = Image.open(io.BytesIO(contents))  # Re-open after verify
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image format: {str(e)}"
        )

    # Run actual TFLite inference
    result = run_inference(image)

    # Save original & thumbnail
    rel_img_url, rel_thumb_url, _, _ = save_image_and_thumbnail(result["processed_image"])

    # Persist in database
    analysis_id = save_analysis(
        image_path=rel_img_url,
        thumbnail_path=rel_thumb_url,
        plant=result["plant"],
        predicted_class=result["predicted_class"],
        confidence=result["confidence"],
        is_simulated=False,
        source=source,
        notes=None
    )

    advice_data = get_disease_record(result["predicted_class"])
    conn_info = get_connection_info()

    return AnalysisResponse(
        id=analysis_id,
        timestamp=result.get("timestamp", ""),
        image_url=rel_img_url,
        thumbnail_url=rel_thumb_url,
        plant=result["plant"],
        predicted_class=result["predicted_class"],
        display_name=result["display_name"],
        is_healthy=result["is_healthy"],
        confidence=result["confidence"],
        confidence_percent=result["confidence_percent"],
        is_low_confidence=result["is_low_confidence"],
        is_simulated=False,
        source=source,
        advice=DiseaseInfo(**advice_data),
        top_predictions=[TopPrediction(**p) for p in result["top_predictions"]],
        qr_url=conn_info.get("url")
    )


@router.post("/autosim", response_model=AnalysisResponse)
async def autosim_analysis(sample_name: str = Query(None)):
    """Run AutoSim: selects a sample leaf image, performs real inference, and records simulation."""
    if not SAMPLES_DIR.exists():
        raise HTTPException(status_code=500, detail="Samples directory not found.")

    available_samples = list(SAMPLES_DIR.glob("*.jpg")) + list(SAMPLES_DIR.glob("*.png"))
    if not available_samples:
        raise HTTPException(status_code=500, detail="No sample images found in app/samples.")

    if sample_name:
        chosen_sample = SAMPLES_DIR / sample_name
        if not chosen_sample.exists():
            chosen_sample = random.choice(available_samples)
    else:
        chosen_sample = random.choice(available_samples)

    try:
        image = Image.open(chosen_sample)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed loading sample leaf: {str(e)}")

    # Run actual TFLite inference pipeline
    result = run_inference(image)

    # Save image & thumbnail to uploads
    rel_img_url, rel_thumb_url, _, _ = save_image_and_thumbnail(result["processed_image"])

    # Persist in SQLite marked as simulated
    analysis_id = save_analysis(
        image_path=rel_img_url,
        thumbnail_path=rel_thumb_url,
        plant=result["plant"],
        predicted_class=result["predicted_class"],
        confidence=result["confidence"],
        is_simulated=True,
        source="autosim",
        notes=f"AutoSim using sample: {chosen_sample.name}"
    )

    advice_data = get_disease_record(result["predicted_class"])
    conn_info = get_connection_info()

    return AnalysisResponse(
        id=analysis_id,
        timestamp="",
        image_url=rel_img_url,
        thumbnail_url=rel_thumb_url,
        plant=result["plant"],
        predicted_class=result["predicted_class"],
        display_name=result["display_name"],
        is_healthy=result["is_healthy"],
        confidence=result["confidence"],
        confidence_percent=result["confidence_percent"],
        is_low_confidence=result["is_low_confidence"],
        is_simulated=True,
        source="autosim",
        advice=DiseaseInfo(**advice_data),
        top_predictions=[TopPrediction(**p) for p in result["top_predictions"]],
        qr_url=conn_info.get("url")
    )
