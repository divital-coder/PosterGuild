"""
Alternative PDF parsing that avoids GPU memory issues
This module provides fallback parsing methods when the main docling converter fails
"""

import os
import PyPDF2
import fitz  # PyMuPDF
from pathlib import Path
import re
from typing import Tuple, Optional

def simple_pdf_text_extraction(pdf_path: str) -> str:
    """
    Extract text from PDF using PyPDF2 (CPU-only, no OCR)
    """
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        # Clean up the text
        text = re.sub(r'\s+', ' ', text)  # Multiple whitespace to single space
        text = re.sub(r'\n+', '\n', text)  # Multiple newlines to single newline
        
        return text.strip()
    except Exception as e:
        print(f"PyPDF2 extraction failed: {e}")
        return ""

def pymupdf_text_extraction(pdf_path: str) -> str:
    """
    Extract text from PDF using PyMuPDF (CPU-only, better text extraction)
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text() + "\n"
        
        doc.close()
        
        # Clean up the text
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        
        return text.strip()
    except Exception as e:
        print(f"PyMuPDF extraction failed: {e}")
        return ""

def fallback_pdf_parsing(pdf_path: str) -> Tuple[str, bool]:
    """
    Fallback PDF parsing that tries multiple methods
    Returns (text_content, success)
    """
    print("🔄 Using fallback PDF parsing (CPU-only)")
    
    # Try PyMuPDF first (usually better)
    text = pymupdf_text_extraction(pdf_path)
    if text and len(text) > 100:
        print("✅ PyMuPDF extraction successful")
        return text, True
    
    # Try PyPDF2 as backup
    text = simple_pdf_text_extraction(pdf_path)
    if text and len(text) > 100:
        print("✅ PyPDF2 extraction successful")
        return text, True
    
    print("❌ All fallback methods failed")
    return "", False

def is_pdf_text_based(pdf_path: str) -> bool:
    """
    Check if PDF has extractable text (not just scanned images)
    """
    try:
        # Quick test with PyMuPDF
        doc = fitz.open(pdf_path)
        text_length = 0
        
        # Check first 3 pages
        for page_num in range(min(3, len(doc))):
            page = doc.load_page(page_num)
            text_length += len(page.get_text().strip())
        
        doc.close()
        
        # If we got reasonable amount of text, it's likely text-based
        return text_length > 200
    except:
        return False

def safe_pdf_parse(pdf_path: str) -> Tuple[str, str]:
    """
    Safe PDF parsing that avoids GPU memory issues
    Returns (text_content, method_used)
    """
    pdf_path = str(pdf_path)
    
    # Check if PDF has extractable text
    if is_pdf_text_based(pdf_path):
        print("📄 PDF appears to be text-based, using simple extraction")
        text, success = fallback_pdf_parsing(pdf_path)
        if success:
            return text, "simple_extraction"
    
    print("🖼️  PDF appears to be image-based or extraction failed")
    print("⚠️  OCR would be needed but is disabled to avoid GPU memory issues")
    print("💡 Try using a text-based PDF or convert your PDF to text format")
    
    # Return minimal text with instructions
    minimal_text = f"""
    This PDF could not be processed due to GPU memory limitations.
    
    To resolve this issue:
    1. Try using a text-based PDF (not scanned images)
    2. Convert your PDF to a text-searchable format
    3. Or free up GPU memory and try again
    
    PDF Path: {pdf_path}
    """
    
    return minimal_text, "failed_gpu_memory"

# Install required packages if not available
def ensure_pdf_dependencies():
    """Ensure required PDF processing packages are available"""
    try:
        import PyPDF2
        import fitz
        return True
    except ImportError as e:
        print(f"❌ Missing PDF dependencies: {e}")
        print("📦 Please install: pip install PyPDF2 PyMuPDF")
        return False

if __name__ == "__main__":
    # Test the fallback parsing
    import sys
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        if Path(pdf_path).exists():
            text, method = safe_pdf_parse(pdf_path)
            print(f"\n📊 Results using {method}:")
            print(f"Text length: {len(text)} characters")
            print(f"First 500 characters:\n{text[:500]}...")
        else:
            print(f"❌ File not found: {pdf_path}")
    else:
        print("Usage: python cpu_pdf_parser.py <pdf_file>")
