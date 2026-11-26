"""Public Internet tunnel runner for PlantHealthApp using Cloudflare Quick Tunnel."""

import os
import sys
import re
import json
import time
import atexit
import signal
import urllib.request
import webbrowser
import subprocess
from pathlib import Path

# Paths
APP_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = APP_DIR.parent
RUNTIME_DIR = APP_DIR / "runtime"
TOOLS_DIR = APP_DIR / "tools"
CONNECTION_FILE = RUNTIME_DIR / "connection.json"
CLOUDFLARED_EXE = TOOLS_DIR / "cloudflared.exe"
PORT = 8000

# Track active subprocesses
server_process = None
tunnel_process = None


def kill_proc_tree(pid: int):
    """Ensure entire process tree is terminated on Windows."""
    try:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def cleanup():
    """Cleanup all processes and runtime files on termination."""
    global server_process, tunnel_process
    print("\n[Shutdown] Stopping server and Cloudflare tunnel processes...")

    if tunnel_process:
        try:
            kill_proc_tree(tunnel_process.pid)
            tunnel_process.kill()
        except Exception:
            pass

    if server_process:
        try:
            kill_proc_tree(server_process.pid)
            server_process.kill()
        except Exception:
            pass

    # Ensure any stray cloudflared is killed
    try:
        subprocess.run(["taskkill", "/F", "/IM", "cloudflared.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

    if CONNECTION_FILE.exists():
        try:
            CONNECTION_FILE.unlink()
        except Exception:
            pass

    print("[Shutdown] Completed cleanly. No orphan processes remain.")


# Register exit handlers
atexit.register(cleanup)
signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))


def ensure_cloudflared() -> Path:
    """Download cloudflared.exe if missing."""
    if CLOUDFLARED_EXE.exists() and CLOUDFLARED_EXE.stat().st_size > 10_000_000:
        return CLOUDFLARED_EXE

    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    print(f"[Setup] Downloading Cloudflare Quick Tunnel tool (cloudflared.exe)...")
    try:
        urllib.request.urlretrieve(url, str(CLOUDFLARED_EXE))
        print(f"[Setup] Downloaded cloudflared.exe ({CLOUDFLARED_EXE.stat().st_size // (1024*1024)} MB).")
        return CLOUDFLARED_EXE
    except Exception as e:
        print(f"[Error] Failed to download cloudflared.exe: {e}")
        sys.exit(1)


def main():
    global server_process, tunnel_process
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Ensure cloudflared is present
    cf_path = ensure_cloudflared()

    # 2. Start FastAPI Backend Server
    print("[1/3] Starting Plant Health backend server on port 8000...")
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.backend.main:app", "--host", "127.0.0.1", "--port", str(PORT)],
        cwd=str(ROOT_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True
    )

    # Allow server 1.5 seconds to bind
    time.sleep(1.5)

    # 3. Start Cloudflare Quick Tunnel
    print("[2/3] Establishing Cloudflare Quick Tunnel (no account required, free HTTPS)...")
    tunnel_cmd = [str(cf_path), "tunnel", "--url", f"http://127.0.0.1:{PORT}"]
    
    tunnel_process = subprocess.Popen(
        tunnel_cmd,
        cwd=str(TOOLS_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    public_url = None
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

    # Read tunnel output to capture public URL
    print("[3/3] Waiting for public tunnel address...")
    start_time = time.time()
    while time.time() - start_time < 35:
        line = tunnel_process.stdout.readline()
        if not line and tunnel_process.poll() is not None:
            break
        if line:
            match = url_pattern.search(line)
            if match:
                public_url = match.group(0)
                break

    if not public_url:
        print("[Error] Could not obtain Cloudflare Tunnel URL within timeout.")
        sys.exit(1)

    # Write connection info for application and QR code
    conn_data = {
        "mode": "online",
        "url": public_url,
        "local_url": f"http://localhost:{PORT}",
        "port": PORT
    }
    with open(CONNECTION_FILE, "w", encoding="utf-8") as f:
        json.dump(conn_data, f, indent=2)

    # Display prominent banner
    print("\n" + "=" * 75)
    print("   PLANT HEALTH DETECTION APP - PUBLIC ONLINE MODE (TUNNEL)")
    print("=" * 75)
    print(f"   Public HTTPS URL:   {public_url}")
    print(f"   Local Address:      http://localhost:{PORT}")
    print("=" * 75)
    print("   • Reachable from any phone anywhere (mobile data or Wi-Fi).")
    print("   • Live camera streaming and PWA features active under HTTPS.")
    print("   • AutoSim or 'Connect Phone' will display QR code for this URL.")
    print("   • Press Ctrl+C in this window to stop both the server and tunnel.")
    print("=" * 75 + "\n")

    # Open browser with public URL
    try:
        webbrowser.open(public_url)
    except Exception:
        pass

    # Monitor processes until user interrupt
    try:
        while True:
            time.sleep(0.5)
            if server_process.poll() is not None or tunnel_process.poll() is not None:
                print("\n[Alert] A process terminated unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\n[Exit] Stop signal received.")
    finally:
        cleanup()


if __name__ == "__main__":
    main()
