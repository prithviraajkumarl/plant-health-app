/**
 * Plant Health Detection App - Client Application
 */

// Application State
const state = {
  activeView: 'scan',
  connectionInfo: null,
  activeStream: null,
  facingMode: 'environment',
  isSecure: window.isSecureContext,
  hasGetUserMedia: !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia),
  currentAnalysis: null,
  diseasesCache: []
};

// DOM Elements
const el = {
  // Navigation
  tabs: document.querySelectorAll('.nav-tab'),
  views: document.querySelectorAll('.view-section'),
  brand: document.getElementById('brandLogo'),
  modeBadge: document.getElementById('modeBadge'),
  btnOpenQr: document.getElementById('btnOpenQr'),
  
  // AutoSim
  btnAutoSim: document.getElementById('btnAutoSim'),
  
  // Inputs
  dropzone: document.getElementById('dropzone'),
  galleryInput: document.getElementById('galleryInput'),
  nativeCameraInput: document.getElementById('nativeCameraInput'),
  btnOpenGallery: document.getElementById('btnOpenGallery'),
  btnStartCamera: document.getElementById('btnStartCamera'),
  btnNativeCam: document.getElementById('btnNativeCam'),
  contextNotice: document.getElementById('contextNotice'),
  
  // Modals
  cameraModal: document.getElementById('cameraModal'),
  cameraVideo: document.getElementById('cameraVideo'),
  btnShutter: document.getElementById('btnShutter'),
  btnFlipCam: document.getElementById('btnFlipCam'),
  btnCloseCamera: document.getElementById('btnCloseCamera'),
  
  qrModal: document.getElementById('qrModal'),
  qrContainer: document.getElementById('qrContainer'),
  qrUrlText: document.getElementById('qrUrlText'),
  btnCopyQrUrl: document.getElementById('btnCopyQrUrl'),
  btnCloseQr: document.getElementById('btnCloseQr'),
  qrModeDesc: document.getElementById('qrModeDesc'),
  
  // Loading
  loadingOverlay: document.getElementById('loadingOverlay'),
  loadingText: document.getElementById('loadingText'),
  
  // Result
  resPlantBadge: document.getElementById('resPlantBadge'),
  resStatusBadge: document.getElementById('resStatusBadge'),
  resDiagnosisTitle: document.getElementById('resDiagnosisTitle'),
  resConfidenceVal: document.getElementById('resConfidenceVal'),
  resConfidenceBar: document.getElementById('resConfidenceBar'),
  resLowConfAlert: document.getElementById('resLowConfAlert'),
  resImage: document.getElementById('resImage'),
  resDesc: document.getElementById('resDesc'),
  resCause: document.getElementById('resCause'),
  resTreatment: document.getElementById('resTreatment'),
  resPrevention: document.getElementById('resPrevention'),
  resAltPredsBox: document.getElementById('resAltPredsBox'),
  resAltPredsList: document.getElementById('resAltPredsList'),
  btnScanAnother: document.getElementById('btnScanAnother'),
  btnResultQr: document.getElementById('btnResultQr'),
  
  // History
  historyList: document.getElementById('historyList'),
  historyEmpty: document.getElementById('historyEmpty'),
  btnClearHistory: document.getElementById('btnClearHistory'),
  
  // Diseases Catalog
  diseaseCatalogList: document.getElementById('diseaseCatalogList'),
  diseaseSearchInput: document.getElementById('diseaseSearchInput'),
  
  // Toast
  toastContainer: document.getElementById('toastContainer')
};

// Initialization
document.addEventListener('DOMContentLoaded', () => {
  initApp();
});

async function initApp() {
  setupNavigation();
  setupEventListeners();
  checkBrowserContext();
  await loadConnectionInfo();
  registerServiceWorker();
}

function showToast(message) {
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  el.toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 2600);
}

// Navigation
function setupNavigation() {
  el.tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.view;
      switchView(target);
    });
  });

  if (el.brand) {
    el.brand.addEventListener('click', () => switchView('scan'));
  }
}

function switchView(viewName) {
  state.activeView = viewName;
  el.tabs.forEach(tab => {
    tab.classList.toggle('active', tab.dataset.view === viewName);
  });
  el.views.forEach(v => {
    v.classList.toggle('active', v.id === `${viewName}View`);
  });

  if (viewName === 'history') {
    loadHistory();
  } else if (viewName === 'diseases') {
    loadDiseases();
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Browser & HTTPS Context Check
function checkBrowserContext() {
  // Over plain HTTP (non-localhost), getUserMedia is strictly forbidden by modern browsers
  const isSecure = window.isSecureContext || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  state.isSecure = isSecure;

  if (!isSecure) {
    if (el.contextNotice) {
      el.contextNotice.style.display = 'flex';
      el.contextNotice.innerHTML = `<span>⚠️ <strong>HTTP Local Mode:</strong> Browser security restricts live camera streams to HTTPS or localhost. Live camera button will open your phone's native camera directly.</span>`;
    }
  } else {
    if (el.contextNotice) {
      el.contextNotice.style.display = 'none';
    }
  }
}

// Connection & QR Code Info
async function loadConnectionInfo() {
  try {
    const res = await fetch('/api/connection-info');
    if (!res.ok) throw new Error('Failed to fetch connection info');
    const data = await res.json();
    state.connectionInfo = data;

    // Update Header Badge
    const isOnline = data.mode === 'online';
    el.modeBadge.innerHTML = `<span class="mode-dot" style="background: ${isOnline ? '#52b788' : '#e9c46a'}"></span> ${isOnline ? 'Online (Tunnel)' : 'Local Wi-Fi'}`;

    // Render QR Code in modal
    renderQrCode(data.url, isOnline);
  } catch (err) {
    console.warn('Could not load connection info:', err);
    el.modeBadge.innerHTML = `<span class="mode-dot"></span> Ready`;
  }
}

function renderQrCode(url, isOnline) {
  if (!el.qrContainer) return;
  el.qrContainer.innerHTML = '';

  // Set description
  if (el.qrModeDesc) {
    el.qrModeDesc.textContent = isOnline
      ? 'Public HTTPS Tunnel URL. Anyone on any network or mobile data can open this.'
      : 'Local Network IP. Connect your phone to the same Wi-Fi network to open.';
  }

  if (el.qrUrlText) {
    el.qrUrlText.textContent = url;
  }

  // Use locally bundled QRCode library
  if (typeof QRCode !== 'undefined') {
    try {
      new QRCode(el.qrContainer, {
        text: url,
        width: 196,
        height: 196,
        colorDark: '#1b4332',
        colorLight: '#ffffff',
        correctLevel: QRCode.CorrectLevel.M
      });
      return;
    } catch (e) {
      console.warn('QRCode library render failed, falling back to SVG:', e);
    }
  }

  // Fallback to backend SVG QR code
  const img = document.createElement('img');
  img.src = '/api/qr.svg?t=' + Date.now();
  img.alt = 'QR Code';
  img.style.width = '196px';
  img.style.height = '196px';
  el.qrContainer.appendChild(img);
}

function openQrModal() {
  if (state.connectionInfo) {
    renderQrCode(state.connectionInfo.url, state.connectionInfo.mode === 'online');
  }
  el.qrModal.classList.add('active');
}

function closeQrModal() {
  el.qrModal.classList.remove('active');
}

// Event Listeners
function setupEventListeners() {
  // QR Modal
  el.btnOpenQr.addEventListener('click', openQrModal);
  el.btnCloseQr.addEventListener('click', closeQrModal);
  el.btnResultQr.addEventListener('click', openQrModal);
  el.btnCopyQrUrl.addEventListener('click', () => {
    if (state.connectionInfo && state.connectionInfo.url) {
      navigator.clipboard.writeText(state.connectionInfo.url)
        .then(() => showToast('URL copied to clipboard!'))
        .catch(() => showToast('Could not copy URL'));
    }
  });

  // AutoSim Button
  el.btnAutoSim.addEventListener('click', handleAutoSim);

  // Gallery Picker
  el.btnOpenGallery.addEventListener('click', () => el.galleryInput.click());
  el.dropzone.addEventListener('click', (e) => {
    if (e.target !== el.btnStartCamera && e.target !== el.btnNativeCam) {
      el.galleryInput.click();
    }
  });

  el.galleryInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) handleFileSelected(file, 'upload');
  });

  // Native Camera Input Fallback
  el.btnNativeCam.addEventListener('click', () => el.nativeCameraInput.click());
  el.nativeCameraInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) handleFileSelected(file, 'camera');
  });

  // Drag and Drop
  ['dragenter', 'dragover'].forEach(name => {
    el.dropzone.addEventListener(name, (e) => {
      e.preventDefault();
      e.stopPropagation();
      el.dropzone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach(name => {
    el.dropzone.addEventListener(name, (e) => {
      e.preventDefault();
      e.stopPropagation();
      el.dropzone.classList.remove('dragover');
    });
  });

  el.dropzone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const file = dt.files[0];
    if (file) handleFileSelected(file, 'upload');
  });

  // In-App Camera Button
  el.btnStartCamera.addEventListener('click', () => {
    if (!state.isSecure || !state.hasGetUserMedia) {
      showToast('Live video blocked on HTTP; launching native camera');
      el.nativeCameraInput.click();
    } else {
      openCameraModal();
    }
  });

  el.btnCloseCamera.addEventListener('click', closeCameraModal);
  el.btnFlipCam.addEventListener('click', toggleCameraFacing);
  el.btnShutter.addEventListener('click', captureCameraFrame);

  // Result view buttons
  el.btnScanAnother.addEventListener('click', () => switchView('scan'));

  // History Clear
  el.btnClearHistory.addEventListener('click', async () => {
    if (confirm('Are you sure you want to clear all analysis history?')) {
      try {
        await fetch('/api/history', { method: 'DELETE' });
        showToast('History cleared');
        loadHistory();
      } catch (err) {
        showToast('Failed to clear history');
      }
    }
  });

  // Diseases Search
  el.diseaseSearchInput.addEventListener('input', (e) => {
    filterDiseases(e.target.value);
  });
}

// Camera Streaming
async function openCameraModal() {
  el.cameraModal.classList.add('active');
  await startCameraStream();
}

async function startCameraStream() {
  stopCameraStream();
  const constraints = {
    video: {
      facingMode: { ideal: state.facingMode },
      width: { ideal: 1280 },
      height: { ideal: 720 }
    },
    audio: false
  };

  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    state.activeStream = stream;
    el.cameraVideo.srcObject = stream;
    await el.cameraVideo.play();
  } catch (err) {
    console.error('Camera access error:', err);
    showToast('Camera access denied or unavailable; opening native camera');
    closeCameraModal();
    el.nativeCameraInput.click();
  }
}

function stopCameraStream() {
  if (state.activeStream) {
    state.activeStream.getTracks().forEach(track => track.stop());
    state.activeStream = null;
  }
  if (el.cameraVideo) {
    el.cameraVideo.srcObject = null;
  }
}

function closeCameraModal() {
  stopCameraStream();
  el.cameraModal.classList.remove('active');
}

function toggleCameraFacing() {
  state.facingMode = state.facingMode === 'environment' ? 'user' : 'environment';
  startCameraStream();
}

function captureCameraFrame() {
  if (!el.cameraVideo || !el.cameraVideo.videoWidth) {
    showToast('Camera not ready');
    return;
  }

  const canvas = document.createElement('canvas');
  canvas.width = el.cameraVideo.videoWidth;
  canvas.height = el.cameraVideo.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(el.cameraVideo, 0, 0, canvas.width, canvas.height);

  closeCameraModal();
  setLoading(true, 'Analyzing captured leaf...');

  canvas.toBlob((blob) => {
    if (!blob) {
      setLoading(false);
      showToast('Capture failed');
      return;
    }
    const file = new File([blob], 'camera_capture.jpg', { type: 'image/jpeg' });
    uploadAndAnalyze(file, 'camera');
  }, 'image/jpeg', 0.92);
}

// File Selection & Upload
function handleFileSelected(file, source) {
  if (!file.type.startsWith('image/')) {
    alert('Please select a valid image file (JPEG, PNG, WebP).');
    return;
  }

  if (file.size > 15 * 1024 * 1024) {
    alert('The selected image exceeds 15 MB. Please choose a smaller photo.');
    return;
  }

  uploadAndAnalyze(file, source);
}

async function uploadAndAnalyze(file, source) {
  setLoading(true, 'Inspecting leaf patterns with AI...');

  const formData = new FormData();
  formData.append('file', file);
  formData.append('source', source);

  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `Server returned ${res.status}`);
    }

    const data = await res.json();
    setLoading(false);
    displayResult(data);
  } catch (err) {
    setLoading(false);
    console.error('Analysis error:', err);
    alert('Analysis failed: ' + err.message);
  }
}

// AutoSim Handler
async function handleAutoSim() {
  setLoading(true, 'Running AutoSim on real sample leaf...');

  try {
    const res = await fetch('/api/autosim', {
      method: 'POST'
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `Server returned ${res.status}`);
    }

    const data = await res.json();
    setLoading(false);
    displayResult(data);

    // After showing result, trigger QR code modal so user can test on phone!
    setTimeout(() => {
      openQrModal();
      showToast('AutoSim finished! Scan QR with your phone to open.');
    }, 800);

  } catch (err) {
    setLoading(false);
    console.error('AutoSim error:', err);
    alert('AutoSim failed: ' + err.message);
  }
}

// Render Result Screen
function displayResult(data) {
  state.currentAnalysis = data;

  // Plant & Condition
  el.resPlantBadge.textContent = `🌱 ${data.plant}`;
  
  if (data.is_healthy) {
    el.resStatusBadge.className = 'status-badge healthy';
    el.resStatusBadge.textContent = '✓ Healthy';
  } else {
    el.resStatusBadge.className = 'status-badge disease';
    el.resStatusBadge.textContent = '⚠ Disease Detected';
  }

  el.resDiagnosisTitle.textContent = data.display_name;

  // Confidence Bar
  el.resConfidenceVal.textContent = `${data.confidence_percent}%`;
  el.resConfidenceBar.style.width = `${Math.min(100, Math.max(5, data.confidence_percent))}%`;

  // Low confidence advisory
  if (data.is_low_confidence) {
    el.resLowConfAlert.style.display = 'flex';
  } else {
    el.resLowConfAlert.style.display = 'none';
  }

  // Analyzed Image
  el.resImage.src = data.image_url;

  // Agronomic Advice
  const advice = data.advice || {};
  el.resDesc.textContent = advice.description || 'No description available.';
  el.resCause.textContent = advice.cause || 'Unknown etiology.';
  el.resTreatment.textContent = advice.treatment || 'Consult a certified local agricultural extension officer.';
  el.resPrevention.textContent = advice.prevention || 'Standard good cultural sanitation practices.';

  // Top Alternatives
  if (data.top_predictions && data.top_predictions.length > 1) {
    el.resAltPredsBox.style.display = 'block';
    el.resAltPredsList.innerHTML = data.top_predictions.slice(1, 3).map(p => `
      <div class="alt-pred-item">
        <span>${p.display_name} (${p.plant})</span>
        <span style="font-weight: 700; color: #4b5563;">${p.confidence_percent}%</span>
      </div>
    `).join('');
  } else {
    el.resAltPredsBox.style.display = 'none';
  }

  switchView('result');
}

// History Handling
async function loadHistory() {
  try {
    const res = await fetch('/api/history');
    if (!res.ok) throw new Error('Failed to fetch history');
    const items = await res.json();
    renderHistoryList(items);
  } catch (err) {
    console.error('History load error:', err);
    el.historyList.innerHTML = `<div class="empty-state"><p>Could not load history.</p></div>`;
  }
}

function renderHistoryList(items) {
  if (!items || items.length === 0) {
    el.historyEmpty.style.display = 'block';
    el.historyList.innerHTML = '';
    return;
  }

  el.historyEmpty.style.display = 'none';
  el.historyList.innerHTML = items.map(item => {
    const dateStr = item.timestamp ? new Date(item.timestamp).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : 'Recent';
    const isHealthy = item.is_healthy;
    return `
      <div class="history-card" data-id="${item.id}">
        <img class="history-thumb" src="${item.thumbnail_url || item.image_url}" alt="Leaf thumbnail" onerror="this.src='/vendor/icon.png'">
        <div class="history-info" onclick="viewHistoryDetail(${item.id})">
          <div class="history-plant-tag">${item.plant}</div>
          <div class="history-disease">${item.display_name}</div>
          <div class="history-meta">
            <span style="color: ${isHealthy ? 'var(--primary)' : 'var(--danger)'}; font-weight: 600;">
              ${isHealthy ? 'Healthy' : 'Diseased'} (${item.confidence_percent}%)
            </span>
            <span>•</span>
            <span>${dateStr}</span>
            ${item.is_simulated ? '<span class="sim-tag">AutoSim</span>' : ''}
          </div>
        </div>
        <button class="btn-delete-item" title="Delete scan" onclick="event.stopPropagation(); deleteHistoryItem(${item.id})">&times;</button>
      </div>
    `;
  }).join('');
}

async function viewHistoryDetail(id) {
  setLoading(true, 'Loading record details...');
  try {
    const res = await fetch(`/api/history/${id}`);
    if (!res.ok) throw new Error('Record not found');
    const data = await res.json();
    setLoading(false);
    displayResult(data);
  } catch (err) {
    setLoading(false);
    showToast('Could not load record details');
  }
}

async function deleteHistoryItem(id) {
  try {
    const res = await fetch(`/api/history/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Delete failed');
    showToast('Record deleted');
    const card = document.querySelector(`.history-card[data-id="${id}"]`);
    if (card) {
      card.style.opacity = '0';
      setTimeout(() => {
        card.remove();
        if (!el.historyList.children.length) {
          el.historyEmpty.style.display = 'block';
        }
      }, 200);
    }
  } catch (err) {
    showToast('Failed to delete record');
  }
}

// Diseases Reference Guide
async function loadDiseases() {
  if (state.diseasesCache.length > 0) {
    renderDiseasesCatalog(state.diseasesCache);
    return;
  }

  try {
    const res = await fetch('/api/diseases');
    if (!res.ok) throw new Error('Failed to fetch diseases');
    const data = await res.json();
    state.diseasesCache = data;
    renderDiseasesCatalog(data);
  } catch (err) {
    console.error('Diseases load error:', err);
    el.diseaseCatalogList.innerHTML = `<p style="padding: 20px; color: #666;">Could not load plant guide.</p>`;
  }
}

function renderDiseasesCatalog(items) {
  if (!items || items.length === 0) {
    el.diseaseCatalogList.innerHTML = `<p style="padding: 20px; color: #666;">No diseases match your search.</p>`;
    return;
  }

  el.diseaseCatalogList.innerHTML = items.map(d => `
    <div class="catalog-item-card">
      <div class="catalog-item-header">
        <span class="catalog-item-name">${d.display_name}</span>
        <span class="plant-badge">🌱 ${d.plant}</span>
      </div>
      <p style="font-size: 0.88rem; color: #4b5563; margin-bottom: 8px;">${d.description}</p>
      <div style="font-size: 0.82rem; color: #1b4332; background: #f0fdf4; padding: 8px 12px; border-radius: 6px;">
        <strong>Care Action:</strong> ${d.treatment}
      </div>
    </div>
  `).join('');
}

function filterDiseases(query) {
  const q = query.trim().toLowerCase();
  if (!q) {
    renderDiseasesCatalog(state.diseasesCache);
    return;
  }
  const filtered = state.diseasesCache.filter(d => 
    d.plant.toLowerCase().includes(q) ||
    d.display_name.toLowerCase().includes(q) ||
    d.description.toLowerCase().includes(q)
  );
  renderDiseasesCatalog(filtered);
}

// Loading Overlay Helper
function setLoading(active, text = 'Processing...') {
  el.loadingText.textContent = text;
  if (active) {
    el.loadingOverlay.classList.add('active');
  } else {
    el.loadingOverlay.classList.remove('active');
  }
}

// Register Service Worker
function registerServiceWorker() {
  if ('serviceWorker' in navigator && (window.location.protocol === 'https:' || window.location.hostname === 'localhost')) {
    navigator.serviceWorker.register('/sw.js')
      .then(() => console.log('Service Worker registered'))
      .catch((err) => console.log('Service Worker registration skipped:', err));
  }
}
