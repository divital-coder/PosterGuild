"""
Modified pipeline runner that forces CPU-only operation
This script wraps the original pipeline with proper CPU-only environment setup
"""

import os
import sys
import subprocess
import torch
from pathlib import Path

def setup_cpu_environment():
    """Setup environment for CPU-only operation"""
    # Clear any GPU memory
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    # Force CPU-only mode
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    os.environ["FORCE_CPU"] = "1"
    
    # Memory optimization
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    os.environ["OMP_NUM_THREADS"] = "4"
    os.environ["OPENBLAS_NUM_THREADS"] = "4"
    os.environ["MKL_NUM_THREADS"] = "4"
    
    # Set PyTorch to CPU
    torch.set_default_device('cpu')
    
    print("🔧 CPU-only environment configured")

def run_pipeline_cpu_only(args):
    """Run the pipeline with CPU-only settings"""
    
    # Setup environment
    setup_cpu_environment()
    
    # Import and run pipeline directly to avoid subprocess issues
    try:
        # Change to project directory
        os.chdir(Path(__file__).parent)
        
        # Import the pipeline module
        sys.path.insert(0, str(Path.cwd()))
        
        # Now run the pipeline with the arguments
        from PosterAgent.new_pipeline import main as pipeline_main
        
        # Convert string arguments back to sys.argv format
        sys.argv = ['new_pipeline.py'] + args
        
        # Run the pipeline
        pipeline_main()
        
    except Exception as e:
        print(f"❌ Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    # Get arguments from command line
    args = sys.argv[1:]
    run_pipeline_cpu_only(args)
