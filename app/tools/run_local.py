"""Local network runner for PlantHealthApp."""

import os
import sys
import json
import socket
import webbrowser
import subprocess
from pathlib import Path

# Paths
APP_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = APP_DIR.parent
RUNTIME_DIR = APP_DIR / "runtime"
CONNECTION_FILE = RUNTIME_DIR / "connection.json"
PORT = 8000


def get_lan_ip() -> str:
    """Detect LAN IPv4 address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def check_firewall_rule():
    """Check or add Windows Firewall rule for port 8000."""
    try:
        # Check if rule exists
        chk = subprocess.run(
            ["netsh", "advfirewall", "firewall", "show", "rule", "name=PlantHealthApp_8000"],
            capture_output=True,
            text=True
        )
        if "No rules match" in chk.stdout or chk.returncode != 0:
            print("[Firewall] Adding inbound firewall rule for port 8000...")
            res = subprocess.run(
                ["netsh", "advfirewall", "firewall", "add", "rule",
                 "name=PlantHealthApp_8000", "dir=in", "action=allow",
                 "protocol=TCP", f"localport={PORT}"],
                capture_output=True,
                text=True
            )
            if res.returncode == 0:
                print("[Firewall] Rule added successfully.")
            else:
                print("[Firewall Note] Could not add rule automatically (standard user permissions).")
                print("                If other devices on your Wi-Fi cannot connect, right-click")
                print("                1_START_LOCAL.bat and select 'Run as Administrator' once.")
    except Exception as e:
        print(f"[Firewall Check] Note: {e}")


def main():
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    lan_ip = get_lan_ip()
    lan_url = f"http://{lan_ip}:{PORT}"
    local_url = f"http://localhost:{PORT}"

    # Write connection info for app and QR code
    conn_data = {
        "mode": "local",
        "url": lan_url,
        "local_url": local_url,
        "ip": lan_ip,
        "port": PORT
    }
    with open(CONNECTION_FILE, "w", encoding="utf-8") as f:
        json.dump(conn_data, f, indent=2)

    # Check firewall
    check_firewall_rule()

    # Print beautiful banner
    print("\n" + "=" * 70)
    print("   PLANT HEALTH DETECTION APP - LOCAL NETWORK MODE")
    print("=" * 70)
    print(f"   Laptop / Localhost:    {local_url}")
    print(f"   Phone / Wi-Fi Network: {lan_url}")
    print("=" * 70)
    print("   1. Open the URL above on any phone or tablet on the same Wi-Fi.")
    print("   2. Or click 'Connect Phone' in the app to scan the QR code.")
    print("   3. Press Ctrl+C in this console window to stop the server.")
    print("=" * 70 + "\n")

    # Automatically open laptop browser
    try:
        webbrowser.open(local_url)
    except Exception:
        pass

    # Start uvicorn
    import uvicorn
    try:
        uvicorn.run("app.backend.main:app", host="0.0.0.0", port=PORT, log_level="info")
    except KeyboardInterrupt:
        print("\n[Server] Stopped by user.")
    finally:
        if CONNECTION_FILE.exists():
            try:
                CONNECTION_FILE.unlink()
            except Exception:
                pass
        print("[Shutdown] Cleaned up runtime state.")


if __name__ == "__main__":
    main()
