"""
CPU-optimized document parsing for Paper2Poster
This module provides a fallback parsing method that uses CPU instead of GPU
"""

import os
import torch
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

def create_cpu_optimized_converter():
    """Create a document converter optimized for CPU usage and low memory"""
    
    # Force CPU usage
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    
    # Set PyTorch to use CPU only
    torch.set_default_device('cpu')
    
    # Configure pipeline for minimal memory usage
    pipeline_options = PdfPipelineOptions()
    pipeline_options.images_scale = 2.0  # Reduced from 5.0 to save memory
    pipeline_options.generate_page_images = True
    pipeline_options.generate_picture_images = True
    
    # Create converter with CPU-optimized settings
    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    
    return doc_converter

def create_minimal_converter():
    """Create a minimal document converter that avoids heavy models"""
    
    # Disable GPU completely
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    
    # Minimal pipeline options
    pipeline_options = PdfPipelineOptions()
    pipeline_options.images_scale = 1.0  # Minimal scaling
    pipeline_options.generate_page_images = False  # Disable image generation
    pipeline_options.generate_picture_images = False  # Disable picture generation
    
    # Use CPU-only converter
    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    
    return doc_converter
