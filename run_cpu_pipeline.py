#!/usr/bin/env python3
"""
CPU-only pipeline wrapper for Paper2Poster
This script runs the poster generation pipeline with CPU-only settings to avoid GPU memory issues
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def setup_cpu_environment():
    """Setup environment variables for CPU-only operation"""
    
    # Disable GPU completely
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    
    # Memory optimization settings
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
    
    # CPU thread limits
    os.environ["OMP_NUM_THREADS"] = "4"
    os.environ["OPENBLAS_NUM_THREADS"] = "4"
    os.environ["MKL_NUM_THREADS"] = "4"
    
    # Force CPU flag
    os.environ["FORCE_CPU"] = "1"
    
    print("🔧 CPU-only environment configured")

def clear_gpu_cache():
    """Clear any existing GPU cache"""
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("🗑️  GPU cache cleared")
    except ImportError:
        pass

def run_with_fallback(args):
    """Run pipeline with fallback to simpler parsing if needed"""
    
    # Setup CPU environment
    setup_cpu_environment()
    clear_gpu_cache()
    
    # Try running the original pipeline first
    cmd = [
        sys.executable, "-m", "PosterAgent.new_pipeline",
        f"--poster_path={args.poster_path}",
        f"--model_name_t={args.model_name_t}",
        f"--model_name_v={args.model_name_v}",
        f"--poster_width_inches={args.poster_width_inches}",
        f"--poster_height_inches={args.poster_height_inches}"
    ]
    
    print(f"🚀 Running command: {' '.join(cmd)}")
    
    # Set up environment for subprocess
    env = os.environ.copy()
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            print("✅ Pipeline completed successfully")
            print(result.stdout)
            return True
        else:
            print("❌ Pipeline failed with error:")
            print(result.stderr)
            
            # Check if it's a GPU memory error
            if "CUDA out of memory" in result.stderr or "OutOfMemoryError" in result.stderr:
                print("\n🔄 GPU memory error detected, trying alternative approach...")
                return try_alternative_parsing(args)
            else:
                return False
                
    except Exception as e:
        print(f"❌ Failed to run pipeline: {e}")
        return False

def try_alternative_parsing(args):
    """Try alternative PDF parsing approach"""
    try:
        from cpu_pdf_parser import safe_pdf_parse, ensure_pdf_dependencies
        
        print("🔄 Attempting CPU-only PDF parsing...")
        
        if not ensure_pdf_dependencies():
            print("❌ Missing PDF parsing dependencies")
            return False
        
        # Parse PDF with CPU-only methods
        text_content, method = safe_pdf_parse(args.poster_path)
        
        if len(text_content) < 500:
            print("❌ Insufficient text content extracted")
            return False
        
        print(f"✅ PDF parsed successfully using {method}")
        print(f"📄 Text length: {len(text_content)} characters")
        
        # For now, just save the extracted text
        # In a full implementation, you'd want to generate a poster from this text
        output_dir = Path("<4o_4o>_generated_posters/dataset") / Path(args.poster_path).stem
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save extracted text
        with open(output_dir / "extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(text_content)
        
        # Create a simple placeholder poster message
        placeholder_content = f"""
        PDF Processed Successfully (CPU Mode)
        
        ✅ PDF: {Path(args.poster_path).name}
        📄 Text Length: {len(text_content)} characters
        🔧 Method: {method}
        
        Note: This is a simplified processing mode due to GPU memory constraints.
        The full poster generation pipeline was unable to complete.
        
        Text content has been extracted and saved to: {output_dir / "extracted_text.txt"}
        """
        
        # Create a simple text-based poster info
        with open(output_dir / "poster_info.txt", "w") as f:
            f.write(placeholder_content)
        
        print(f"📁 Results saved to: {output_dir}")
        print("⚠️  Note: This is a simplified result due to GPU memory limitations")
        
        return True
        
    except Exception as e:
        print(f"❌ Alternative parsing failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="CPU-only Paper2Poster pipeline")
    parser.add_argument("--poster_path", required=True, help="Path to the PDF file")
    parser.add_argument("--model_name_t", default="4o", help="Text model name")
    parser.add_argument("--model_name_v", default="4o", help="Vision model name")
    parser.add_argument("--poster_width_inches", type=int, default=48, help="Poster width")
    parser.add_argument("--poster_height_inches", type=int, default=36, help="Poster height")
    
    args = parser.parse_args()
    
    print("🎯 Paper2Poster CPU-Only Pipeline")
    print("=" * 40)
    print(f"📄 PDF: {args.poster_path}")
    print(f"🤖 Text Model: {args.model_name_t}")
    print(f"👁️  Vision Model: {args.model_name_v}")
    print(f"📏 Size: {args.poster_width_inches}\" x {args.poster_height_inches}\"")
    print()
    
    success = run_with_fallback(args)
    
    if success:
        print("\n🎉 Process completed!")
        sys.exit(0)
    else:
        print("\n❌ Process failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
