// Paper2Poster Frontend JavaScript

let currentJobId = null;
let statusCheckInterval = null;

// DOM elements
const uploadSection = document.getElementById('upload-section');
const progressSection = document.getElementById('progress-section');
const resultsSection = document.getElementById('results-section');
const errorSection = document.getElementById('error-section');
const uploadForm = document.getElementById('upload-form');
const progressBar = document.getElementById('progress-bar');
const progressMessage = document.getElementById('progress-message');
const posterPreview = document.getElementById('poster-preview');
const downloadImageBtn = document.getElementById('download-image');
const downloadPptxBtn = document.getElementById('download-pptx');
const newPosterBtn = document.getElementById('new-poster-btn');
const retryBtn = document.getElementById('retry-btn');
const errorMessage = document.getElementById('error-message');

// Event listeners
uploadForm.addEventListener('submit', handleUpload);
newPosterBtn.addEventListener('click', resetInterface);
retryBtn.addEventListener('click', resetInterface);

// File upload handler
async function handleUpload(event) {
    event.preventDefault();
    
    const formData = new FormData(uploadForm);
    const file = formData.get('file');
    
    // Validate file
    if (!file || file.size === 0) {
        showError('Please select a PDF file');
        return;
    }
    
    if (file.size > 50 * 1024 * 1024) { // 50MB limit
        showError('File size must be less than 50MB');
        return;
    }
    
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        showError('Please select a PDF file');
        return;
    }
    
    try {
        // Show progress section
        showSection(progressSection);
        updateProgress(0, 'Uploading file...');
        
        // Upload file
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Upload failed');
        }
        
        const data = await response.json();
        currentJobId = data.job_id;
        
        // Start status checking
        startStatusChecking();
        
    } catch (error) {
        console.error('Upload error:', error);
        showError(`Upload failed: ${error.message}`);
    }
}

// Start checking job status
function startStatusChecking() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }
    
    statusCheckInterval = setInterval(async () => {
        try {
            const response = await fetch(`/status/${currentJobId}`);
            
            if (!response.ok) {
                throw new Error('Failed to get status');
            }
            
            const status = await response.json();
            updateProgress(status.progress, status.message);
            
            if (status.status === 'completed') {
                clearInterval(statusCheckInterval);
                showResults(status);
            } else if (status.status === 'error') {
                clearInterval(statusCheckInterval);
                showError(status.message);
            }
            
        } catch (error) {
            console.error('Status check error:', error);
            clearInterval(statusCheckInterval);
            showError('Failed to check status');
        }
    }, 2000); // Check every 2 seconds
}

// Update progress bar and message
function updateProgress(progress, message) {
    progressBar.style.width = `${progress}%`;
    progressBar.setAttribute('aria-valuenow', progress);
    progressBar.textContent = `${progress}%`;
    progressMessage.innerHTML = `<strong>${message}</strong>`;
}

// Show results section
function showResults(status) {
    // Set poster preview
    if (status.poster_image) {
        posterPreview.src = status.poster_image + '?t=' + Date.now(); // Cache busting
        posterPreview.style.display = 'block';
    }
    
    // Set download links
    if (status.poster_image) {
        downloadImageBtn.href = `/download/${currentJobId}/poster`;
        downloadImageBtn.style.display = 'inline-block';
    } else {
        downloadImageBtn.style.display = 'none';
    }
    
    if (status.pptx_file) {
        downloadPptxBtn.href = `/download/${currentJobId}/pptx`;
        downloadPptxBtn.style.display = 'inline-block';
    } else {
        downloadPptxBtn.style.display = 'none';
    }
    
    showSection(resultsSection);
}

// Show error section
function showError(message) {
    errorMessage.textContent = message;
    errorSection.classList.add('shake');
    showSection(errorSection);
    
    // Remove shake animation after it completes
    setTimeout(() => {
        errorSection.classList.remove('shake');
    }, 500);
}

// Show specific section and hide others
function showSection(targetSection) {
    const sections = [uploadSection, progressSection, resultsSection, errorSection];
    
    sections.forEach(section => {
        if (section === targetSection) {
            section.style.display = 'block';
            section.classList.add('fade-in');
        } else {
            section.style.display = 'none';
            section.classList.remove('fade-in');
        }
    });
}

// Reset interface to initial state
function resetInterface() {
    // Clear intervals
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
        statusCheckInterval = null;
    }
    
    // Reset variables
    currentJobId = null;
    
    // Reset form
    uploadForm.reset();
    
    // Reset progress
    updateProgress(0, 'Initializing...');
    
    // Show upload section
    showSection(uploadSection);
}

// Download file helper
async function downloadFile(url, filename) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Download failed');
        
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
        console.error('Download error:', error);
        alert('Download failed. Please try again.');
    }
}

// File input validation
document.getElementById('pdf-file').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const fileInput = event.target;
    
    if (file) {
        // Check file type
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            fileInput.value = '';
            alert('Please select a PDF file');
            return;
        }
        
        // Check file size (50MB limit)
        if (file.size > 50 * 1024 * 1024) {
            fileInput.value = '';
            alert('File size must be less than 50MB');
            return;
        }
        
        // Update file input appearance to show file is selected
        fileInput.classList.add('is-valid');
    } else {
        fileInput.classList.remove('is-valid');
    }
});

// Form validation
function validateForm() {
    const fileInput = document.getElementById('pdf-file');
    const file = fileInput.files[0];
    
    if (!file) {
        fileInput.classList.add('is-invalid');
        return false;
    }
    
    fileInput.classList.remove('is-invalid');
    return true;
}

// Add form validation on submit
uploadForm.addEventListener('submit', function(event) {
    if (!validateForm()) {
        event.preventDefault();
        event.stopPropagation();
    }
});

// Drag and drop functionality
const fileInput = document.getElementById('pdf-file');
const uploadCard = document.querySelector('#upload-section .card-body');

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadCard.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

// Highlight drop area when item is dragged over it
['dragenter', 'dragover'].forEach(eventName => {
    uploadCard.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    uploadCard.addEventListener(eventName, unhighlight, false);
});

// Handle dropped files
uploadCard.addEventListener('drop', handleDrop, false);

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    uploadCard.classList.add('border-primary', 'bg-light');
}

function unhighlight(e) {
    uploadCard.classList.remove('border-primary', 'bg-light');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        const file = files[0];
        if (file.name.toLowerCase().endsWith('.pdf')) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change', { bubbles: true }));
        } else {
            alert('Please drop a PDF file');
        }
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Show upload section by default
    showSection(uploadSection);
    
    // Add any initialization code here
    console.log('Paper2Poster frontend initialized');
});

// Handle page refresh/close
window.addEventListener('beforeunload', function() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }
});

// Auto-hide alerts
function showAlert(message, type = 'info', duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto remove after duration
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, duration);
}

// Progress estimation based on typical processing stages
function estimateProgress(message) {
    const stages = {
        'Starting': 5,
        'Analyzing': 15,
        'Extracting': 25,
        'Processing': 40,
        'Generating layout': 60,
        'Creating content': 75,
        'Finalizing': 85,
        'Rendering': 95
    };
    
    for (const [stage, progress] of Object.entries(stages)) {
        if (message.toLowerCase().includes(stage.toLowerCase())) {
            return progress;
        }
    }
    
    return null;
}
