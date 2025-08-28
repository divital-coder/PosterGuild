# Paper2Poster Web Frontend

A modern, user-friendly web interface for the Paper2Poster project that allows users to upload research papers and generate academic posters through a browser.

## 🌟 Features

- **Simple Upload Interface**: Drag & drop or click to upload PDF research papers
- **Real-time Progress Tracking**: Monitor the poster generation process with live updates
- **Multiple Output Formats**: Download both PNG images and editable PowerPoint files
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Advanced Configuration**: Customize AI models and poster dimensions
- **Professional UI**: Clean, modern interface with smooth animations

## 🚀 Quick Start

### Option 1: Using the Startup Script (Recommended)
```bash
./start_frontend.sh
```

### Option 2: Manual Start
```bash
# Install dependencies
pip install fastapi uvicorn python-multipart jinja2

# Start the server
python frontend.py
```

The web interface will be available at:
- **Local**: http://localhost:8000
- **Network**: http://0.0.0.0:8000

## 📋 Requirements

- Python 3.8 or higher
- All dependencies from the main project
- FastAPI and related web dependencies (automatically installed)

## 🎯 How to Use

1. **Open the Web Interface**: Navigate to http://localhost:8000 in your browser
2. **Upload Your Paper**: 
   - Click "Choose File" or drag & drop a PDF research paper
   - Maximum file size: 50MB
3. **Configure Settings** (Optional):
   - Select AI models (GPT-4o recommended)
   - Set poster dimensions (default: 48" x 36")
4. **Generate Poster**: Click "Generate Poster" and wait for processing
5. **Download Results**: Once complete, download the poster image or PowerPoint file

## 🔧 Configuration Options

### AI Models
- **Text Model**: Processes paper content and generates text
  - GPT-4o (Recommended)
  - GPT-4o Mini
  - GPT-3.5 Turbo
- **Vision Model**: Handles images and visual elements
  - GPT-4o (Recommended)
  - GPT-4o Mini

### Poster Dimensions
- **Width**: 24-72 inches (default: 48")
- **Height**: 18-54 inches (default: 36")
- Standard academic poster size is 48" x 36"

## 📁 Project Structure

```
Paper2Poster/
├── frontend.py           # Main FastAPI application
├── templates/
│   └── index.html       # Web interface template
├── static/
│   ├── style.css        # Custom CSS styles
│   └── script.js        # Frontend JavaScript
├── uploads/             # Temporary upload storage
├── results/             # Generated poster storage
└── start_frontend.sh    # Quick start script
```

## 🛠️ API Endpoints

- `GET /` - Main web interface
- `POST /upload` - Upload paper and start processing
- `GET /status/{job_id}` - Check processing status
- `GET /download/{job_id}/{file_type}` - Download generated files
- `GET /health` - Health check endpoint

## 🎨 Customization

### Styling
Edit `static/style.css` to customize the appearance:
- Colors and gradients
- Button styles
- Layout spacing
- Animations

### Functionality
Modify `static/script.js` to add features:
- File validation rules
- Progress tracking
- Download handling
- Error management

### Templates
Update `templates/index.html` to change:
- Page layout
- Form elements
- Content sections
- Meta information

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Kill any existing process on port 8000
   lsof -ti:8000 | xargs kill -9
   ```

2. **Upload Fails**:
   - Check file size (max 50MB)
   - Ensure file is a valid PDF
   - Verify sufficient disk space

3. **Generation Errors**:
   - Check API keys are properly configured
   - Verify the main pipeline works via command line
   - Check server logs for detailed error messages

4. **Browser Issues**:
   - Clear browser cache
   - Try incognito/private mode
   - Ensure JavaScript is enabled

### Debug Mode

Run with debug logging:
```bash
python frontend.py --log-level debug
```

## 🔒 Security Notes

- Files are temporarily stored and should be cleaned up after processing
- Consider implementing authentication for production use
- Add rate limiting for public deployments
- Validate all user inputs thoroughly

## 📈 Performance Tips

- Use SSD storage for faster file operations
- Configure adequate RAM for concurrent users
- Consider using a reverse proxy (nginx) for production
- Implement job queuing for high-load scenarios

## 🤝 Contributing

To contribute to the web frontend:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the interface thoroughly
5. Submit a pull request

## 📄 License

This project follows the same license as the main Paper2Poster project.
