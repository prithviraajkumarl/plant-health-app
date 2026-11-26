"""Inference engine for PlantHealthApp running TFLite model."""

import json
import uuid
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional
import numpy as np
from PIL import Image, ImageOps

from app.backend.config import (
    MODEL_FILE,
    CATEGORIES_FILE,
    CONFIDENCE_THRESHOLD,
    UPLOADS_DIR
)
from app.backend.seed_data import get_disease_info

# Global interpreter instance
_INTERPRETER = None
_CATEGORIES: List[str] = []
_INPUT_DETAILS = None
_OUTPUT_DETAILS = None


def get_interpreter():
    """Lazily load and cache the TFLite interpreter and categories."""
    global _INTERPRETER, _CATEGORIES, _INPUT_DETAILS, _OUTPUT_DETAILS

    if _INTERPRETER is not None:
        return _INTERPRETER

    if not MODEL_FILE.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_FILE}")

    if not CATEGORIES_FILE.exists():
        raise FileNotFoundError(f"Categories file not found at {CATEGORIES_FILE}")

    # Load categories
    with open(CATEGORIES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        _CATEGORIES = list(data.keys())

    # Try importing LiteRT / TFLite interpreter
    try:
        from ai_edge_litert.interpreter import Interpreter
        _INTERPRETER = Interpreter(model_path=str(MODEL_FILE))
    except ImportError:
        try:
            import tflite_runtime.interpreter as tflite
            _INTERPRETER = tflite.Interpreter(model_path=str(MODEL_FILE))
        except ImportError:
            try:
                import tensorflow as tf
                _INTERPRETER = tf.lite.Interpreter(model_path=str(MODEL_FILE))
            except Exception as e:
                raise RuntimeError(f"Could not load any TFLite runtime: {e}")

    _INTERPRETER.allocate_tensors()
    _INPUT_DETAILS = _INTERPRETER.get_input_details()
    _OUTPUT_DETAILS = _INTERPRETER.get_output_details()

    return _INTERPRETER


def preprocess_image(image: Image.Image) -> Tuple[np.ndarray, Image.Image]:
    """Correct EXIF orientation, convert to RGB, and resize to (224, 224)."""
    # Auto-rotate according to EXIF tag if present
    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        pass

    image_rgb = image.convert("RGB")
    resized = image_rgb.resize((224, 224), Image.Resampling.BILINEAR)

    # Normalize to [0, 1] as expected by the trained MobileNet model
    arr = np.array(resized, dtype=np.float32) / 255.0
    tensor = np.expand_dims(arr, axis=0)

    return tensor, image_rgb


def save_image_and_thumbnail(image: Image.Image) -> Tuple[str, str, Path, Path]:
    """Save user image and generated thumbnail to uploads directory."""
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    thumbs_dir = UPLOADS_DIR / "thumbs"
    thumbs_dir.mkdir(parents=True, exist_ok=True)

    uid = uuid.uuid4().hex[:12]
    filename = f"scan_{uid}.jpg"
    thumb_name = f"thumb_{uid}.jpg"

    file_path = UPLOADS_DIR / filename
    thumb_path = thumbs_dir / thumb_name

    # Max dimension 1200 for stored image
    img_to_save = image.copy()
    img_to_save.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
    img_to_save.save(file_path, "JPEG", quality=88)

    # Thumbnail for fast listing (160x160)
    thumb_img = ImageOps.fit(image.copy(), (160, 160), Image.Resampling.LANCZOS)
    thumb_img.save(thumb_path, "JPEG", quality=80)

    rel_image_url = f"/uploads/{filename}"
    rel_thumb_url = f"/uploads/thumbs/{thumb_name}"

    return rel_image_url, rel_thumb_url, file_path, thumb_path


def run_inference(image: Image.Image) -> Dict[str, Any]:
    """Execute model inference and return predicted class, confidence, top predictions."""
    interpreter = get_interpreter()
    input_tensor, processed_img = preprocess_image(image)

    interpreter.set_tensor(_INPUT_DETAILS[0]["index"], input_tensor)
    interpreter.invoke()
    preds = interpreter.get_tensor(_OUTPUT_DETAILS[0]["index"])[0]

    # Softmax / probability distribution check
    # If logits instead of probabilities, apply softmax
    if np.sum(preds) < 0.9 or np.sum(preds) > 1.1 or np.any(preds < 0):
        exp_preds = np.exp(preds - np.max(preds))
        probs = exp_preds / np.sum(exp_preds)
    else:
        probs = preds

    # Sort descending
    top_indices = np.argsort(probs)[::-1]
    best_idx = int(top_indices[0])
    best_conf = float(probs[best_idx])
    best_label = _CATEGORIES[best_idx]

    is_low_conf = best_conf < CONFIDENCE_THRESHOLD

    # Compile top 3 predictions
    top_preds = []
    for idx in top_indices[:3]:
        lbl = _CATEGORIES[int(idx)]
        c = float(probs[int(idx)])
        info = get_disease_info(lbl)
        top_preds.append({
            "class_label": lbl,
            "display_name": info["display_name"],
            "plant": info["plant"],
            "confidence": round(c, 4),
            "confidence_percent": round(c * 100, 1),
            "is_healthy": info["is_healthy"]
        })

    disease_advice = get_disease_info(best_label)

    return {
        "predicted_class": best_label,
        "plant": disease_advice["plant"],
        "display_name": disease_advice["display_name"],
        "is_healthy": disease_advice["is_healthy"],
        "confidence": round(best_conf, 4),
        "confidence_percent": round(best_conf * 100, 1),
        "is_low_confidence": is_low_conf,
        "advice": disease_advice,
        "top_predictions": top_preds,
        "processed_image": processed_img
    }
