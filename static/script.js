// Emotion configuration
const EMOTIONS = {
    happy: { emoji: '😊', color: '#fbbf24', label: 'Happy' },
    sad: { emoji: '😢', color: '#60a5fa', label: 'Sad' },
    angry: { emoji: '😠', color: '#ef4444', label: 'Angry' },
    fear: { emoji: '😨', color: '#a78bfa', label: 'Fear' },
    surprise: { emoji: '😲', color: '#f97316', label: 'Surprise' },
    neutral: { emoji: '😐', color: '#9ca3af', label: 'Neutral' },
    disgust: { emoji: '🤢', color: '#84cc16', label: 'Disgust' },
    confused: { emoji: '😕', color: '#f59e0b', label: 'Confused' },
    tired: { emoji: '😫', color: '#6b7280', label: 'Tired' },
    excited: { emoji: '🤩', color: '#ec4899', label: 'Excited' },
    bored: { emoji: '😑', color: '#64748b', label: 'Bored' },
    anxious: { emoji: '😰', color: '#8b5cf6', label: 'Anxious' },
    calm: { emoji: '😌', color: '#10b981', label: 'Calm' },
    frustrated: { emoji: '😤', color: '#dc2626', label: 'Frustrated' },
    content: { emoji: '😊', color: '#059669', label: 'Content' },
    worried: { emoji: '😟', color: '#7c3aed', label: 'Worried' }
};

// DOM Elements - Text Mode
const textInput = document.getElementById('textInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const charCount = document.getElementById('charCount');

// DOM Elements - Face Mode
const videoElement = document.getElementById('videoElement');
const canvasElement = document.getElementById('canvasElement');
const cameraOverlay = document.getElementById('cameraOverlay');
const startCameraBtn = document.getElementById('startCameraBtn');
const captureBtn = document.getElementById('captureBtn');
const stopCameraBtn = document.getElementById('stopCameraBtn');

// DOM Elements - Common
const resultsSection = document.getElementById('resultsSection');
const loadingOverlay = document.getElementById('loadingOverlay');
const toast = document.getElementById('toast');

// State
let analysisCount = 0;
let currentMode = 'text';
let cameraStream = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎭 AI Emotion Detection App Initialized');
    
    // Verify all DOM elements are loaded
    console.log('Checking DOM elements...');
    console.log('- videoElement:', videoElement ? '✅' : '❌');
    console.log('- canvasElement:', canvasElement ? '✅' : '❌');
    console.log('- cameraOverlay:', cameraOverlay ? '✅' : '❌');
    console.log('- startCameraBtn:', startCameraBtn ? '✅' : '❌');
    console.log('- captureBtn:', captureBtn ? '✅' : '❌');
    console.log('- stopCameraBtn:', stopCameraBtn ? '✅' : '❌');
    
    // Load initial data
    loadHistory();
    loadStats();
    
    // Event listeners - Mode switching
    document.querySelectorAll('.mode-tab').forEach(tab => {
        tab.addEventListener('click', () => switchMode(tab.dataset.mode));
    });
    
    // Event listeners - Text mode
    textInput.addEventListener('input', updateCharCount);
    analyzeBtn.addEventListener('click', analyzeEmotion);
    textInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            analyzeEmotion();
        }
    });
    
    // Event listeners - Face mode
    if (startCameraBtn) {
        startCameraBtn.addEventListener('click', () => {
            console.log('🔘 Start Camera button clicked');
            startCamera();
        });
    } else {
        console.error('❌ Start Camera button not found!');
    }
    
    if (captureBtn) {
        captureBtn.addEventListener('click', () => {
            console.log('🔘 Capture button clicked');
            captureAndAnalyze();
        });
    }
    
    if (stopCameraBtn) {
        stopCameraBtn.addEventListener('click', () => {
            console.log('🔘 Stop Camera button clicked');
            stopCamera();
        });
    }
    
    // Set initial mode to text
    const textModeSection = document.getElementById('textMode');
    if (textModeSection) {
        textModeSection.style.display = 'block';
        console.log('✅ Text mode set as default');
    }
    
    console.log('✅ Event listeners attached successfully');
    console.log('💡 Click "Facial Expression" tab to test camera');
});

// Update character count
function updateCharCount() {
    const length = textInput.value.length;
    charCount.textContent = `${length} / 5000 characters`;
    
    if (length > 4500) {
        charCount.style.color = '#ef4444';
    } else if (length > 4000) {
        charCount.style.color = '#f59e0b';
    } else {
        charCount.style.color = '#94a3b8';
    }
}

// Show/hide loading overlay
function showLoading(show = true) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
}

// Show toast notification
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Analyze emotion
async function analyzeEmotion() {
    const text = textInput.value.trim();
    
    // Validation
    if (!text) {
        showToast('Please enter some text to analyze', 'error');
        textInput.focus();
        return;
    }
    
    if (text.length > 5000) {
        showToast('Text is too long. Maximum 5000 characters allowed.', 'error');
        return;
    }
    
    // Disable button and show loading
    analyzeBtn.disabled = true;
    showLoading(true);
    
    try {
        const response = await fetch('/api/detect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        
        if (!response.ok || !data.success) {
            throw new Error(data.message || 'Failed to analyze emotion');
        }
        
        // Display results
        displayResults(data);
        
        // Update stats and history immediately
        analysisCount++;
        await loadHistory();
        await loadStats();
        
        console.log('[INFO] Text analysis complete - History and stats refreshed');
        
        // Show success message
        showToast('Emotion analyzed successfully!', 'success');
        
    } catch (error) {
        console.error('Error:', error);
        showToast(error.message || 'Failed to analyze emotion. Please try again.', 'error');
    } finally {
        analyzeBtn.disabled = false;
        showLoading(false);
    }
}

// Display analysis results
function displayResults(data) {
    const { emotion, confidence, all_emotions, sentiment } = data;
    
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Update main emotion display
    const emotionIcon = document.getElementById('emotionIcon');
    const emotionName = document.getElementById('emotionName');
    const confidenceFill = document.getElementById('confidenceFill');
    const confidenceText = document.getElementById('confidenceText');
    
    emotionIcon.textContent = EMOTIONS[emotion].emoji;
    emotionName.textContent = emotion.charAt(0).toUpperCase() + emotion.slice(1);
    emotionName.className = `emotion-name emotion-${emotion}`;
    
    const confidencePercent = Math.round(confidence * 100);
    confidenceFill.style.width = `${confidencePercent}%`;
    confidenceFill.style.backgroundColor = EMOTIONS[emotion].color;
    confidenceText.textContent = `Confidence: ${confidencePercent}%`;
    
    // Update emotions breakdown
    displayEmotionsChart(all_emotions);
    
    // Update sentiment analysis (only for text mode)
    const sentimentSection = document.querySelector('.sentiment-info');
    const polarityValue = document.getElementById('polarityValue');
    const subjectivityValue = document.getElementById('subjectivityValue');
    
    if (sentiment && sentiment.polarity !== undefined && sentiment.subjectivity !== undefined) {
        // Show sentiment section for text analysis
        if (sentimentSection) sentimentSection.style.display = 'block';
        
        if (polarityValue) {
            polarityValue.textContent = sentiment.polarity.toFixed(2);
            polarityValue.style.color = sentiment.polarity > 0 ? '#10b981' : sentiment.polarity < 0 ? '#ef4444' : '#9ca3af';
        }
        
        if (subjectivityValue) {
            subjectivityValue.textContent = sentiment.subjectivity.toFixed(2);
            subjectivityValue.style.color = sentiment.subjectivity > 0.5 ? '#8b5cf6' : '#3b82f6';
        }
    } else {
        // Hide sentiment section for facial detection
        if (sentimentSection) sentimentSection.style.display = 'none';
    }
}

// Display emotions breakdown chart
function displayEmotionsChart(emotions) {
    const emotionsChart = document.getElementById('emotionsChart');
    emotionsChart.innerHTML = '';
    
    // Sort emotions by value
    const sortedEmotions = Object.entries(emotions)
        .sort(([, a], [, b]) => b - a);
    
    sortedEmotions.forEach(([emotion, value]) => {
        const percent = Math.round(value * 100);
        
        const barDiv = document.createElement('div');
        barDiv.className = 'emotion-bar';
        
        barDiv.innerHTML = `
            <div class="emotion-label">
                <span class="emotion-emoji">${EMOTIONS[emotion].emoji}</span>
                <span>${emotion.charAt(0).toUpperCase() + emotion.slice(1)}</span>
            </div>
            <div class="emotion-progress">
                <div class="emotion-progress-fill" style="width: ${percent}%; background-color: ${EMOTIONS[emotion].color}">
                    ${percent > 10 ? percent + '%' : ''}
                </div>
            </div>
            <div class="emotion-value">${percent}%</div>
        `;
        
        emotionsChart.appendChild(barDiv);
    });
}

// Load history
async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        if (!response.ok) {
            console.warn('History API returned non-OK status:', response.status);
            return;
        }
        const data = await response.json();
        
        if (data.success && data.history && data.history.length > 0) {
            displayHistory(data.history);
        }
    } catch (error) {
        console.warn('Could not load history (this is normal on first load):', error.message);
    }
}

// Display history
function displayHistory(history) {
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = '';
    
    // Reverse to show newest first
    const reversedHistory = [...history].reverse();
    
    reversedHistory.forEach(item => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.style.borderLeftColor = EMOTIONS[item.emotion].color;
        
        const timestamp = new Date(item.timestamp).toLocaleString();
        const confidencePercent = Math.round(item.confidence * 100);
        
        historyItem.innerHTML = `
            <div class="history-header">
                <div class="history-emotion">
                    ${EMOTIONS[item.emotion].emoji} ${item.emotion.charAt(0).toUpperCase() + item.emotion.slice(1)}
                </div>
                <div class="history-confidence">${confidencePercent}%</div>
            </div>
            <div class="history-text">"${item.text}"</div>
            <div class="history-time">${timestamp}</div>
        `;
        
        historyList.appendChild(historyItem);
    });
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        if (!response.ok) {
            console.warn('Stats API returned non-OK status:', response.status);
            return;
        }
        const data = await response.json();
        
        if (data.success) {
            displayStats(data.stats);
        }
    } catch (error) {
        console.warn('Could not load stats (this is normal on first load):', error.message);
    }
}

// Display statistics
function displayStats(stats) {
    const statsGrid = document.getElementById('statsGrid');
    statsGrid.innerHTML = '';
    
    // Total detections
    const totalDiv = document.createElement('div');
    totalDiv.className = 'stat-item';
    totalDiv.innerHTML = `
        <div class="stat-value" id="totalDetections">${stats.total_detections}</div>
        <div class="stat-label">Total Analyses</div>
    `;
    statsGrid.appendChild(totalDiv);
    
    // Emotion counts
    if (stats.emotion_counts && Object.keys(stats.emotion_counts).length > 0) {
        const sortedEmotions = Object.entries(stats.emotion_counts)
            .sort(([, a], [, b]) => b - a);
        
        sortedEmotions.forEach(([emotion, count]) => {
            const statDiv = document.createElement('div');
            statDiv.className = 'stat-item';
            statDiv.innerHTML = `
                <div class="stat-value" style="color: ${EMOTIONS[emotion].color}">
                    ${EMOTIONS[emotion].emoji} ${count}
                </div>
                <div class="stat-label">${emotion.charAt(0).toUpperCase() + emotion.slice(1)}</div>
            `;
            statsGrid.appendChild(statDiv);
        });
    }
}

// Example texts for quick testing
const exampleTexts = [
    "I am so happy and excited about this amazing opportunity!",
    "This is terrible and makes me really angry and frustrated.",
    "I'm feeling sad and lonely today, missing my friends.",
    "That was such a shocking and unexpected surprise!",
    "I'm worried and afraid about what might happen next.",
    "Everything is just okay, nothing special happening."
];

// Add example text button functionality (optional)
function loadExampleText() {
    const randomText = exampleTexts[Math.floor(Math.random() * exampleTexts.length)];
    textInput.value = randomText;
    updateCharCount();
    textInput.focus();
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to focus input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        textInput.focus();
    }
    
    // Escape to clear input
    if (e.key === 'Escape' && document.activeElement === textInput) {
        textInput.value = '';
        updateCharCount();
    }
});

// Auto-refresh stats every 30 seconds
setInterval(() => {
    loadStats();
}, 30000);

// ============================================
// MODE SWITCHING
// ============================================

function switchMode(mode) {
    if (mode === 'speech') return; // Not implemented yet
    
    console.log(`🔄 Switching to ${mode} mode...`);
    currentMode = mode;
    
    // Update tab active states
    document.querySelectorAll('.mode-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.mode === mode);
    });
    
    // Get mode sections
    const textModeSection = document.getElementById('textMode');
    const faceModeSection = document.getElementById('faceMode');
    
    console.log('textMode element:', textModeSection);
    console.log('faceMode element:', faceModeSection);
    
    // Update content visibility using display property
    if (mode === 'text') {
        if (textModeSection) {
            textModeSection.style.display = 'block';
            textModeSection.classList.add('active');
        }
        if (faceModeSection) {
            faceModeSection.style.display = 'none';
            faceModeSection.classList.remove('active');
        }
    } else if (mode === 'face') {
        if (textModeSection) {
            textModeSection.style.display = 'none';
            textModeSection.classList.remove('active');
        }
        if (faceModeSection) {
            faceModeSection.style.display = 'block';
            faceModeSection.classList.add('active');
        }
        console.log('✅ Face mode section should now be visible');
    }
    
    // Stop camera if switching away from face mode
    if (mode !== 'face' && cameraStream) {
        stopCamera();
    }
    
    // Hide results when switching modes
    resultsSection.style.display = 'none';
    
    console.log(`✅ Switched to ${mode} mode`);
}

// ============================================
// FACIAL EXPRESSION DETECTION
// ============================================

async function startCamera() {
    try {
        console.log('🎥 Requesting camera access...');
        
        // Check if getUserMedia is supported
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            throw new Error('Camera API not supported in this browser');
        }
        
        // Request camera access
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: 'user'
            }
        });
        
        console.log('✅ Camera access granted');
        
        // Set video source
        videoElement.srcObject = cameraStream;
        
        // Wait for video to be ready
        await new Promise((resolve) => {
            videoElement.onloadedmetadata = () => {
                videoElement.play();
                resolve();
            };
        });
        
        // Hide overlay and show controls
        cameraOverlay.style.display = 'none';
        startCameraBtn.style.display = 'none';
        captureBtn.style.display = 'inline-flex';
        stopCameraBtn.style.display = 'inline-flex';
        
        showToast('Camera started successfully!', 'success');
        console.log('📷 Camera started and ready');
        
    } catch (error) {
        console.error('Camera error:', error);
        let errorMsg = 'Failed to access camera. ';
        
        if (error.name === 'NotAllowedError') {
            errorMsg += 'Please allow camera permissions.';
        } else if (error.name === 'NotFoundError') {
            errorMsg += 'No camera found on this device.';
        } else if (error.name === 'NotReadableError') {
            errorMsg += 'Camera is already in use by another application.';
        } else {
            errorMsg += error.message || 'Please check your camera.';
        }
        
        showToast(errorMsg, 'error');
    }
}

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
        videoElement.srcObject = null;
        
        // Show overlay and reset controls
        cameraOverlay.style.display = 'flex';
        startCameraBtn.style.display = 'inline-flex';
        captureBtn.style.display = 'none';
        stopCameraBtn.style.display = 'none';
        
        console.log('📷 Camera stopped');
    }
}

async function captureAndAnalyze() {
    if (!cameraStream) {
        showToast('Camera is not active. Please start the camera first.', 'error');
        return;
    }
    
    try {
        console.log('📸 Capturing image...');
        
        // Check if video is ready
        if (videoElement.videoWidth === 0 || videoElement.videoHeight === 0) {
            throw new Error('Video not ready. Please wait a moment and try again.');
        }
        
        // Capture frame from video
        const context = canvasElement.getContext('2d');
        canvasElement.width = videoElement.videoWidth;
        canvasElement.height = videoElement.videoHeight;
        context.drawImage(videoElement, 0, 0);
        
        // Convert to base64
        const imageData = canvasElement.toDataURL('image/jpeg', 0.8);
        console.log('✅ Image captured, sending to API...');
        
        // Show loading
        showLoading(true);
        captureBtn.disabled = true;
        
        // Send to API
        console.log('[API] Sending request to /api/detect-face...');
        const response = await fetch('/api/detect-face', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });
        
        console.log('[API] Response status:', response.status, response.statusText);
        
        const data = await response.json();
        console.log('[API] Response data:', data);
        
        if (!response.ok) {
            const errorMsg = data.message || data.error || 'Failed to detect emotion';
            console.error('[API] Error response:', errorMsg);
            throw new Error(errorMsg);
        }
        
        if (!data.success) {
            console.error('[API] Detection failed:', data);
            throw new Error(data.message || data.error || 'Detection failed');
        }
        
        // Display results
        displayResults(data);
        
        // Update stats and history immediately
        analysisCount++;
        await loadHistory();
        await loadStats();
        
        console.log('[INFO] Facial analysis complete - History and stats refreshed');
        
        // Show success message
        const facesMsg = data.faces_detected > 1 ? `${data.faces_detected} faces` : '1 face';
        showToast(`Emotion detected from ${facesMsg}!`, 'success');
        console.log('✅ Facial emotion detection complete');
        
    } catch (error) {
        console.error('[ERROR] Capture error:', error);
        console.error('[ERROR] Error type:', typeof error);
        console.error('[ERROR] Error name:', error?.name);
        console.error('[ERROR] Error message:', error?.message);
        console.error('[ERROR] Error stack:', error?.stack);
        
        let errorMessage = 'Failed to analyze facial expression. Please try again.';
        
        if (error && error.message) {
            errorMessage = error.message;
        } else if (typeof error === 'string') {
            errorMessage = error;
        }
        
        showToast(errorMessage, 'error');
    } finally {
        captureBtn.disabled = false;
        showLoading(false);
    }
}

console.log('🎭 AI Emotion Detection App Loaded Successfully!');
console.log('💡 Tip: Press Ctrl+Enter to analyze text quickly');
console.log('📷 Facial expression detection available!');
