"""
ATS Scoring Engine Module

This module evaluates extracted resume information and calculates
an Applicant Tracking System (ATS) compatibility score.
It also identifies missing sections, missing skills, and provides recommendations.
"""
from typing import Dict, List, Tuple

# Core industry skills for a general tech/data role to compare against.
# In a full application, this could be dynamic based on the job description.
TARGET_INDUSTRY_SKILLS = {
    "Python", "SQL", "Machine Learning", "Data Analysis", "Communication",
    "Git", "Problem Solving", "Cloud Computing"
}

def check_resume_sections(extracted_data: Dict[str, str]) -> Dict[str, bool]:
    """
    Checks which standard resume sections are present based on extracted data.
    
    Args:
        extracted_data (Dict[str, str]): A dictionary containing extracted fields.
        
    Returns:
        Dict[str, bool]: A dictionary mapping section names to boolean presence.
    """
    sections = {
        "Contact Information": (
            extracted_data.get("email") != "Not Found" or 
            extracted_data.get("phone") != "Not Found"
        ),
        "Education": extracted_data.get("education") != "Not Found",
        "Experience": extracted_data.get("experience") != "Not Found",
        "Skills": extracted_data.get("skills") != "Not Found",
        "Projects": extracted_data.get("projects") != "Not Found"
    }
    return sections

def find_missing_skills(extracted_skills_str: str) -> List[str]:
    """
    Compares extracted skills against a predefined industry target list.
    
    Args:
        extracted_skills_str (str): Comma-separated string of extracted skills.
        
    Returns:
        List[str]: A list of missing important skills.
    """
    if extracted_skills_str == "Not Found":
        return list(TARGET_INDUSTRY_SKILLS)
        
    extracted_skills_set = {skill.strip().lower() for skill in extracted_skills_str.split(",")}
    missing = []
    
    for target in TARGET_INDUSTRY_SKILLS:
        if target.lower() not in extracted_skills_set:
            missing.append(target)
            
    return missing

def calculate_ats_score(extracted_data: Dict[str, str], raw_text: str) -> Tuple[int, List[str], List[str]]:
    """
    Calculates the ATS score out of 100 based on multiple criteria.
    
    Args:
        extracted_data (Dict[str, str]): Extracted resume fields.
        raw_text (str): The raw text of the resume for length/keyword analysis.
        
    Returns:
        Tuple[int, List[str], List[str]]: 
            - score (int)
            - strengths (List[str])
            - weaknesses (List[str])
    """
    score = 0
    strengths = []
    weaknesses = []
    
    # 1. Section Presence (50 points total, 10 per section)
    sections = check_resume_sections(extracted_data)
    for section, is_present in sections.items():
        if is_present:
            score += 10
            strengths.append(f"Includes {section} section.")
        else:
            weaknesses.append(f"Missing {section} section.")
            
    # 2. Resume Length (15 points)
    word_count = len(raw_text.split())
    if 300 <= word_count <= 800:
        score += 15
        strengths.append(f"Optimal resume length ({word_count} words).")
    elif word_count < 300:
        score += 5
        weaknesses.append(f"Resume is too short ({word_count} words). Aim for 300-800 words.")
    else:
        score += 5
        weaknesses.append(f"Resume is too long ({word_count} words). Aim for conciseness.")
        
    # 3. Skills Match (25 points)
    missing_skills = find_missing_skills(extracted_data.get("skills", ""))
    skills_ratio = 1.0 - (len(missing_skills) / len(TARGET_INDUSTRY_SKILLS)) if TARGET_INDUSTRY_SKILLS else 1.0
    skills_score = int(25 * max(0.0, skills_ratio))
    score += skills_score
    
    if skills_score > 15:
        strengths.append("Good match with industry-standard skills.")
    else:
        weaknesses.append("Lacks several key industry skills.")
        
    # 4. Certifications / Keywords Bonus (10 points)
    cert_keywords = ["certification", "certified", "coursera", "udemy", "aws", "azure", "cfa", "cpa", "pmp"]
    raw_lower = raw_text.lower()
    has_certs = any(kw in raw_lower for kw in cert_keywords)
    
    if has_certs:
        score += 10
        strengths.append("Found mentions of certifications or advanced industry keywords.")
    else:
        weaknesses.append("No obvious certifications detected.")

    # Ensure score stays strictly within 0-100 boundaries
    score = max(0, min(100, score))
    
    return score, strengths, weaknesses

def generate_recommendations(weaknesses: List[str], missing_skills: List[str]) -> List[str]:
    """
    Generates actionable ATS improvement recommendations.
    
    Args:
        weaknesses (List[str]): Identified weaknesses in the resume.
        missing_skills (List[str]): Skills missing from the resume.
        
    Returns:
        List[str]: A list of practical recommendations.
    """
    recs = []
    
    if not weaknesses and not missing_skills:
        return ["Your resume looks fantastic! Keep it up and tailor it to specific job descriptions."]
        
    for w in weaknesses:
        if "Missing" in w and "section" in w:
            section_name = w.replace("Missing ", "").replace(" section.", "")
            recs.append(f"Add a dedicated '{section_name}' section to improve parseability.")
        elif "too short" in w:
            recs.append("Expand on your experiences and projects with bullet points detailing achievements.")
        elif "too long" in w:
            recs.append("Condense your resume by removing older or irrelevant experiences.")
        elif "certifications" in w:
            recs.append("Consider adding a 'Certifications' section if you have completed relevant professional courses.")
            
    if missing_skills:
        recs.append(f"Try to naturally incorporate these highly-searched skills if you possess them: {', '.join(missing_skills)}")
        
    recs.append("Ensure you use standard section headings (e.g., 'Work Experience', 'Education', 'Skills') so ATS parsers can easily read your document.")
    
    return recs
