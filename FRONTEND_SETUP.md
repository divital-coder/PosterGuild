# Paper2Poster Web Frontend Setup

## 🎉 Frontend Successfully Established!

Your Paper2Poster project now has a complete web interface that allows users to upload PDF files and generate academic posters through a browser.

## ✅ What's Working

### 1. Web Interface
- **URL**: http://localhost:8000
- **Features**: 
  - Drag & drop PDF upload
  - Real-time progress tracking
  - Download generated posters
  - Responsive design with modern UI

### 2. Fixed Issues
- **File Naming Bug**: ✅ RESOLVED
  - Each uploaded file now generates in its own directory
  - No more conflicts between different uploads
  - Example: `bhavya_resume.pdf` → `<4o_4o>_generated_posters/dataset/bhavya_resume/`

- **GPU Memory Issues**: ✅ RESOLVED
  - CPU-only processing pipeline implemented
  - No more "CUDA out of memory" errors
  - Uses PyMuPDF/PyPDF2 for PDF parsing instead of GPU-heavy docling

- **API Key Environment**: ✅ RESOLVED
  - OpenAI API key properly passed to subprocess calls
  - Web interface can successfully run background poster generation

## 🚀 How to Use

### Start the Server
```bash
source /home/dorachan/Desktop/.venv/bin/activate
cd /home/dorachan/Desktop/Paper2Poster
python frontend.py
```

### Access the Interface
1. Open browser to http://localhost:8000
2. Upload a PDF file (research paper or CV)
3. Select model options (default: 4o for both text and vision)
4. Set poster size (default: 48" x 36")
5. Click "Generate Poster"
6. Wait for processing (real-time progress shown)
7. Download the generated poster PNG and PowerPoint files

## 📁 File Structure

```
Paper2Poster/
├── frontend.py                 # Main FastAPI web server
├── run_cpu_pipeline.py         # CPU-only wrapper script
├── templates/
│   └── index.html             # Web interface
├── static/
│   ├── style.css              # Styling
│   └── script.js              # Frontend JavaScript
├── uploads/                   # Temporary upload storage
└── <4o_4o>_generated_posters/
    └── dataset/
        ├── my-awesome-paper/   # First test poster
        └── bhavya_resume/      # Second test poster
```

## 🔧 Technical Details

### Backend (FastAPI)
- File upload handling with unique UUIDs
- Background task processing
- Real-time status tracking via WebSocket-like polling
- CPU-only PDF processing to avoid GPU constraints

### Frontend (Bootstrap + JavaScript)
- Modern gradient design with animations
- Mobile-responsive layout
- Drag & drop file upload
- Progress visualization
- Error handling and validation

### Key Fixes Applied
1. **PosterAgent/new_pipeline.py**: Fixed directory naming logic to use actual filename instead of hardcoded paths
2. **run_cpu_pipeline.py**: Created CPU-only processing wrapper
3. **frontend.py**: Proper environment variable handling for subprocess calls

## 🎯 Success Metrics

- ✅ Multiple file uploads work independently
- ✅ No GPU memory conflicts
- ✅ Professional web interface
- ✅ Real-time progress feedback
- ✅ Download functionality for both PNG and PPTX files
- ✅ Proper error handling and logging

Your Paper2Poster frontend is now fully operational! 🎉
