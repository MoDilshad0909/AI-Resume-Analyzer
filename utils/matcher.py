"""
Job Description Matching Engine Module

This module compares a candidate's extracted resume information against a 
Job Description (JD) using exact keyword matching and semantic similarity 
via SentenceTransformers.
"""

import streamlit as st
import spacy
from sentence_transformers import SentenceTransformer, util
from typing import List
import re
from utils.extractor import SKILLS_DB

@st.cache_resource
def load_semantic_model():
    """
    Loads the SentenceTransformer model for semantic matching.
    Cached to prevent reloading on every Streamlit run.
    """
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource
def load_spacy_model():
    """
    Loads the spaCy NLP model.
    Cached to prevent reloading on every Streamlit run.
    """
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        import spacy.cli
        spacy.cli.download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

def extract_keywords(jd_text: str) -> List[str]:
    """
    Extracts important keywords (skills, tools) from the Job Description.
    
    Args:
        jd_text (str): The raw job description text.
        
    Returns:
        List[str]: A list of extracted keywords.
    """
    if not jd_text or not jd_text.strip():
        return []
        
    nlp = load_spacy_model()
    doc = nlp(jd_text)
    
    jd_keywords = set()
    jd_lower = jd_text.lower()
    
    # 1. Exact match from predefined SKILLS_DB
    for skill in SKILLS_DB:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, jd_lower):
            jd_keywords.add(skill)
            
    # 2. Extract Proper Nouns as potential technologies/tools
    for token in doc:
        if token.pos_ == 'PROPN' and not token.is_stop and len(token.text) > 2:
            clean_token = token.text.strip(".,;:()[]{}")
            if clean_token and not clean_token.isnumeric():
                jd_keywords.add(clean_token.title())
                
    # Sort and limit to the top 40 keywords to avoid noise
    final_keywords = sorted(list(jd_keywords))
    return final_keywords[:40]

def get_matching_skills(resume_skills: List[str], jd_keywords: List[str], threshold: float = 0.6) -> List[str]:
    """
    Finds JD keywords matched by Resume skills using Semantic Similarity.
    
    Args:
        resume_skills (List[str]): Skills extracted from the resume.
        jd_keywords (List[str]): Keywords extracted from the JD.
        threshold (float): Cosine similarity threshold for a semantic match.
        
    Returns:
        List[str]: The matched JD keywords.
    """
    if not jd_keywords or not resume_skills:
        return []
        
    model = load_semantic_model()
    
    # Convert lists to embeddings
    resume_embeddings = model.encode(resume_skills, convert_to_tensor=True)
    jd_embeddings = model.encode(jd_keywords, convert_to_tensor=True)
    
    # Compute cosine similarity matrix between JD keywords and Resume skills
    cosine_scores = util.cos_sim(jd_embeddings, resume_embeddings)
    
    matched = set()
    
    # For each JD keyword, check if there is any resume skill with similarity >= threshold
    for i, jd_kw in enumerate(jd_keywords):
        max_score = cosine_scores[i].max().item()
        if max_score >= threshold:
            matched.add(jd_kw)
            
    return sorted(list(matched))

def get_missing_skills(matched_skills: List[str], jd_keywords: List[str]) -> List[str]:
    """
    Identifies JD keywords that were not matched.
    
    Args:
        matched_skills (List[str]): Skills successfully matched.
        jd_keywords (List[str]): All extracted JD keywords.
        
    Returns:
        List[str]: Missing keywords.
    """
    matched_set = set(matched_skills)
    missing = [kw for kw in jd_keywords if kw not in matched_set]
    return missing

def calculate_match_score(matched_skills: List[str], jd_keywords: List[str]) -> int:
    """
    Calculates the Match Percentage (0-100).
    
    Args:
        matched_skills (List[str]): The skills that successfully matched.
        jd_keywords (List[str]): The total required skills/keywords.
        
    Returns:
        int: Match percentage score.
    """
    if not jd_keywords:
        return 0
    ratio = len(matched_skills) / len(jd_keywords)
    score = int(ratio * 100)
    return min(100, max(0, score))

def generate_match_recommendations(missing_skills: List[str], score: int) -> List[str]:
    """
    Generates actionable recommendations based on missing skills and match score.
    
    Args:
        missing_skills (List[str]): JD skills not found in the resume.
        score (int): The match percentage.
        
    Returns:
        List[str]: Actionable recommendations.
    """
    recs = []
    
    if score >= 80:
        recs.append("Great job! Your resume is highly tailored to this job description.")
    elif score >= 50:
        recs.append("Your resume has a moderate match. Consider adding some of the missing keywords if you have experience with them.")
    else:
        recs.append("Your resume match is low. You may need to heavily tailor your resume for this specific role to pass ATS screening.")
        
    if missing_skills:
        # Show top 5 missing skills in recommendation to keep it concise
        top_missing = missing_skills[:5]
        recs.append(f"Consider highlighting these missing skills in your experience bullets: {', '.join(top_missing)}")
        
    return recs
