# How to Host Online 24/7 for 2 Months (Free)

This guide explains how to host the **Plant Health Detection App** online continuously for **2 months (or indefinitely)** at **$0 cost**, with permanent HTTPS URLs accessible from any smartphone or laptop worldwide.

---

## Comparison of Hosting Options

| Method | Uptime | Free Duration | Sleeping? | Setup Difficulty | Best For |
|---|---|---|---|---|---|
| **Option 1: Hugging Face Spaces** ⭐ *(Recommended)* | 24/7 Always-On | **Permanent (Unlimited)** | **No** (Stays awake 24/7) | 🟢 Very Easy (3 mins) | Best overall: 16 GB RAM, zero cost, no credit card, never expires |
| **Option 2: Render.com** | 24/7 (On demand) | Free tier forever | Yes (Wakes in 30s when opened) | 🟡 Medium (Requires GitHub) | Good if you already use GitHub & Render |
| **Option 3: PC Background Runner (Local Host)** | As long as PC is on | Unlimited | Depends on laptop power | 🟢 1-Click | If you want to host directly from your machine |

---

## Option 1: Hugging Face Spaces (Recommended — 100% Free Forever)

Hugging Face Spaces provides **free CPU hardware** (2 vCPU, 16 GB RAM, 50 GB storage) with a permanent SSL/HTTPS domain that **does not shut down after 2 months** and does not require a credit card.

### Step 1: Create a Free Hugging Face Account
1. Go to [https://huggingface.co/join](https://huggingface.co/join) and create a free account.
2. Verify your email.

### Step 2: Create a New Space
1. Visit [https://huggingface.co/new-space](https://huggingface.co/new-space).
2. Set **Space name** (e.g., `plant-health-app`).
3. Select **License**: `MIT`.
4. Select **Space SDK**: **Docker** -> **Blank**.
5. Set **Space hardware**: **CPU basic • 2 vCPU • 16 GB RAM • Free**.
6. Visibility: **Public**.
7. Click **Create Space**.

### Step 3: Push Your Code to the Space
In your Space page, Hugging Face gives you a Git URL (e.g., `https://huggingface.co/spaces/YOUR_USERNAME/plant-health-app`).

Open PowerShell or Command Prompt in `PlantHealthApp`:
```cmd
cd "C:\Users\Prithvi\OneDrive\Documents\praveen\PlantHealthApp"

:: 1. Initialize git if not already done
git init
git add .
git commit -m "Deploy Plant Health Detection App"

:: 2. Add your Hugging Face Space as a remote
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/plant-health-app

:: 3. Push your app
git push --force space master:main
```
*(When prompted for credentials, use your Hugging Face username and an Access Token generated at [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) with "Write" permissions).*

### Step 4: Your App is Live!
- Hugging Face automatically detects the provided `Dockerfile`, builds the container, and starts the server on port `7860`.
- Within 2 minutes, your permanent public URL will be live at:
  ```
  https://YOUR_USERNAME-plant-health-app.hf.space
  ```
- Anyone on mobile data or Wi-Fi can scan the QR code or visit this link anytime over the next 2 months (and beyond).

---

## Option 2: Render.com (Automated GitHub Deployment)

Render allows you to host web apps directly connected to your GitHub repository for free.

### Step 1: Push Project to GitHub
1. Create a free repository on [GitHub](https://github.com/new) named `plant-health-app`.
2. Push your project:
   ```cmd
   cd "C:\Users\Prithvi\OneDrive\Documents\praveen\PlantHealthApp"
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/plant-health-app.git
   git push -u origin main
   ```

### Step 2: Deploy on Render
1. Sign up for free at [https://render.com](https://render.com).
2. Click **New +** -> **Web Service**.
3. Select your GitHub repository `plant-health-app`.
4. Choose **Environment**: **Docker**.
5. Set **Instance Type**: **Free**.
6. Click **Deploy Web Service**.
7. Render automatically reads `render.yaml` and launches your app at `https://plant-health-app.onrender.com`.

---

## Option 3: Host 24/7 from your PC via Cloudflare Named Tunnel

If you want the app to run directly from your laptop without uploading to external platforms:

1. **Keep Windows Awake**:
   In Windows Settings -> **System** -> **Power & battery**, set *"When plugged in, turn off my screen after: 10 minutes"* and *"Put my device to sleep: **Never**"*.
2. **Permanent Free Cloudflare Domain**:
   With a free Cloudflare account, you can create a permanent named tunnel (e.g. `plants.yourdomain.com` or a free Cloudflare tunnel token) that automatically reconnects even if your PC restarts.
3. **Background Run**:
   You can run `app/tools/run_online.py` minimized in the background.

---

## Verification Checklist After Hosting
1. Open the public HTTPS URL on your phone using mobile 4G/5G data (disconnect from Wi-Fi to test).
2. Verify that **In-App Live Camera** requests permission and streams video (since HTTPS is active).
3. Tap **AutoSim** to confirm TFLite inference runs on the cloud host and persists in SQLite.
4. Open the **History** tab to verify scan persistence.
