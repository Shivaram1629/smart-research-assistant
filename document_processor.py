import streamlit as st
import pdfplumber
import io
from typing import Union

class DocumentProcessor:
    """Handles document upload and text extraction for PDF and TXT files."""
    
    def __init__(self):
        pass
    
    def extract_text(self, uploaded_file) -> str:
        """
        Extract text content from uploaded file.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            str: Extracted text content
            
        Raises:
            Exception: If file format is unsupported or extraction fails
        """
        try:
            file_extension = uploaded_file.name.lower().split('.')[-1]
            
            if file_extension == 'pdf':
                return self._extract_pdf_text(uploaded_file)
            elif file_extension == 'txt':
                return self._extract_txt_text(uploaded_file)
            else:
                raise Exception(f"Unsupported file format: {file_extension}. Please upload PDF or TXT files only.")
                
        except Exception as e:
            raise Exception(f"Failed to extract text from document: {str(e)}")
    
    def _extract_pdf_text(self, uploaded_file) -> str:
        """Extract text from PDF file using pdfplumber."""
        try:
            # Convert uploaded file to bytes
            pdf_bytes = uploaded_file.read()
            
            # Create a BytesIO object
            pdf_file = io.BytesIO(pdf_bytes)
            
            text_content = ""
            
            with pdfplumber.open(pdf_file) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_content += f"\n--- Page {page_num} ---\n"
                        text_content += page_text + "\n"
            
            if not text_content.strip():
                raise Exception("No text content found in PDF. The file might be image-based or corrupted.")
            
            return text_content.strip()
            
        except Exception as e:
            raise Exception(f"PDF extraction failed: {str(e)}")
    
    def _extract_txt_text(self, uploaded_file) -> str:
        """Extract text from TXT file."""
        try:
            # Try different encodings
            encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    uploaded_file.seek(0)  # Reset file pointer
                    text_content = uploaded_file.read().decode(encoding)
                    
                    if not text_content.strip():
                        raise Exception("The text file appears to be empty.")
                    
                    return text_content.strip()
                    
                except UnicodeDecodeError:
                    continue
            
            raise Exception("Unable to decode text file. Please ensure it's a valid text file with proper encoding.")
            
        except Exception as e:
            raise Exception(f"TXT extraction failed: {str(e)}")
    
    def validate_document_content(self, text: str) -> bool:
        """
        Validate that the extracted text content is suitable for processing.
        
        Args:
            text: Extracted text content
            
        Returns:
            bool: True if content is valid for processing
        """
        if not text or len(text.strip()) < 100:
            return False
        
        # Check for minimum word count (reasonable document should have at least 50 words)
        word_count = len(text.split())
        if word_count < 50:
            return False
        
        return True
    
    def get_document_stats(self, text: str) -> dict:
        """
        Get basic statistics about the document.
        
        Args:
            text: Document text content
            
        Returns:
            dict: Document statistics
        """
        lines = text.split('\n')
        words = text.split()
        characters = len(text)
        
        return {
            "lines": len(lines),
            "words": len(words),
            "characters": characters,
            "characters_no_spaces": len(text.replace(' ', '')),
            "estimated_reading_time": max(1, len(words) // 200)  # Assuming 200 WPM reading speed
        }
