# Troubleshooting Guide

Solutions and diagnostics for common issues encountered during setup, networking, camera capture, and tunnel operation.

---

## 1. Phone Cannot Connect over Wi-Fi (`1_START_LOCAL.bat`)

### Symptom
You can open `http://localhost:8000` on your laptop, but your phone shows *"This site can't be reached"* or *"Connection timed out"* when opening `http://192.168.x.x:8000`.

### Causes & Fixes

#### A. Windows Defender Firewall Blocking Inbound Port 8000
Windows Firewall frequently blocks incoming connections from other devices on the local network.
- **Fix 1 (One-click Admin)**: Right-click `1_START_LOCAL.bat` and select **"Run as Administrator"** once. The script will automatically execute:
  ```cmd
  netsh advfirewall firewall add rule name="PlantHealthApp_8000" dir=in action=allow protocol=TCP localport=8000
  ```
- **Fix 2 (Manual GUI)**:
  1. Open Windows Search and type **"Windows Defender Firewall"**.
  2. Click **"Allow an app or feature through Windows Defender Firewall"**.
  3. Ensure **Python** has checkboxes enabled for **Private** networks.

#### B. Phone and Laptop on Different Wi-Fi Networks
- Ensure your phone is not using cellular mobile data instead of Wi-Fi.
- Check if your router has separate 2.4 GHz and 5 GHz networks or a "Guest Wi-Fi". Many guest networks enable **AP Isolation (Client Isolation)**, which blocks connected devices from communicating with one another. Connect both devices to the primary home/office Wi-Fi.

#### C. IP Address Changed
- If your router reassigns your laptop's DHCP address, restart `1_START_LOCAL.bat`. The script re-interrogates network adapters on every start and displays the new IP.

---

## 2. In-App Live Camera Blocked on Phone Browser

### Symptom
Tapping the in-app camera button on a mobile phone shows an alert or fails to stream video.

### Explanation & Browser Security Rule
Modern mobile browsers (Chrome on Android, Safari on iOS) enforce a strict security policy:
- `navigator.mediaDevices.getUserMedia` (live video streaming) is **only permitted on Secure Contexts** (`https://*` or `http://localhost`).
- Plain unencrypted LAN IP addresses (`http://192.168.x.x`) are considered **insecure contexts**.

### Built-in Handling & Solutions
1. **Built-in Native Camera Fallback**:
   The app detects when it is running in an insecure context. Clicking **"In-App Live Camera"** or **"Phone Camera (Direct)"** will automatically open your phone's native camera app using `<input type="file" accept="image/*" capture="environment">`. Once you take the picture, it feeds directly into the AI analysis pipeline.
2. **Switch to Online Mode (`2_START_ONLINE.bat`)**:
   Online mode serves the application over a genuine public **HTTPS** URL (`https://*.trycloudflare.com`). Live camera streaming works unrestricted in Safari, Chrome, and Edge.

---

## 3. Port 8000 Already in Use

### Symptom
When starting the server, you receive an error:
`[Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000): only one usage of each socket address is normally permitted`

### Solution
Another application or an earlier instance of Python is still bound to port 8000.
1. Open PowerShell and find the Process ID (PID) occupying port 8000:
   ```powershell
   Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess
   ```
2. Terminate the process:
   ```cmd
   taskkill /F /PID <PID>
   ```
3. Re-run `1_START_LOCAL.bat`.

---

## 4. Cloudflare Tunnel Not Starting (`2_START_ONLINE.bat`)

### Symptom
The console hangs on `Waiting for public tunnel address...` or displays `Could not obtain Cloudflare Tunnel URL within timeout`.

### Causes & Fixes
- **Missing or Corrupted `cloudflared.exe`**:
  If the initial download was interrupted, delete `app/tools/cloudflared.exe` and re-run `2_START_ONLINE.bat`. The launcher will re-download the binary automatically.
- **Outbound UDP/QUIC Blocked by Network**:
  Some corporate or campus networks block non-standard outbound ports. Cloudflare Tunnel uses port 7844 (UDP) and port 443 (TCP). If restricted, test on your home Wi-Fi or phone hotspot.
- **Antivirus Interference**:
  Certain antivirus software may flag newly downloaded tunneling utilities. Whitelist `app/tools/cloudflared.exe`.

---

## 5. Clean Process Termination

### Ensuring No Orphaned Processes Remain
Both launchers are engineered with cleanup routines:
- When you press `Ctrl+C` in the console or close the window, the supervisor script invokes `taskkill /F /T /PID` to terminate the entire process hierarchy of both the uvicorn server and `cloudflared.exe`.
- The temporary state file `app/runtime/connection.json` is automatically deleted.
- If you ever need to manually verify no background processes remain:
  ```cmd
  taskkill /F /IM cloudflared.exe
  ```
