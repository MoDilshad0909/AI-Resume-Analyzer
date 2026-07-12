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
from utils.ai_review import (
    review_resume, improve_summary, rewrite_experience,
    suggest_missing_keywords, generate_resume_feedback
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
        /* Custom UI tweaks for tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            border-radius: 4px 4px 0px 0px;
            padding: 10px 20px;
            background-color: #f8f9fa;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Sidebar ---
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100.png?text=Logo+Placeholder", use_container_width=True)
        st.title("Settings")
        st.markdown("Configure your AI Resume Analyzer here.")
        st.markdown("---")
        st.info("Check your `.env` file to ensure `GEMINI_API_KEY` is configured for AI features.")

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
            st.markdown("---")
            
            # Reorganizing outputs into modern Streamlit Tabs
            tab_extract, tab_ats, tab_jd, tab_ai = st.tabs([
                "📝 Extracted Info", 
                "📊 ATS Dashboard", 
                "🎯 JD Match", 
                "🤖 AI Intelligent Review"
            ])
            
            # --- TAB 1: Extracted Info ---
            with tab_extract:
                st.markdown("### 🔍 Structured Data")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.markdown(f"""
                    <div class="info-card"><h4>👤 Name</h4><p>{name}</p></div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"""
                    <div class="info-card"><h4>📧 Email</h4><p>{email}</p></div>
                    """, unsafe_allow_html=True)
                with col_c:
                    st.markdown(f"""
                    <div class="info-card"><h4>📱 Phone</h4><p>{phone}</p></div>
                    """, unsafe_allow_html=True)
                    
                st.markdown(f"""
                <div class="info-card"><h4>🛠️ Skills</h4><p>{skills}</p></div>
                """, unsafe_allow_html=True)
                
                col_d, col_e, col_f = st.columns(3)
                with col_d:
                    st.markdown(f"""
                    <div class="info-card"><h4>🎓 Education</h4><p>{education}</p></div>
                    """, unsafe_allow_html=True)
                with col_e:
                    st.markdown(f"""
                    <div class="info-card"><h4>💼 Experience</h4><p>{experience}</p></div>
                    """, unsafe_allow_html=True)
                with col_f:
                    st.markdown(f"""
                    <div class="info-card"><h4>📂 Projects</h4><p>{projects}</p></div>
                    """, unsafe_allow_html=True)

                st.markdown("### 📄 Raw Text Preview")
                st.text_area(label="Extracted Text", value=extracted_text, height=300, disabled=True, label_visibility="collapsed")

            # --- TAB 2: ATS Score Dashboard ---
            with tab_ats:
                st.markdown("### 📊 Standard ATS Evaluation")
                score, strengths, weaknesses = calculate_ats_score(extracted_data, extracted_text)
                missing_skills = find_missing_skills(skills)
                ats_recommendations = generate_recommendations(weaknesses, missing_skills)
                
                st.markdown(f"#### Overall Score: **{score}/100**")
                st.progress(score / 100)
                
                if score >= 80:
                    st.success("Excellent! Your resume is highly compatible with general ATS filters.")
                elif score >= 60:
                    st.warning("Good, but there is room for improvement to pass strict ATS filters.")
                else:
                    st.error("Needs Work. Please review the recommendations below.")
                    
                col_s, col_w = st.columns(2)
                with col_s:
                    st.markdown("##### ✅ Resume Strengths")
                    for s in strengths:
                        st.markdown(f"- {s}")
                with col_w:
                    st.markdown("##### ❌ Resume Weaknesses")
                    for w in weaknesses:
                        st.markdown(f"- {w}")
                        
                st.markdown("##### 💡 Actionable Recommendations")
                for r in ats_recommendations:
                    st.markdown(f"- {r}")

            # --- TAB 3: Job Description Match Analysis ---
            with tab_jd:
                if not jd_text.strip():
                    st.info("ℹ️ Paste a Job Description in the text area above to see semantic matching results.")
                else:
                    resume_skills_list = [s.strip() for s in skills.split(',')] if skills != "Not Found" else []
                    
                    with st.spinner("Calculating semantic match with Job Description..."):
                        jd_keywords = extract_keywords(jd_text)
                        
                        if not jd_keywords:
                            st.warning("⚠️ Could not extract enough keywords from the JD.")
                        else:
                            matched_skills = get_matching_skills(resume_skills_list, jd_keywords)
                            missing_skills_jd = get_missing_skills(matched_skills, jd_keywords)
                            match_score = calculate_match_score(matched_skills, jd_keywords)
                            jd_recs = generate_match_recommendations(missing_skills_jd, match_score)
                            
                            st.markdown(f"### 🎯 Resume Match Percentage: **{match_score}%**")
                            st.progress(match_score / 100)
                            
                            col_stats1, col_stats2, col_stats3 = st.columns(3)
                            col_stats1.metric("Total Job Skills", len(jd_keywords))
                            col_stats2.metric("Matched Skills", len(matched_skills))
                            col_stats3.metric("Missing Skills", len(missing_skills_jd))
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            
                            col_jd1, col_jd2 = st.columns(2)
                            with col_jd1:
                                st.markdown("##### ✅ Matched Skills (Semantic)")
                                if matched_skills:
                                    st.markdown(", ".join([f"`{ms}`" for ms in matched_skills]))
                                else:
                                    st.info("No semantic matches found.")
                            with col_jd2:
                                st.markdown("##### ❌ Missing JD Skills")
                                if missing_skills_jd:
                                    st.markdown(", ".join([f"`{ms}`" for ms in missing_skills_jd]))
                                else:
                                    st.success("You matched all key JD skills!")
                                    
                            st.markdown("##### 💡 Recommendations")
                            for rec in jd_recs:
                                st.info(rec)

            # --- TAB 4: Gemini AI Intelligent Review ---
            with tab_ai:
                st.markdown("### 🤖 Gemini AI Resume Assistant")
                st.markdown("Leverage Google Generative AI to deeply analyze and rewrite your resume content.")
                
                if st.button("✨ Generate AI Insights"):
                    with st.spinner("Gemini is analyzing your resume... this may take a few seconds."):
                        ai_review = review_resume(extracted_text)
                        ai_summary = improve_summary(extracted_text)
                        ai_exp = rewrite_experience(experience)
                        ai_feedback = generate_resume_feedback(extracted_text)
                        
                        st.markdown("#### 🧐 Professional Review")
                        st.info(ai_review)
                        
                        st.markdown("#### ✍️ Improved Summary Suggestion")
                        st.success(ai_summary)
                        
                        st.markdown("#### 💼 Experience Rewrite (STAR Method)")
                        st.success(ai_exp)
                        
                        st.markdown("#### ⚙️ Structural ATS Feedback")
                        st.warning(ai_feedback)
                        
                        if jd_text.strip():
                            st.markdown("#### 🔍 JD Specific Keyword Suggestions")
                            ai_jd_keywords = suggest_missing_keywords(extracted_text, jd_text)
                            st.error(ai_jd_keywords)
                            
        except ValueError as ve:
            st.error(f"⚠️ **Error:** {ve}")
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
