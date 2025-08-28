#!/usr/bin/env python3
"""
Test script for Paper2Poster setup
This script checks if all requirements are met before running the frontend
"""

import os
import sys
import subprocess
from pathlib import Path

def check_api_key():
    """Check if OpenAI API key is set"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        return False
    elif api_key.startswith('sk-'):
        print("✅ OPENAI_API_KEY is set")
        return True
    else:
        print("⚠️  OPENAI_API_KEY format might be incorrect")
        return False

def check_gpu_status():
    """Check GPU status and memory"""
    try:
        import torch
        if torch.cuda.is_available():
            device_count = torch.cuda.device_count()
            current_device = torch.cuda.current_device()
            device_name = torch.cuda.get_device_name(current_device)
            total_memory = torch.cuda.get_device_properties(current_device).total_memory
            
            print(f"🎮 GPU Available: {device_name}")
            print(f"   Total Memory: {total_memory / 1024**3:.2f} GB")
            
            # Check available memory
            torch.cuda.empty_cache()
            allocated = torch.cuda.memory_allocated(current_device)
            cached = torch.cuda.memory_reserved(current_device)
            free = total_memory - allocated
            
            print(f"   Free Memory: {free / 1024**3:.2f} GB")
            
            if free < 1 * 1024**3:  # Less than 1GB free
                print("⚠️  Low GPU memory - will use CPU mode")
                return False
            else:
                print("✅ Sufficient GPU memory available")
                return True
        else:
            print("🔄 No GPU available - will use CPU mode")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed - will use CPU mode")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'jinja2',
        'torch',
        'docling'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} missing")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_file_structure():
    """Check if required files exist"""
    required_files = [
        'frontend.py',
        'templates/index.html',
        'static/style.css',
        'static/script.js',
        'PosterAgent/new_pipeline.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def main():
    print("🔍 Paper2Poster Setup Check")
    print("=" * 40)
    
    # Check all requirements
    api_key_ok = check_api_key()
    print()
    
    gpu_ok = check_gpu_status()
    print()
    
    deps_ok = check_dependencies()
    print()
    
    files_ok = check_file_structure()
    print()
    
    # Summary
    print("📊 Summary:")
    print(f"   API Key: {'✅' if api_key_ok else '❌'}")
    print(f"   GPU: {'✅' if gpu_ok else '🔄 CPU Mode'}")
    print(f"   Dependencies: {'✅' if deps_ok else '❌'}")
    print(f"   Files: {'✅' if files_ok else '❌'}")
    
    if api_key_ok and deps_ok and files_ok:
        print("\n🎉 All checks passed! You can start the frontend.")
        
        if not gpu_ok:
            print("\n💡 Note: Running in CPU mode due to GPU limitations.")
            print("   This is slower but should work without memory issues.")
        
        return True
    else:
        print("\n❌ Some issues need to be resolved before starting.")
        
        if not api_key_ok:
            print("\n🔧 To fix API key issue:")
            print("   export OPENAI_API_KEY='your-api-key-here'")
        
        if not deps_ok:
            print("\n🔧 To fix dependencies:")
            print("   pip install -r requirements.txt")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
