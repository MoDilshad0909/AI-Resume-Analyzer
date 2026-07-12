"""
LinkedIn Optimization Module

This module generates professional LinkedIn headlines and summaries
using Google Gemini AI based on the candidate's resume.
"""
from config.gemini import initialize_gemini

def generate_linkedin_headline(resume_text: str) -> str:
    """
    Generates LinkedIn headline options.
    
    Args:
        resume_text (str): Extracted resume text.
        
    Returns:
        str: Generated headlines.
    """
    prompt = f"""
    You are an expert LinkedIn Brand Strategist.
    Based on the following resume, generate 5 strong, SEO-optimized LinkedIn headlines.
    Make them impactful, professional, and highlight the candidate's core value proposition.
    
    Resume:
    {resume_text[:2500]}
    """
    try:
        model = initialize_gemini()
        response = model.generate_content(prompt)
        return response.text if response and response.text else "AI could not generate a response."
    except Exception as e:
        return f"Failed to connect to AI Service: {str(e)}"

def generate_professional_summary(resume_text: str) -> str:
    """
    Generates a LinkedIn "About" section summary.
    
    Args:
        resume_text (str): Extracted resume text.
        
    Returns:
        str: Generated LinkedIn summary.
    """
    prompt = f"""
    You are an expert LinkedIn Brand Strategist.
    Write a compelling, first-person LinkedIn "About" section summary based on the following resume.
    It should tell a professional story, highlight key achievements, include core skills, and end with a call to action.
    
    Resume:
    {resume_text[:2500]}
    """
    try:
        model = initialize_gemini()
        response = model.generate_content(prompt)
        return response.text if response and response.text else "AI could not generate a response."
    except Exception as e:
        return f"Failed to connect to AI Service: {str(e)}"
