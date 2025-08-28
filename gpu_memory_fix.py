"""
GPU Memory optimization script for Paper2Poster
This script helps configure the environment for better GPU memory management
"""

import os
import torch

def setup_gpu_memory_optimization():
    """Set up environment variables for optimal GPU memory usage"""
    
    # Set PyTorch CUDA memory allocation configuration
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    
    # Enable CUDA launch blocking for better error reporting
    os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
    
    # Clear GPU cache if PyTorch is available
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print(f"GPU Memory available: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
        print(f"GPU Memory allocated: {torch.cuda.memory_allocated(0) / 1024**3:.2f} GB")
        print(f"GPU Memory cached: {torch.cuda.memory_reserved(0) / 1024**3:.2f} GB")
    
    print("GPU memory optimization settings applied")

def force_cpu_mode():
    """Force CPU-only mode to avoid GPU memory issues"""
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    print("Forced CPU-only mode - GPU disabled")

def check_gpu_memory():
    """Check current GPU memory usage"""
    if torch.cuda.is_available():
        device = torch.cuda.current_device()
        total_memory = torch.cuda.get_device_properties(device).total_memory
        allocated_memory = torch.cuda.memory_allocated(device)
        cached_memory = torch.cuda.memory_reserved(device)
        free_memory = total_memory - allocated_memory
        
        print(f"GPU {device} Memory Status:")
        print(f"  Total: {total_memory / 1024**3:.2f} GB")
        print(f"  Allocated: {allocated_memory / 1024**3:.2f} GB")
        print(f"  Cached: {cached_memory / 1024**3:.2f} GB")
        print(f"  Free: {free_memory / 1024**3:.2f} GB")
        
        return free_memory > 1024**3  # Return True if more than 1GB free
    else:
        print("CUDA not available")
        return False

if __name__ == "__main__":
    # Check GPU memory and decide whether to use GPU or CPU
    if check_gpu_memory():
        setup_gpu_memory_optimization()
    else:
        force_cpu_mode()
