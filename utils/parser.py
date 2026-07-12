"""
Resume Parser Module

This module provides utility functions for extracting text and structured
information from uploaded resume files (PDF).
"""
import fitz  # PyMuPDF
from typing import Optional

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from a given PDF file bytes using PyMuPDF.

    Args:
        file_bytes (bytes): The raw bytes of the uploaded PDF file.

    Returns:
        str: The extracted text as a string.

    Raises:
        ValueError: If the provided file bytes are empty, the PDF contains no pages, 
                    or no readable text could be extracted (e.g., image-only PDF).
        Exception: For any corrupted file, unsupported format, or read failure during parsing.
    """
    if not file_bytes:
        raise ValueError("The provided PDF file is empty.")

    try:
        # Open the PDF file from memory bytes
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        raise Exception(f"Failed to read the PDF file. It may be corrupted or unsupported. Details: {str(e)}")
        
    if pdf_document.page_count == 0:
        pdf_document.close()
        raise ValueError("The PDF document contains no pages.")

    extracted_text = []
    
    # Iterate through all pages and extract text
    for page_num in range(pdf_document.page_count):
        try:
            page = pdf_document.load_page(page_num)
            text = page.get_text("text")
            if text:
                extracted_text.append(text)
        except Exception as e:
            # Raise an exception if any specific page fails to process
            pdf_document.close()
            raise Exception(f"Failed to extract text from page {page_num + 1}. Details: {str(e)}")

    pdf_document.close()
    
    # Join the extracted text from all pages
    full_text = "\n".join(extracted_text).strip()
    
    if not full_text:
        raise ValueError("No readable text could be extracted. The PDF might be image-based or empty.")
        
    return full_text
