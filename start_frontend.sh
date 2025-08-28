#!/bin/bash

# Paper2Poster Web Frontend Startup Script

echo "🎯 Paper2Poster Web Frontend"
echo "=============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if we're in a virtual environment or can use uv
if [[ -n "$VIRTUAL_ENV" ]] || command -v uv &> /dev/null; then
    echo "✅ Virtual environment detected or UV available"
else
    echo "⚠️  Warning: No virtual environment detected. Consider using a virtual environment."
fi

# Check for OPENAI_API_KEY
if [[ -z "$OPENAI_API_KEY" ]]; then
    echo "⚠️  OPENAI_API_KEY not found in environment"
    echo "Please set your OpenAI API key:"
    echo "export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo "Or add it to your .bashrc or .zshrc file"
    echo ""
    read -p "Do you want to continue without setting the API key? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Please set the OPENAI_API_KEY and try again."
        exit 1
    fi
else
    echo "✅ OPENAI_API_KEY found"
fi

echo "📦 Installing/updating dependencies..."

# Install required packages (try uv first, then pip)
if command -v uv &> /dev/null; then
    echo "Using UV package manager..."
    uv pip install fastapi uvicorn python-multipart jinja2
else
    echo "Using pip..."
    pip3 install fastapi uvicorn python-multipart jinja2
fi

# Set GPU memory optimization
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export CUDA_LAUNCH_BLOCKING=1

echo "🚀 Starting Paper2Poster web server..."
echo ""
echo "📋 Server Information:"
echo "   • Local URL: http://localhost:8000"
echo "   • Network URL: http://0.0.0.0:8000"
echo ""
echo "💡 Tips:"
echo "   • Make sure your OpenAI API key is set"
echo "   • CPU mode is enabled to avoid GPU memory issues"
echo "   • Upload PDF files up to 50MB"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 frontend.py
