"""Diseases router for exploring crop disease knowledge base."""

from typing import List
from fastapi import APIRouter, HTTPException

from app.backend.schemas import DiseaseInfo
from app.backend.database import get_all_diseases_records, get_disease_record

router = APIRouter(prefix="/api/diseases", tags=["diseases"])


@router.get("", response_model=List[DiseaseInfo])
def list_diseases():
    """Get all 38+ plant diseases and healthy crop profiles in the database."""
    records = get_all_diseases_records()
    return [DiseaseInfo(**r) for r in records]


@router.get("/{class_label}", response_model=DiseaseInfo)
def get_disease(class_label: str):
    """Get specific disease or healthy profile details."""
    record = get_disease_record(class_label)
    if not record:
        raise HTTPException(status_code=404, detail="Disease label not found.")
    return DiseaseInfo(**record)
