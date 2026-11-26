"""History router for retrieving and managing past analyses."""

from pathlib import Path
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Query

from app.backend.config import UPLOADS_DIR
from app.backend.schemas import HistoryItem, AnalysisResponse, DiseaseInfo, TopPrediction
from app.backend.database import (
    get_all_analyses,
    get_analysis_by_id,
    delete_analysis_by_id,
    delete_all_analyses_history,
    get_disease_record
)

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("", response_model=List[HistoryItem])
def list_history(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """List previous analyses with metadata and thumbnails."""
    rows = get_all_analyses(limit=limit, offset=offset)
    items = []
    for r in rows:
        disease = get_disease_record(r["predicted_class"])
        conf = float(r["confidence"])
        items.append(HistoryItem(
            id=r["id"],
            timestamp=r["timestamp"],
            image_url=r["image_path"],
            thumbnail_url=r.get("thumbnail_path") or r["image_path"],
            plant=r["plant"],
            predicted_class=r["predicted_class"],
            display_name=disease.get("display_name", r["predicted_class"]),
            is_healthy=disease.get("is_healthy", False),
            confidence=round(conf, 4),
            confidence_percent=round(conf * 100, 1),
            is_low_confidence=conf < 0.60,
            is_simulated=bool(r["is_simulated"]),
            source=r["source"]
        ))
    return items


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_history_detail(analysis_id: int):
    """Get full details of a specific past analysis."""
    record = get_analysis_by_id(analysis_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis record not found.")

    advice_data = get_disease_record(record["predicted_class"])
    conf = float(record["confidence"])

    return AnalysisResponse(
        id=record["id"],
        timestamp=record["timestamp"],
        image_url=record["image_path"],
        thumbnail_url=record.get("thumbnail_path") or record["image_path"],
        plant=record["plant"],
        predicted_class=record["predicted_class"],
        display_name=advice_data.get("display_name", record["predicted_class"]),
        is_healthy=advice_data.get("is_healthy", False),
        confidence=round(conf, 4),
        confidence_percent=round(conf * 100, 1),
        is_low_confidence=conf < 0.60,
        is_simulated=bool(record["is_simulated"]),
        source=record["source"],
        advice=DiseaseInfo(**advice_data),
        top_predictions=[]
    )


@router.delete("/{analysis_id}")
def delete_history_item(analysis_id: int):
    """Delete single analysis and remove uploaded files from disk."""
    record = delete_analysis_by_id(analysis_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis record not found.")

    # Clean up image files if they exist in uploads/
    img_path_rel = record.get("image_path", "").lstrip("/").replace("uploads/", "")
    thumb_path_rel = record.get("thumbnail_path", "").lstrip("/").replace("uploads/", "")

    if img_path_rel:
        p = UPLOADS_DIR / img_path_rel
        if p.exists() and p.is_file():
            try:
                p.unlink()
            except Exception:
                pass

    if thumb_path_rel:
        p = UPLOADS_DIR / thumb_path_rel
        if p.exists() and p.is_file():
            try:
                p.unlink()
            except Exception:
                pass

    return {"status": "ok", "deleted_id": analysis_id}


@router.delete("")
def clear_all_history():
    """Clear all analysis history records and remove uploaded files."""
    records = delete_all_analyses_history()
    for record in records:
        img_path_rel = record.get("image_path", "").lstrip("/").replace("uploads/", "")
        thumb_path_rel = record.get("thumbnail_path", "").lstrip("/").replace("uploads/", "")

        if img_path_rel:
            p = UPLOADS_DIR / img_path_rel
            if p.exists() and p.is_file():
                try:
                    p.unlink()
                except Exception:
                    pass

        if thumb_path_rel:
            p = UPLOADS_DIR / thumb_path_rel
            if p.exists() and p.is_file():
                try:
                    p.unlink()
                except Exception:
                    pass

    return {"status": "ok", "deleted_count": len(records)}
