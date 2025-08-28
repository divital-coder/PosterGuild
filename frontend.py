#!/usr/bin/env python3
"""
Paper2Poster Web Frontend
A FastAPI-based web application for converting research papers to posters.
"""

import os
import shutil
import tempfile
import subprocess
import logging
import asyncio
import threading
from pathlib import Path
from typing import Optional
import uuid
import json

from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Paper2Poster", description="Convert research papers to academic posters")

# Create necessary directories
UPLOAD_DIR = Path("uploads")
RESULTS_DIR = Path("results")
STATIC_DIR = Path("static")
TEMPLATES_DIR = Path("templates")

for directory in [UPLOAD_DIR, RESULTS_DIR, STATIC_DIR, TEMPLATES_DIR]:
    directory.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/results", StaticFiles(directory=RESULTS_DIR), name="results")

# Templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Store job status
job_status = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main upload page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_paper(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    model_name_t: str = Form(default="4o"),
    model_name_v: str = Form(default="4o"),
    poster_width: int = Form(default=48),
    poster_height: int = Form(default=36)
):
    """
    Upload a PDF paper and start the poster generation process.
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    try:
        # Create temporary directory for this job
        job_dir = UPLOAD_DIR / job_id
        job_dir.mkdir(exist_ok=True)
        
        # Save uploaded file
        pdf_path = job_dir / file.filename
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Initialize job status
        job_status[job_id] = {
            "status": "processing",
            "filename": file.filename,
            "progress": 0,
            "message": "Starting poster generation...",
            "poster_image": None,
            "pptx_file": None
        }
        
        # Start poster generation in background
        background_tasks.add_task(
            generate_poster_sync, 
            job_id, pdf_path, model_name_t, model_name_v, poster_width, poster_height
        )
        
        return JSONResponse({
            "job_id": job_id,
            "message": "File uploaded successfully. Poster generation started."
        })
        
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

def generate_poster_sync(job_id: str, pdf_path: Path, model_name_t: str, model_name_v: str, poster_width: int, poster_height: int):
    """
    Generate poster synchronously (called as background task).
    """
    try:
        # Update status
        job_status[job_id]["progress"] = 10
        job_status[job_id]["message"] = "Analyzing paper structure..."
        
        # Set up environment variables for better GPU memory management
        env = os.environ.copy()
        
        # Ensure OPENAI_API_KEY is available
        if "OPENAI_API_KEY" not in env:
            # Try to get from the current environment
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                env["OPENAI_API_KEY"] = api_key
            else:
                raise Exception("OPENAI_API_KEY not found in environment")
        
        # GPU memory optimization
        env["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
        env["CUDA_LAUNCH_BLOCKING"] = "1"
        
        # Force CPU usage for OCR to avoid GPU memory issues
        env["CUDA_VISIBLE_DEVICES"] = ""  # This forces CPU usage
        
        # Set additional memory optimization flags
        env["OMP_NUM_THREADS"] = "4"  # Limit CPU threads
        env["OPENBLAS_NUM_THREADS"] = "4"
        env["MKL_NUM_THREADS"] = "4"
        
        # Prepare command using CPU-only wrapper
        cmd = [
            "python", "run_cpu_pipeline.py",
            f"--poster_path={pdf_path}",
            f"--model_name_t={model_name_t}",
            f"--model_name_v={model_name_v}",
            f"--poster_width_inches={poster_width}",
            f"--poster_height_inches={poster_height}"
        ]
        
        job_status[job_id]["progress"] = 30
        job_status[job_id]["message"] = "Generating poster layout..."
        
        # Run the poster generation with environment variables
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
            env=env  # Pass the modified environment
        )
        
        if process.returncode != 0:
            job_status[job_id]["status"] = "error"
            job_status[job_id]["message"] = f"Poster generation failed: {process.stderr}"
            logger.error(f"Poster generation failed for job {job_id}: {process.stderr}")
            return
        
        job_status[job_id]["progress"] = 80
        job_status[job_id]["message"] = "Finalizing poster..."
        
        # Find generated files - use the actual paper name from the uploaded file
        paper_name = pdf_path.stem
        generated_dir = Path(f"<4o_4o>_generated_posters/dataset/{paper_name}")
        
        if not generated_dir.exists():
            # Try alternative naming - look for directories modified recently
            base_dir = Path("<4o_4o>_generated_posters/dataset")
            if base_dir.exists():
                dirs = [d for d in base_dir.iterdir() if d.is_dir()]
                if dirs:
                    # Sort by modification time (most recent first) instead of alphabetically
                    dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                    generated_dir = dirs[0]  # Get the most recently modified one
                    logger.info(f"Using most recently modified directory: {generated_dir}")
        
        if generated_dir and generated_dir.exists():
            logger.info(f"Found generated directory: {generated_dir}")
            # Copy results to results directory
            result_dir = RESULTS_DIR / job_id
            result_dir.mkdir(exist_ok=True)
            
            poster_image = generated_dir / "poster.png"
            # Find any .pptx file in the directory
            pptx_files = list(generated_dir.glob("*.pptx"))
            
            if poster_image.exists():
                shutil.copy2(poster_image, result_dir / "poster.png")
                job_status[job_id]["poster_image"] = f"/results/{job_id}/poster.png"
                logger.info(f"Copied poster image from {poster_image}")
            
            if pptx_files:
                pptx_file = pptx_files[0]
                shutil.copy2(pptx_file, result_dir / pptx_file.name)
                job_status[job_id]["pptx_file"] = f"/results/{job_id}/{pptx_file.name}"
                logger.info(f"Copied PowerPoint file from {pptx_file}")
            
            job_status[job_id]["status"] = "completed"
            job_status[job_id]["progress"] = 100
            job_status[job_id]["message"] = "Poster generated successfully!"
        else:
            job_status[job_id]["status"] = "error"
            job_status[job_id]["message"] = f"Generated files not found for {paper_name}"
            logger.error(f"Generated directory not found: {generated_dir}")
            
    except Exception as e:
        job_status[job_id]["status"] = "error"
        job_status[job_id]["message"] = f"Error: {str(e)}"
        logger.error(f"Error generating poster for job {job_id}: {str(e)}")

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """Get the status of a poster generation job."""
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job_status[job_id]

@app.get("/download/{job_id}/{file_type}")
async def download_file(job_id: str, file_type: str):
    """Download generated files (poster image or PowerPoint)."""
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_info = job_status[job_id]
    
    if file_type == "poster" and job_info.get("poster_image"):
        file_path = RESULTS_DIR / job_id / "poster.png"
        if file_path.exists():
            return FileResponse(
                path=file_path,
                filename=f"poster_{job_id}.png",
                media_type="image/png"
            )
    
    elif file_type == "pptx" and job_info.get("pptx_file"):
        pptx_files = list((RESULTS_DIR / job_id).glob("*.pptx"))
        if pptx_files:
            file_path = pptx_files[0]
            return FileResponse(
                path=file_path,
                filename=file_path.name,
                media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
    
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Paper2Poster"}

if __name__ == "__main__":
    uvicorn.run(
        "frontend:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
