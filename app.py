import streamlit as st
from utils.parser import extract_text_from_pdf
from utils.extractor import (
    extract_name, extract_email, extract_phone,
    extract_skills, extract_education,
    extract_experience, extract_projects
)
from utils.ats import (
    calculate_ats_score, find_missing_skills, generate_recommendations
)
from utils.matcher import (
    extract_keywords, calculate_match_score,
    get_matching_skills, get_missing_skills,
    generate_match_recommendations
)

def main():
    """
    Main function to run the Streamlit AI Resume Analyzer application.
    """
    # Set page configuration for a professional look
    st.set_page_config(
        page_title="AI Resume Analyzer",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # --- CSS for modern white UI ---
    st.markdown("""
        <style>
        .main {
            background-color: #FFFFFF;
            color: #333333;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 24px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            color: #6c757d;
            text-align: center;
            padding: 15px;
            font-size: 14px;
            border-top: 1px solid #dee2e6;
            z-index: 999;
        }
        .block-container {
            padding-bottom: 80px; /* Space for footer */
        }
        .stTextArea textarea {
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px !important;
            background-color: #f8f9fa;
            color: #212529;
            border: 1px solid #ced4da;
            border-radius: 4px;
        }
        .info-card {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
            margin-bottom: 20px;
            height: 100%;
        }
        .info-card h4 {
            margin-top: 0;
            color: #4CAF50;
            font-size: 16px;
            margin-bottom: 10px;
            font-weight: 600;
        }
        .info-card p {
            margin: 0;
            font-size: 15px;
            color: #333;
            word-wrap: break-word;
        }
        .stMetric {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #e9ecef;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Sidebar ---
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100.png?text=Logo+Placeholder", use_container_width=True)
        st.title("Settings")
        st.markdown("Configure your AI Resume Analyzer here.")
        st.markdown("---")
        st.info("Additional configuration options (e.g., Gemini API settings) will be added here in future updates.")

    # --- Main Content ---
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("https://via.placeholder.com/80x80.png?text=Icon", use_container_width=True)
    with col2:
        st.title("AI Resume Analyzer")
        st.subheader("Leverage Generative AI to optimize your resume for ATS and industry standards.")

    st.markdown("---")

    # Upload Section
    col_upload1, col_upload2 = st.columns([1, 1])
    
    with col_upload1:
        st.markdown("### 📥 1. Upload Your Resume")
        st.markdown("Please upload your resume in **PDF** format for analysis.")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    with col_upload2:
        st.markdown("### 📝 2. Job Description (Optional)")
        st.markdown("Paste the Job Description to check semantic alignment.")
        jd_text = st.text_area("Paste JD here...", height=120, label_visibility="collapsed")

    if uploaded_file is not None:
        try:
            # Extract PDF Text
            file_bytes = uploaded_file.read()
            extracted_text = extract_text_from_pdf(file_bytes)
            
            # Extract fields
            name = extract_name(extracted_text)
            email = extract_email(extracted_text)
            phone = extract_phone(extracted_text)
            skills = extract_skills(extracted_text)
            education = extract_education(extracted_text)
            experience = extract_experience(extracted_text)
            projects = extract_projects(extracted_text)
            
            extracted_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "skills": skills,
                "education": education,
                "experience": experience,
                "projects": projects
            }

            st.success("✅ Resume Uploaded and Processed Successfully!")
            
            # --- Day 5: Job Description Match Analysis ---
            if jd_text.strip():
                st.markdown("---")
                st.markdown("## 🎯 Job Description Match Analysis")
                
                # Convert skills string to list for matching
                resume_skills_list = [s.strip() for s in skills.split(',')] if skills != "Not Found" else []
                
                # Run JD matching logic
                with st.spinner("Calculating semantic match with Job Description..."):
                    jd_keywords = extract_keywords(jd_text)
                    
                    if not jd_keywords:
                        st.warning("⚠️ Could not extract enough keywords from the Job Description. Please paste a more detailed description.")
                    else:
                        matched_skills = get_matching_skills(resume_skills_list, jd_keywords)
                        missing_skills_jd = get_missing_skills(matched_skills, jd_keywords)
                        match_score = calculate_match_score(matched_skills, jd_keywords)
                        jd_recs = generate_match_recommendations(missing_skills_jd, match_score)
                        
                        # Match Score Progress
                        st.markdown(f"### 📊 Resume Match Percentage: **{match_score}%**")
                        st.progress(match_score / 100)
                        
                        # Keyword Statistics using st.metric
                        st.markdown("#### 📈 Keyword Statistics")
                        col_stats1, col_stats2, col_stats3 = st.columns(3)
                        col_stats1.metric(label="Total Job Skills", value=len(jd_keywords))
                        col_stats2.metric(label="Matched Skills", value=len(matched_skills))
                        col_stats3.metric(label="Missing Skills", value=len(missing_skills_jd))
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Detailed Lists
                        col_jd1, col_jd2 = st.columns(2)
                        with col_jd1:
                            st.markdown("#### ✅ Matched Skills (Semantic)")
                            if matched_skills:
                                st.markdown(", ".join([f"`{ms}`" for ms in matched_skills]))
                            else:
                                st.info("No semantic matches found.")
                                
                            st.markdown("#### 📄 Your Resume Skills")
                            if resume_skills_list:
                                st.markdown(", ".join([f"`{rs}`" for rs in resume_skills_list]))
                            else:
                                st.info("No skills detected in resume.")
                                
                        with col_jd2:
                            st.markdown("#### ❌ Missing JD Skills")
                            if missing_skills_jd:
                                st.markdown(", ".join([f"`{ms}`" for ms in missing_skills_jd]))
                            else:
                                st.success("You matched all key JD skills!")
                                
                            st.markdown("#### 📋 Extracted Job Skills")
                            if jd_keywords:
                                st.markdown(", ".join([f"`{jk}`" for jk in jd_keywords]))
                                
                        st.markdown("#### 💡 Match Recommendations")
                        for rec in jd_recs:
                            st.info(rec)

            # --- Day 4: ATS Score Dashboard ---
            st.markdown("---")
            st.markdown("## 📊 Standard ATS Evaluation Dashboard")
            
            score, strengths, weaknesses = calculate_ats_score(extracted_data, extracted_text)
            missing_skills = find_missing_skills(skills)
            ats_recommendations = generate_recommendations(weaknesses, missing_skills)
            
            st.markdown(f"### Overall ATS Score: **{score}/100**")
            st.progress(score / 100)
            
            if score >= 80:
                st.success("Excellent! Your resume is highly compatible with general ATS filters.")
            elif score >= 60:
                st.warning("Good, but there is room for improvement to pass strict ATS filters.")
            else:
                st.error("Needs Work. Please review the recommendations below.")
                
            col_s, col_w = st.columns(2)
            with col_s:
                st.markdown("#### ✅ Resume Strengths")
                for s in strengths:
                    st.markdown(f"- {s}")
            with col_w:
                st.markdown("#### ❌ Resume Weaknesses")
                for w in weaknesses:
                    st.markdown(f"- {w}")
                    
            st.markdown("<br>", unsafe_allow_html=True)
                    
            col_m, col_r = st.columns(2)
            with col_m:
                st.markdown("#### 🔍 Missing General Industry Skills")
                if missing_skills:
                    for ms in missing_skills:
                        st.markdown(f"- `{ms}`")
                else:
                    st.success("No critical industry skills missing!")
            with col_r:
                st.markdown("#### 💡 Actionable Recommendations")
                for r in ats_recommendations:
                    st.markdown(f"- {r}")
            
            # --- Day 3: Structured Information Extraction ---
            st.markdown("---")
            st.markdown("### 🔍 Extracted Information")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown(f"""
                <div class="info-card">
                    <h4>👤 Name</h4>
                    <p>{name}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                st.markdown(f"""
                <div class="info-card">
                    <h4>📧 Email</h4>
                    <p>{email}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_c:
                st.markdown(f"""
                <div class="info-card">
                    <h4>📱 Phone</h4>
                    <p>{phone}</p>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown(f"""
            <div class="info-card">
                <h4>🛠️ Skills</h4>
                <p>{skills}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_d, col_e, col_f = st.columns(3)
            with col_d:
                st.markdown(f"""
                <div class="info-card">
                    <h4>🎓 Education</h4>
                    <p>{education}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_e:
                st.markdown(f"""
                <div class="info-card">
                    <h4>💼 Experience</h4>
                    <p>{experience}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_f:
                st.markdown(f"""
                <div class="info-card">
                    <h4>📂 Projects</h4>
                    <p>{projects}</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            
            st.markdown("### 📄 Resume Preview")
            st.markdown("#### Raw Extracted Text")
            st.text_area(
                label="Extracted Text",
                value=extracted_text,
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )
            
        except ValueError as ve:
            st.error(f"⚠️ **Parsing Error:** {ve}")
        except Exception as e:
            st.error(f"❌ **Failed to process Request:** {e}")

    # --- Footer ---
    st.markdown(
        """
        <div class="footer">
            <p>Developed with ❤️ for Data Science & AI Portfolio | © 2026 AI Resume Analyzer</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
