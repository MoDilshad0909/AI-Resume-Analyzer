"""
Interview Preparation Module

This module generates targeted interview questions based on the 
alignment between a candidate's resume and a specific Job Description.
"""
from config.gemini import initialize_gemini

def generate_interview_questions(resume_text: str, jd_text: str) -> str:
    """
    Generates tailored interview questions based on Resume and JD.
    
    Args:
        resume_text (str): Extracted resume text.
        jd_text (str): Job description text.
        
    Returns:
        str: Generated interview questions and ideal answers.
    """
    if not jd_text.strip():
        return "Please provide a Job Description to generate tailored interview questions."
        
    prompt = f"""
    You are an expert Technical Recruiter and Hiring Manager.
    Based on the provided Job Description and Candidate Resume, generate 7 highly targeted interview questions.
    Include a mix of technical/hard skills questions, behavioral questions (STAR method), and culture-fit questions based on gaps or highlights in the resume.
    Briefly outline what a 'good' answer would look like for each question to help the candidate prepare.
    
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
