# Plant Health Detection App

An on-device, AI-driven plant disease diagnosis and agronomic care guide for Windows, mobile phones, and laptops.

Built with a **FastAPI backend**, an on-device **MobileNet TensorFlow Lite** model, an embedded **SQLite database**, a modern **responsive Progressive Web App (PWA)**, and automated **double-click `.bat` launchers**.

---

## Key Features

- **Real On-Device AI Diagnosis**: Classifies plant health across **38 distinct disease and healthy categories** spanning 14 crops (Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Bell Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, and Tomato).
- **Comprehensive Agronomic Advice**: Every diagnosis delivers immediate descriptions, biological causes, actionable treatment steps, and preventive measures.
- **Three Input Modes**:
  1. **Upload & Drag-and-Drop**: From file picker or desktop drag-and-drop.
  2. **In-App Live Camera**: Live video preview with viewfinder, lens flipping (rear/front), and instant snapshot capture via `getUserMedia`.
  3. **Native Phone Camera**: Fallback capture directly invoking the smartphone camera app.
- **Context-Aware Security**: Automatically detects insecure HTTP contexts on mobile devices and provides seamless fallback to native camera capture, while activating full live video on HTTPS/localhost.
- **One-Click AutoSim Demo**: Instantly runs real AI inference on a bundled sample leaf, saves the diagnosis to the SQLite database, and presents a scannable QR code.
- **Zero-Configuration Launchers**:
  - `1_START_LOCAL.bat`: Runs on local network (`0.0.0.0:8000`), automatically detects your PC's Wi-Fi LAN IP, writes connection info, opens the browser, and prints a QR-ready link for any phone on the Wi-Fi.
  - `2_START_ONLINE.bat`: Launches the server and establishes a free public **Cloudflare Quick Tunnel** (`https://*.trycloudflare.com`), enabling instant encrypted access from mobile 4G/5G data anywhere without port forwarding or accounts.
- **Strict Process Hygiene**: Guaranteed clean shutdown on `Ctrl+C` or window closure with zero orphaned background processes.
- **Persistent SQLite Database**: Automatically seeds 38+ crop profiles and persists past scans with thumbnails, timestamps, and delete controls.

---

## Folder Layout

The project delivers this exact structure:

```
PlantHealthApp/
├── 1_START_LOCAL.bat        <- Local network mode (LAN Wi-Fi)
├── 2_START_ONLINE.bat       <- Public internet mode (Cloudflare HTTPS Tunnel)
├── docs/                    <- Comprehensive documentation
│   ├── README.md            <- Project overview & quickstart
│   ├── DATABASE.md          <- SQLite schema, ER diagram, sample data
│   ├── HOW_IT_WORKS.md      <- Architecture, ML pipeline & network flows
│   ├── API.md               <- Endpoint documentation & examples
│   ├── TROUBLESHOOTING.md   <- Solutions for network, firewall & camera
│   └── CREDITS_AND_LICENSES.md <- Base repo, datasets & licenses
└── app/                     <- Complete application package
    ├── backend/             <- FastAPI application & routers
    ├── frontend/            <- Responsive web UI (PWA, CSS, JS)
    ├── models/              <- MobileNet TFLite model & categories.json
    ├── samples/             <- Bundled sample leaf images for AutoSim
    ├── uploads/             <- Stored user scans and thumbnails
    ├── tools/               <- cloudflared.exe and Python runners
    ├── runtime/             <- Active connection state (connection.json)
    ├── db/                  <- SQLite database (plant_health.db)
    └── requirements.txt     <- Python dependencies
```

---

## System Requirements

- **Operating System**: Windows 10 or Windows 11 (64-bit).
- **Python**: Python 3.10, 3.11, or 3.12 installed.
- **Node.js**: **Not required** (the web UI is pre-built vanilla HTML5/ES6/CSS).
- **Hardware**: Any modern dual-core CPU with 2 GB RAM (inference runs in ~40 ms on CPU).

---

## How to Run

### Mode 1: Local Wi-Fi Network Mode (`1_START_LOCAL.bat`)

Use this mode when your laptop and smartphone are connected to the same Wi-Fi router.

1. Double-click `1_START_LOCAL.bat`.
2. On first run, it creates the isolated virtual environment `app\.venv` and installs all dependencies automatically.
3. The launcher detects your laptop's local IPv4 address (e.g. `http://192.168.1.15:8000`) and displays:
   ```
   ======================================================================
      PLANT HEALTH DETECTION APP - LOCAL NETWORK MODE
   ======================================================================
      Laptop / Localhost:    http://localhost:8000
      Phone / Wi-Fi Network: http://192.168.1.15:8000
   ======================================================================
   ```
4. Your default browser opens to `http://localhost:8000`.
5. On your phone, connect to the same Wi-Fi and open `http://192.168.1.15:8000` (or click **Connect Phone** in the web UI to scan the QR code).
6. Press `Ctrl+C` or close the command window to stop the server cleanly.

### Mode 2: Public Internet Mode (`2_START_ONLINE.bat`)

Use this mode when your phone is on cellular data (4G/5G) or outside the local network.

1. Double-click `2_START_ONLINE.bat`.
2. The launcher starts the server and initiates a free Cloudflare Quick Tunnel.
3. It prints your unique, encrypted public HTTPS link:
   ```
   ======================================================================
      PLANT HEALTH DETECTION APP - PUBLIC ONLINE MODE (TUNNEL)
   ======================================================================
      Public HTTPS URL:   https://your-tunnel-name.trycloudflare.com
      Local Address:      http://localhost:8000
   ======================================================================
   ```
4. Your browser opens the public link. You can scan the QR code on any phone with an internet connection.
5. In this mode, full live camera streaming is active because the connection is encrypted with HTTPS.
6. Press `Ctrl+C` or close the window: the launcher terminates the server and the tunnel process tree cleanly, removing any temporary runtime files.

---

## Documentation Index

- [Database Schema & Architecture](DATABASE.md)
- [How It Works & ML Pipeline](HOW_IT_WORKS.md)
- [REST API Reference](API.md)
- [Troubleshooting & FAQs](TROUBLESHOOTING.md)
- [Credits, Datasets & Licenses](CREDITS_AND_LICENSES.md)
