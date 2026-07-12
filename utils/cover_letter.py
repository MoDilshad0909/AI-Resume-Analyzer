"""
Cover Letter Generator Module

This module interfaces with the Google Gemini API to generate
ATS-optimized cover letters tailored to a specific Job Description.
"""
from config.gemini import initialize_gemini

def generate_cover_letter(resume_text: str, jd_text: str) -> str:
    """
    Generates a professional cover letter based on Resume and Job Description.
    
    Args:
        resume_text (str): Extracted resume text.
        jd_text (str): Job description text.
        
    Returns:
        str: Generated cover letter text.
    """
    if not jd_text.strip():
        return "Please provide a Job Description to generate a tailored cover letter."
        
    prompt = f"""
    You are an expert Career Coach and Resume Writer.
    Write a highly professional, ATS-optimized cover letter for the following job description based on the candidate's resume.
    Do not use generic placeholders like [Your Name] if the information is available in the resume. 
    Keep it compelling, concise (under 400 words), and focused on the value the candidate brings to the specific role.

    Job Description:
    {jd_text[:2000]}
    
    Resume:
    {resume_text[:2500]}
    """
    try:
        model = initialize_gemini()
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text
        return "AI could not generate a response at this time."
    except Exception as e:
        return f"Failed to connect to Google Gemini AI Service: {str(e)}"
