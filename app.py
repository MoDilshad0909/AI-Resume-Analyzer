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
from utils.cover_letter import generate_cover_letter
from utils.linkedin import generate_linkedin_headline, generate_professional_summary
from utils.email_generator import generate_cold_email
from utils.interview import generate_interview_questions

def main():
    """
    Main function to run the Streamlit AI Resume Analyzer application.
    """
    st.set_page_config(
        page_title="AI Career Assistant",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
        <style>
        .main { background-color: #FFFFFF; color: #333333; }
        .stButton>button { background-color: #4CAF50; color: white; border-radius: 5px; border: none; padding: 10px 24px; font-weight: bold; }
        .stButton>button:hover { background-color: #45a049; }
        .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #f8f9fa; color: #6c757d; text-align: center; padding: 15px; font-size: 14px; border-top: 1px solid #dee2e6; z-index: 999; }
        .block-container { padding-bottom: 80px; }
        .stTextArea textarea { font-family: 'Courier New', Courier, monospace; font-size: 14px !important; background-color: #f8f9fa; color: #212529; border: 1px solid #ced4da; border-radius: 4px; }
        .info-card { background-color: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e9ecef; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 20px; height: 100%; }
        .info-card h4 { margin-top: 0; color: #4CAF50; font-size: 16px; margin-bottom: 10px; font-weight: 600; }
        .info-card p { margin: 0; font-size: 15px; color: #333; word-wrap: break-word; }
        .stTabs [data-baseweb="tab-list"] { gap: 10px; }
        .stTabs [data-baseweb="tab"] { height: 50px; border-radius: 4px 4px 0px 0px; padding: 10px 20px; background-color: #f8f9fa; }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.image("https://via.placeholder.com/300x100.png?text=AI+Career+Assistant", use_container_width=True)
        st.title("Settings")
        st.info("Check your `.env` file to ensure `GEMINI_API_KEY` is configured for AI features.")

    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("https://via.placeholder.com/80x80.png?text=Icon", use_container_width=True)
    with col2:
        st.title("AI Career Assistant")
        st.subheader("Your end-to-end intelligent career optimization platform.")

    st.markdown("---")

    col_upload1, col_upload2 = st.columns([1, 1])
    
    with col_upload1:
        st.markdown("### 📥 1. Upload Your Resume")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    with col_upload2:
        st.markdown("### 📝 2. Target Job Description (Optional)")
        jd_text = st.text_area("Paste JD here...", height=120, label_visibility="collapsed")

    if uploaded_file is not None:
        try:
            file_bytes = uploaded_file.read()
            extracted_text = extract_text_from_pdf(file_bytes)
            
            name = extract_name(extracted_text)
            email = extract_email(extracted_text)
            phone = extract_phone(extracted_text)
            skills = extract_skills(extracted_text)
            education = extract_education(extracted_text)
            experience = extract_experience(extracted_text)
            projects = extract_projects(extracted_text)
            
            extracted_data = {
                "name": name, "email": email, "phone": phone,
                "skills": skills, "education": education,
                "experience": experience, "projects": projects
            }

            st.success("✅ Resume Processed Successfully!")
            st.markdown("---")
            
            tab_extract, tab_ats, tab_jd, tab_ai, tab_cover, tab_linkedin, tab_email, tab_interview = st.tabs([
                "📝 Extracted Info", 
                "📊 ATS Score", 
                "🎯 JD Match", 
                "🤖 Resume Review",
                "✉️ Cover Letter",
                "💼 LinkedIn",
                "📧 Cold Email",
                "🎤 Interview Prep"
            ])
            
            with tab_extract:
                col_a, col_b, col_c = st.columns(3)
                with col_a: st.markdown(f'<div class="info-card"><h4>👤 Name</h4><p>{name}</p></div>', unsafe_allow_html=True)
                with col_b: st.markdown(f'<div class="info-card"><h4>📧 Email</h4><p>{email}</p></div>', unsafe_allow_html=True)
                with col_c: st.markdown(f'<div class="info-card"><h4>📱 Phone</h4><p>{phone}</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="info-card"><h4>🛠️ Skills</h4><p>{skills}</p></div>', unsafe_allow_html=True)
                col_d, col_e, col_f = st.columns(3)
                with col_d: st.markdown(f'<div class="info-card"><h4>🎓 Education</h4><p>{education}</p></div>', unsafe_allow_html=True)
                with col_e: st.markdown(f'<div class="info-card"><h4>💼 Experience</h4><p>{experience}</p></div>', unsafe_allow_html=True)
                with col_f: st.markdown(f'<div class="info-card"><h4>📂 Projects</h4><p>{projects}</p></div>', unsafe_allow_html=True)

            with tab_ats:
                score, strengths, weaknesses = calculate_ats_score(extracted_data, extracted_text)
                missing_skills = find_missing_skills(skills)
                ats_recommendations = generate_recommendations(weaknesses, missing_skills)
                
                st.markdown(f"#### Overall Score: **{score}/100**")
                st.progress(score / 100)
                col_s, col_w = st.columns(2)
                with col_s:
                    st.markdown("##### ✅ Strengths")
                    for s in strengths: st.markdown(f"- {s}")
                with col_w:
                    st.markdown("##### ❌ Weaknesses")
                    for w in weaknesses: st.markdown(f"- {w}")
                st.markdown("##### 💡 Recommendations")
                for r in ats_recommendations: st.markdown(f"- {r}")

            with tab_jd:
                if not jd_text.strip():
                    st.info("ℹ️ Paste a Job Description above to see semantic matching.")
                else:
                    resume_skills_list = [s.strip() for s in skills.split(',')] if skills != "Not Found" else []
                    with st.spinner("Calculating semantic match..."):
                        jd_keywords = extract_keywords(jd_text)
                        matched_skills = get_matching_skills(resume_skills_list, jd_keywords)
                        missing_skills_jd = get_missing_skills(matched_skills, jd_keywords)
                        match_score = calculate_match_score(matched_skills, jd_keywords)
                        st.markdown(f"### 🎯 Resume Match: **{match_score}%**")
                        st.progress(match_score / 100)
                        col_stats1, col_stats2, col_stats3 = st.columns(3)
                        col_stats1.metric("JD Skills", len(jd_keywords))
                        col_stats2.metric("Matched", len(matched_skills))
                        col_stats3.metric("Missing", len(missing_skills_jd))

            with tab_ai:
                st.markdown("### 🤖 Intelligent Resume Review")
                if st.button("✨ Generate Review", key="btn_review"):
                    with st.spinner("Analyzing..."):
                        st.info(review_resume(extracted_text))
                        st.success(improve_summary(extracted_text))
                        st.success(rewrite_experience(experience))
                        st.warning(generate_resume_feedback(extracted_text))
                        if jd_text.strip():
                            st.error(suggest_missing_keywords(extracted_text, jd_text))

            with tab_cover:
                st.markdown("### ✉️ Cover Letter Generator")
                if not jd_text.strip():
                    st.info("Please paste a Job Description to generate a Cover Letter.")
                else:
                    if st.button("✨ Generate Cover Letter", key="btn_cl"):
                        with st.spinner("Writing..."):
                            cl_text = generate_cover_letter(extracted_text, jd_text)
                            st.markdown(cl_text)
                            st.download_button("📥 Download txt", cl_text, "Cover_Letter.txt")

            with tab_linkedin:
                st.markdown("### 💼 LinkedIn Profile Optimizer")
                if st.button("✨ Generate LinkedIn Content", key="btn_li"):
                    with st.spinner("Optimizing..."):
                        st.markdown("#### Headlines")
                        hl_text = generate_linkedin_headline(extracted_text)
                        st.info(hl_text)
                        st.markdown("#### About Section Summary")
                        sum_text = generate_professional_summary(extracted_text)
                        st.success(sum_text)
                        st.download_button("📥 Download Content", f"Headlines:\n{hl_text}\n\nSummary:\n{sum_text}", "LinkedIn_Content.txt")

            with tab_email:
                st.markdown("### 📧 Cold Email Outreach Generator")
                if not jd_text.strip():
                    st.info("Please paste a Job Description to generate a Cold Email.")
                else:
                    if st.button("✨ Generate Cold Email", key="btn_email"):
                        with st.spinner("Drafting..."):
                            email_text = generate_cold_email(extracted_text, jd_text)
                            st.markdown(email_text)
                            st.download_button("📥 Download Email", email_text, "Cold_Email.txt")

            with tab_interview:
                st.markdown("### 🎤 Interview Preparation")
                if not jd_text.strip():
                    st.info("Please paste a Job Description to generate tailored Interview Questions.")
                else:
                    if st.button("✨ Generate Interview Questions", key="btn_int"):
                        with st.spinner("Generating Q&A..."):
                            int_text = generate_interview_questions(extracted_text, jd_text)
                            st.markdown(int_text)
                            st.download_button("📥 Download Q&A", int_text, "Interview_Prep.txt")
                            
        except Exception as e:
            st.error(f"❌ **Failed to process Request:** {e}")

    st.markdown('<div class="footer"><p>© 2026 AI Career Assistant</p></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
