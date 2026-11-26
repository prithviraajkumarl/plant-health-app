"""Pydantic schemas for PlantHealthApp API."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DiseaseInfo(BaseModel):
    class_label: str
    plant: str
    display_name: str
    is_healthy: bool = False
    description: str
    cause: str
    treatment: str
    prevention: str


class TopPrediction(BaseModel):
    class_label: str
    display_name: str
    plant: str
    confidence: float
    confidence_percent: float
    is_healthy: bool


class AnalysisResponse(BaseModel):
    id: int
    timestamp: str
    image_url: str
    thumbnail_url: str
    plant: str
    predicted_class: str
    display_name: str
    is_healthy: bool
    confidence: float
    confidence_percent: float
    is_low_confidence: bool
    is_simulated: bool = False
    source: str = "upload"  # upload, camera, autosim
    advice: DiseaseInfo
    top_predictions: List[TopPrediction] = []
    qr_url: Optional[str] = None


class HistoryItem(BaseModel):
    id: int
    timestamp: str
    image_url: str
    thumbnail_url: str
    plant: str
    predicted_class: str
    display_name: str
    is_healthy: bool
    confidence: float
    confidence_percent: float
    is_low_confidence: bool
    is_simulated: bool
    source: str


class ConnectionInfo(BaseModel):
    mode: str
    url: str
    local_url: str
    ip: Optional[str] = None
    port: int
    qr_svg_url: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    classes_count: int
    database_ok: bool
    connection_mode: str
    version: str = "1.0.0"
