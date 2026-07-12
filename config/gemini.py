"""
Gemini Configuration Module

This module handles loading environment variables and configuring the
Google Gemini Generative AI client securely.
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()

# Singleton instance to prevent multiple configurations
_MODEL_INSTANCE = None

def initialize_gemini():
    """
    Initializes the Google Gemini API client securely and returns the model.
    Reads the API key from the environment variables.
    
    Returns:
        genai.GenerativeModel: The configured Gemini model instance.
        
    Raises:
        ValueError: If the GEMINI_API_KEY is missing or invalid.
    """
    global _MODEL_INSTANCE
    
    if _MODEL_INSTANCE is not None:
        return _MODEL_INSTANCE
        
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key.strip() == "" or api_key == "your_gemini_api_key_here":
        raise ValueError("A valid GEMINI_API_KEY is not set in the .env file. Please update it to use AI features.")
        
    # Configure the global genai client
    genai.configure(api_key=api_key)
    
    # We use gemini-1.5-flash as it is highly optimized for fast text processing
    _MODEL_INSTANCE = genai.GenerativeModel('gemini-1.5-flash')
    
    return _MODEL_INSTANCE
