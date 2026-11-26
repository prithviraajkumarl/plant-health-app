# Credits, Datasets & Licenses

The Plant Health Detection App builds upon open-source datasets, models, and community software.

---

## 1. Base Project

- **Repository**: [healthycropping](https://github.com/keylorpineda/healthycropping)
- **Author**: Keylor Pineda
- **License**: MIT License
- **Contributions Adapted**:
  - Inspiration for FastAPI backend architecture and agronomic care workflows.
  - Data schema concepts, disease taxonomies, and agronomic knowledge base concepts for tropical crops (Banana, Cacao, Coffee) incorporated alongside PlantVillage classes.

---

## 2. Machine Learning Model & Weights

- **Model Repository**: [Plant-Diseases-Detector](https://github.com/obeshor/Plant-Diseases-Detector)
- **Author**: Yannick Serge Obam (`obeshor`)
- **Architecture**: MobileNetV2 trained for edge and mobile deployment with TensorFlow Lite.
- **Weights File**: `app/models/plant_disease_model.tflite` (11.57 MB).
- **Categories Mapping**: `app/models/categories.json` (38 classes).
- **License**: MIT License.

---

## 3. Dataset

- **Name**: [PlantVillage Dataset](https://plantvillage.psu.edu/)
- **Authors**: David P. Hughes and Marcel Salathé (2015).
- **Citation**:
  > Hughes, D., & Salathé, M. (2015). *An open access repository of images on plant health to enable the development of mobile disease diagnostics.* arXiv preprint arXiv:1511.08060.
- **Dataset Description**: Over 54,306 curated images covering 14 plant species and 26 diseases along with healthy controls.
- **License**: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

---

## 4. Third-Party Software & Libraries

| Library / Tool | Primary Use | License |
|---|---|---|
| **FastAPI** | High-performance Python web framework | MIT License |
| **Uvicorn** | Lightning-fast ASGI web server implementation | BSD 3-Clause License |
| **Google LiteRT / TFLite** | Lightweight CPU inference engine for neural network models | Apache License 2.0 |
| **Pillow (PIL)** | Image loading, EXIF auto-transposition, and thumbnail creation | Historical Permission Notice and Disclaimer (HPND) |
| **SQLite** | Embedded zero-configuration serverless database engine | Public Domain |
| **Cloudflare `cloudflared`** | Secure zero-trust public HTTPS tunneling daemon | Apache License 2.0 |
| **QRCode.js (davidshimjs)** | Pure client-side JavaScript QR code generator | MIT License |
| **Python `qrcode`** | Server-side SVG & PNG QR code generation | BSD License |
| **Pydantic** | Data validation and schema enforcement | MIT License |
