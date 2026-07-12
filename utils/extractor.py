"""
Resume Information Extractor Module

This module uses Regular Expressions and spaCy NLP to extract structured
information (Name, Email, Phone, Skills, Education, Experience, Projects)
from raw resume text.
"""
import re
import spacy
from typing import List, Union

# Load spaCy NLP model, download if missing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Predefined dictionary of skills commonly found in tech resumes
SKILLS_DB = [
    "Python", "SQL", "Power BI", "Excel", "Machine Learning", "Deep Learning",
    "TensorFlow", "PyTorch", "Pandas", "NumPy", "Java", "C++", "HTML", "CSS",
    "JavaScript", "Git", "Docker", "AWS", "Azure", "React", "Angular", "Vue",
    "Node.js", "Django", "Flask", "FastAPI", "Scikit-Learn", "NLP", "Computer Vision"
]

def extract_name(text: str) -> str:
    """
    Extracts the person's name using spaCy Named Entity Recognition (NER).
    
    Args:
        text (str): The raw resume text.
        
    Returns:
        str: The extracted name or "Not Found".
    """
    try:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                # Basic check to avoid capturing single letters or extremely long strings
                if 2 < len(ent.text.strip()) < 30:
                    return ent.text.strip()
    except Exception:
        pass
    return "Not Found"

def extract_email(text: str) -> str:
    """
    Extracts the email address using Regular Expressions.
    
    Args:
        text (str): The raw resume text.
        
    Returns:
        str: The extracted email or "Not Found".
    """
    try:
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        if match:
            return match.group(0).strip()
    except Exception:
        pass
    return "Not Found"

def extract_phone(text: str) -> str:
    """
    Extracts the phone number using Regular Expressions.
    
    Args:
        text (str): The raw resume text.
        
    Returns:
        str: The extracted phone number or "Not Found".
    """
    try:
        phone_pattern = r'(\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'
        match = re.search(phone_pattern, text)
        if match:
            return match.group(0).strip()
    except Exception:
        pass
    return "Not Found"

def extract_skills(text: str) -> str:
    """
    Extracts skills from text based on a predefined dictionary.
    
    Args:
        text (str): The raw resume text.
        
    Returns:
        str: A comma-separated string of skills or "Not Found".
    """
    try:
        extracted_skills = set()
        text_lower = text.lower()
        
        for skill in SKILLS_DB:
            # Word boundary regex to avoid partial matches (e.g. 'java' in 'javascript')
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                extracted_skills.add(skill)
                
        if extracted_skills:
            return ", ".join(sorted(list(extracted_skills)))
    except Exception:
        pass
    return "Not Found"

def extract_education(text: str) -> str:
    """
    Extracts education degrees from text.
    
    Args:
        text (str): The raw resume text.
        
    Returns:
        str: A comma-separated string of degrees or "Not Found".
    """
    try:
        degrees = ["B.Tech", "B.E.", "M.Tech", "MBA", "MCA", "BCA", "MSc", "BSc", "PhD", "Bachelor", "Master"]
        extracted_edu = set()
        
        for degree in degrees:
            pattern = r'\b' + re.escape(degree) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                extracted_edu.add(degree)
                
        if extracted_edu:
            return ", ".join(sorted(list(extracted_edu)))
    except Exception:
        pass
    return "Not Found"

def extract_experience(text: str) -> str:
    """
    Extracts experience/internship references from text using heuristics.
    
    Args:
        text (str): The raw resume text.
        
    Returns:
        str: A snippet of the experience section or "Not Found".
    """
    try:
        lines = text.split('\n')
        experience_lines = []
        in_experience_section = False
        
        for line in lines:
            line_lower = line.strip().lower()
            if line_lower in ['experience', 'work experience', 'internship', 'internships', 'employment history', 'professional experience']:
                in_experience_section = True
                continue
            
            if in_experience_section:
                # Stop if we hit another common section header
                if line_lower in ['education', 'projects', 'skills', 'certifications', 'achievements', 'summary']:
                    break
                if line.strip():
                    experience_lines.append(line.strip())
                    
        if experience_lines:
            extracted = " | ".join(experience_lines[:5])
            if len(experience_lines) > 5:
                extracted += " ..."
            return extracted
    except Exception:
        pass
    return "Not Found"

def extract_projects(text: str) -> str:
    """
    Extracts project references from text using heuristics.
    
    Args:
        text (str): The raw resume text.
        
    Returns:
        str: A snippet of the projects section or "Not Found".
    """
    try:
        lines = text.split('\n')
        project_lines = []
        in_project_section = False
        
        for line in lines:
            line_lower = line.strip().lower()
            if line_lower in ['projects', 'academic projects', 'personal projects', 'key projects']:
                in_project_section = True
                continue
            
            if in_project_section:
                # Stop if we hit another common section header
                if line_lower in ['education', 'experience', 'skills', 'certifications', 'achievements', 'work experience', 'professional experience']:
                    break
                if line.strip():
                    project_lines.append(line.strip())
                    
        if project_lines:
            extracted = " | ".join(project_lines[:5])
            if len(project_lines) > 5:
                extracted += " ..."
            return extracted
    except Exception:
        pass
    return "Not Found"
