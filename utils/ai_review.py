"""
AI Review Module

This module interfaces with the Google Gemini API to analyze resumes,
improve professional summaries, rewrite experience bullets, and provide
intelligent ATS structural feedback based on Job Descriptions.
"""
from config.gemini import initialize_gemini

def _generate_content_safe(prompt: str) -> str:
    """
    Helper function to call Gemini safely and handle potential API errors.
    
    Args:
        prompt (str): The structured prompt to send to Gemini.
        
    Returns:
        str: The AI's response text, or an error message if it fails.
    """
    try:
        model = initialize_gemini()
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text
        return "AI could not generate a response at this time."
    except ValueError as ve:
        return f"API Configuration Error: {ve}"
    except Exception as e:
        return f"Failed to connect to Google Gemini AI Service: {str(e)}"

def review_resume(resume_text: str) -> str:
    """
    Provides a general professional review of the resume.
    """
    prompt = f"""
    You are an expert HR Manager and Technical Recruiter.
    Review the following resume and provide a brief, professional critique (max 3 short paragraphs).
    Highlight what the candidate does well and what crucial information is missing.
    
    Resume:
    {resume_text[:2500]}
    """
    return _generate_content_safe(prompt)

def improve_summary(resume_text: str) -> str:
    """
    Generates an improved, ATS-friendly professional summary.
    """
    prompt = f"""
    You are an expert Resume Writer.
    Based on the following resume text, write a powerful, ATS-friendly professional summary (3-4 sentences max).
    Focus heavily on key achievements, core technical competencies, and business impact.
    
    Resume:
    {resume_text[:2500]}
    """
    return _generate_content_safe(prompt)

def rewrite_experience(experience_text: str) -> str:
    """
    Rewrites weak experience bullet points using action verbs and the STAR method.
    """
    if not experience_text or experience_text.strip() == "Not Found":
        return "No experience section found to rewrite. Please ensure your experience section is clearly labeled."
        
    prompt = f"""
    You are an expert Resume Writer.
    Rewrite the following experience section to be more impactful. 
    Use strong action verbs and imply metrics where possible (following the STAR method).
    Keep it concise and format as professional bullet points.
    
    Experience Section:
    {experience_text[:1500]}
    """
    return _generate_content_safe(prompt)

def suggest_missing_keywords(resume_text: str, jd_text: str) -> str:
    """
    Suggests missing keywords specifically based on a Job Description.
    """
    if not jd_text.strip():
        return "No Job Description provided to suggest missing keywords."
        
    prompt = f"""
    You are an ATS Optimization Expert.
    Compare the following Resume to the Job Description. Identify 5-7 highly specific keywords, tools, or skills that are explicitly mentioned in the JD but missing or poorly represented in the Resume.
    Return them as a clean, actionable bulleted list.
    
    Job Description:
    {jd_text[:2000]}
    
    Resume:
    {resume_text[:2500]}
    """
    return _generate_content_safe(prompt)

def generate_resume_feedback(resume_text: str) -> str:
    """
    Generates ATS formatting and structural feedback.
    """
    prompt = f"""
    You are a Senior ATS Software Engineer.
    Analyze the raw text structure of this resume and suggest 3 practical formatting or structural improvements to ensure it parses perfectly in standard ATS systems (e.g. Workday, Greenhouse).
    Focus on layout issues, standard headings, and typical parsing pitfalls.
    
    Resume:
    {resume_text[:2500]}
    """
    return _generate_content_safe(prompt)
