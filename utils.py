import streamlit as st
import re
from typing import Dict, List, Any

def clear_session_state():
    """Clear all document-related session state variables."""
    keys_to_clear = [
        "document_content",
        "document_summary", 
        "document_name",
        "interaction_mode",
        "challenge_questions",
        "challenge_answers",
        "qa_history"
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def format_citation(citation: str) -> str:
    """
    Format citation text for better display.
    
    Args:
        citation: Raw citation text
        
    Returns:
        str: Formatted citation
    """
    if not citation:
        return "No specific citation available"
    
    # Clean up the citation text
    citation = citation.strip()
    
    # Add proper formatting
    if not citation.startswith("Source:") and not citation.startswith("Reference:"):
        citation = f"Source: {citation}"
    
    return citation

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length].strip() + "..."

def validate_file_size(uploaded_file, max_size_mb: int = 10) -> bool:
    """
    Validate that uploaded file is within size limits.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        max_size_mb: Maximum file size in MB
        
    Returns:
        bool: True if file size is acceptable
    """
    if uploaded_file is None:
        return False
    
    file_size_mb = uploaded_file.size / (1024 * 1024)
    return file_size_mb <= max_size_mb

def extract_key_phrases(text: str, num_phrases: int = 5) -> List[str]:
    """
    Extract key phrases from text using simple heuristics.
    
    Args:
        text: Input text
        num_phrases: Number of key phrases to extract
        
    Returns:
        list: List of key phrases
    """
    # Simple extraction based on capitalized words and common patterns
    sentences = re.split(r'[.!?]+', text)
    key_phrases = []
    
    for sentence in sentences[:20]:  # Check first 20 sentences
        # Look for capitalized words (potential key terms)
        words = sentence.split()
        for i, word in enumerate(words):
            if (word[0].isupper() and len(word) > 3 and 
                not word.isupper() and word not in ['The', 'This', 'That', 'These', 'Those']):
                
                # Try to capture 2-3 word phrases
                phrase_end = min(i + 3, len(words))
                phrase = ' '.join(words[i:phrase_end])
                
                if len(phrase) > 5 and phrase not in key_phrases:
                    key_phrases.append(phrase)
                    
                if len(key_phrases) >= num_phrases:
                    break
        
        if len(key_phrases) >= num_phrases:
            break
    
    return key_phrases[:num_phrases]

def format_score_color(score: int) -> str:
    """
    Get color code for score display.
    
    Args:
        score: Numeric score (0-100)
        
    Returns:
        str: Color code for Streamlit
    """
    if score >= 80:
        return "green"
    elif score >= 60:
        return "orange"
    else:
        return "red"

def get_reading_time_estimate(text: str, wpm: int = 200) -> str:
    """
    Estimate reading time for given text.
    
    Args:
        text: Text content
        wpm: Words per minute reading speed
        
    Returns:
        str: Formatted reading time estimate
    """
    word_count = len(text.split())
    minutes = max(1, word_count // wpm)
    
    if minutes == 1:
        return "1 minute"
    elif minutes < 60:
        return f"{minutes} minutes"
    else:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if remaining_minutes == 0:
            return f"{hours} hour{'s' if hours > 1 else ''}"
        else:
            return f"{hours} hour{'s' if hours > 1 else ''} {remaining_minutes} minutes"

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage.
    
    Args:
        filename: Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[^\w\-_\.]', '_', filename)
    
    # Ensure reasonable length
    if len(sanitized) > 50:
        name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
        sanitized = name[:45] + ('.' + ext if ext else '')
    
    return sanitized

def format_document_stats(stats: Dict[str, Any]) -> str:
    """
    Format document statistics for display.
    
    Args:
        stats: Dictionary of document statistics
        
    Returns:
        str: Formatted statistics string
    """
    return f"""
    📊 **Document Statistics:**
    - **Words:** {stats.get('words', 0):,}
    - **Characters:** {stats.get('characters', 0):,}
    - **Lines:** {stats.get('lines', 0):,}
    - **Estimated reading time:** {stats.get('estimated_reading_time', 1)} minutes
    """

def check_api_key() -> bool:
    """
    Check if OpenAI API key is available.
    
    Returns:
        bool: True if API key is available
    """
    import os
    return bool(os.getenv("OPENAI_API_KEY"))

def display_error_message(error_type: str, details: str = ""):
    """
    Display standardized error messages.
    
    Args:
        error_type: Type of error (api, file, processing, etc.)
        details: Additional error details
    """
    error_messages = {
        "api": "❌ **API Error**: Unable to connect to OpenAI services. Please check your API key and try again.",
        "file": "❌ **File Error**: There was an issue processing your document. Please ensure it's a valid PDF or TXT file.",
        "processing": "❌ **Processing Error**: An error occurred while analyzing the document.",
        "upload": "❌ **Upload Error**: Failed to upload the document. Please try again.",
        "general": "❌ **Error**: An unexpected error occurred."
    }
    
    base_message = error_messages.get(error_type, error_messages["general"])
    
    if details:
        st.error(f"{base_message}\n\n**Details:** {details}")
    else:
        st.error(base_message)

def create_progress_indicator(current_step: int, total_steps: int, step_name: str = ""):
    """
    Create a progress indicator for multi-step processes.
    
    Args:
        current_step: Current step number
        total_steps: Total number of steps
        step_name: Name of current step
    """
    progress = current_step / total_steps
    
    if step_name:
        st.write(f"**Step {current_step}/{total_steps}:** {step_name}")
    
    st.progress(progress)
