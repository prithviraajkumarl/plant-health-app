# REST API Reference

The Plant Health Detection App exposes a RESTful API powered by FastAPI.

- **Base URL (Local)**: `http://localhost:8000` (or `http://192.168.x.x:8000`)
- **Base URL (Online)**: `https://*.trycloudflare.com`
- **Interactive OpenAPI Documentation**: Available at `/docs` (Swagger UI) and `/redoc`.

---

## Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/analyze` | Analyze leaf image via multipart upload |
| `POST` | `/api/autosim` | Run instant AutoSim simulation on a sample leaf |
| `GET` | `/api/history` | List previous diagnoses with thumbnails |
| `GET` | `/api/history/{id}` | Retrieve full details of a specific diagnosis |
| `DELETE` | `/api/history/{id}` | Delete a diagnosis and remove stored images |
| `DELETE` | `/api/history` | Clear entire diagnosis history |
| `GET` | `/api/diseases` | List all 38+ plant disease and healthy profiles |
| `GET` | `/api/diseases/{class_label}` | Get detailed profile for a specific disease class |
| `GET` | `/api/connection-info` | Get active connection mode and mobile URLs |
| `GET` | `/api/qr.svg` | Generate vector SVG QR code for current URL |
| `GET` | `/api/qr.png` | Generate raster PNG QR code for current URL |
| `GET` | `/api/samples` | List bundled sample leaf images |
| `GET` | `/api/health` | Health check verifying model and database status |

---

## Endpoint Details

### 1. `POST /api/analyze`

Upload a leaf photo from a file picker, drag-and-drop, or captured camera canvas.

- **Content-Type**: `multipart/form-data`
- **Form Parameters**:
  - `file`: Image binary (`image/jpeg`, `image/png`, or `image/webp`). Max 15 MB.
  - `source`: (Optional) `"upload"` or `"camera"` (default: `"upload"`).

#### Example Request (cURL)
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@tomato_leaf.jpg" \
  -F "source=upload"
```

#### Example Response (`200 OK`)
```json
{
  "id": 14,
  "timestamp": "2026-11-25T22:38:15",
  "image_url": "/uploads/scan_e901f4c3a2.jpg",
  "thumbnail_url": "/uploads/thumbs/thumb_e901f4c3a2.jpg",
  "plant": "Tomato",
  "predicted_class": "Tomato___Early_blight",
  "display_name": "Early Blight",
  "is_healthy": false,
  "confidence": 0.9482,
  "confidence_percent": 94.8,
  "is_low_confidence": false,
  "is_simulated": false,
  "source": "upload",
  "advice": {
    "class_label": "Tomato___Early_blight",
    "plant": "Tomato",
    "display_name": "Early Blight",
    "is_healthy": false,
    "description": "Concentric rings forming a distinctive target board pattern...",
    "cause": "Fungus Alternaria linariae. Overwinters in old tomato vines...",
    "treatment": "Prune away lower yellowing and infected leaves...",
    "prevention": "Mulch the soil heavily around tomato plants to stop soil splash..."
  },
  "top_predictions": [
    {
      "class_label": "Tomato___Early_blight",
      "display_name": "Early Blight",
      "plant": "Tomato",
      "confidence": 0.9482,
      "confidence_percent": 94.8,
      "is_healthy": false
    },
    {
      "class_label": "Tomato___Septoria_leaf_spot",
      "display_name": "Septoria Leaf Spot",
      "plant": "Tomato",
      "confidence": 0.0312,
      "confidence_percent": 3.1,
      "is_healthy": false
    }
  ],
  "qr_url": "http://192.168.1.15:8000"
}
```

---

### 2. `POST /api/autosim`

Executes a complete AI analysis using a bundled sample leaf image without requiring user file input. Persists the result as simulated in SQLite.

- **Query Parameters**:
  - `sample_name`: (Optional) Specific sample filename (e.g. `apple_scab.jpg`). If omitted, selects randomly from `app/samples/`.

#### Example Response (`200 OK`)
```json
{
  "id": 15,
  "timestamp": "2026-11-25T22:39:10",
  "image_url": "/uploads/scan_47a1bc82f0.jpg",
  "thumbnail_url": "/uploads/thumbs/thumb_47a1bc82f0.jpg",
  "plant": "Apple",
  "predicted_class": "Apple___Apple_scab",
  "display_name": "Apple Scab",
  "is_healthy": false,
  "confidence": 0.9802,
  "confidence_percent": 98.0,
  "is_low_confidence": false,
  "is_simulated": true,
  "source": "autosim",
  "advice": { ... },
  "top_predictions": [ ... ],
  "qr_url": "http://192.168.1.15:8000"
}
```

---

### 3. `GET /api/history`

Retrieves a paginated list of past diagnoses, ordered newest first.

- **Query Parameters**:
  - `limit`: (Optional) Max items to return (1–200, default 50).
  - `offset`: (Optional) Pagination offset (default 0).

#### Example Response (`200 OK`)
```json
[
  {
    "id": 15,
    "timestamp": "2026-11-25T22:39:10",
    "image_url": "/uploads/scan_47a1bc82f0.jpg",
    "thumbnail_url": "/uploads/thumbs/thumb_47a1bc82f0.jpg",
    "plant": "Apple",
    "predicted_class": "Apple___Apple_scab",
    "display_name": "Apple Scab",
    "is_healthy": false,
    "confidence": 0.9802,
    "confidence_percent": 98.0,
    "is_low_confidence": false,
    "is_simulated": true,
    "source": "autosim"
  }
]
```

---

### 4. `DELETE /api/history/{id}`

Deletes an analysis record from SQLite and removes its associated image files from `app/uploads/`.

#### Example Response (`200 OK`)
```json
{
  "status": "ok",
  "deleted_id": 15
}
```

---

### 5. `GET /api/connection-info`

Provides connection metadata for mobile device linking and QR codes.

#### Example Response (`200 OK`)
```json
{
  "mode": "local",
  "url": "http://192.168.1.15:8000",
  "local_url": "http://localhost:8000",
  "ip": "192.168.1.15",
  "port": 8000,
  "qr_svg_url": "/api/qr.svg"
}
```

---

### 6. `GET /api/health`

Health check endpoint for automated verifications and status monitoring.

#### Example Response (`200 OK`)
```json
{
  "status": "ok",
  "model_loaded": true,
  "classes_count": 38,
  "database_ok": true,
  "connection_mode": "local",
  "version": "1.0.0"
}
```
