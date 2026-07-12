"""
Cold Email Generator Module

This module generates tailored cold outreach emails to recruiters
or hiring managers based on the candidate's resume and a JD.
"""
from config.gemini import initialize_gemini

def generate_cold_email(resume_text: str, jd_text: str) -> str:
    """
    Generates a cold outreach email for the job.
    
    Args:
        resume_text (str): Extracted resume text.
        jd_text (str): Job description text.
        
    Returns:
        str: Generated cold email.
    """
    if not jd_text.strip():
        return "Please provide a Job Description to generate a tailored cold email."
        
    prompt = f"""
    You are an expert Career Coach and B2B Copywriter.
    Write a concise, compelling cold outreach email to a hiring manager or recruiter for the following job description, leveraging the candidate's resume.
    Keep it under 150 words. Focus on the immediate value the candidate brings and include a clear subject line.
    
    Job Description:
    {jd_text[:2000]}
    
    Resume:
    {resume_text[:2500]}
    """
    try:
        model = initialize_gemini()
        response = model.generate_content(prompt)
        return response.text if response and response.text else "AI could not generate a response."
    except Exception as e:
        return f"Failed to connect to AI Service: {str(e)}"
