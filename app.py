import streamlit as st
from utils.parser import extract_text_from_pdf
from utils.extractor import (
    extract_name, extract_email, extract_phone,
    extract_skills, extract_education,
    extract_experience, extract_projects
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
        /* Style for the text area */
        .stTextArea textarea {
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px !important;
            background-color: #f8f9fa;
            color: #212529;
            border: 1px solid #ced4da;
            border-radius: 4px;
        }
        /* Custom Card Styling for Extracted Info */
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
        </style>
    """, unsafe_allow_html=True)

    # --- Sidebar ---
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100.png?text=Logo+Placeholder", use_container_width=True)
        st.title("Settings")
        st.markdown("Configure your AI Resume Analyzer here.")
        st.markdown("---")
        st.info("Additional configuration options (e.g., Target Job Role, API settings) will be added here in future updates.")

    # --- Main Content ---
    # Header Section
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("https://via.placeholder.com/80x80.png?text=Icon", use_container_width=True)
    with col2:
        st.title("AI Resume Analyzer")
        st.subheader("Leverage Generative AI to optimize your resume for ATS and industry standards.")

    st.markdown("---")

    # Upload Section
    st.markdown("### 📥 Upload Your Resume")
    st.markdown("Please upload your resume in **PDF** format for analysis.")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:
        try:
            # Read the uploaded PDF file as bytes
            file_bytes = uploaded_file.read()
            
            # Extract text using our custom parser
            extracted_text = extract_text_from_pdf(file_bytes)
            
            # Display Success Message
            st.success("✅ Resume Uploaded Successfully")
            
            # --- Day 3: Structured Information Extraction ---
            st.markdown("### 🔍 Extracted Information")
            
            # Extract fields
            name = extract_name(extracted_text)
            email = extract_email(extracted_text)
            phone = extract_phone(extracted_text)
            skills = extract_skills(extracted_text)
            education = extract_education(extracted_text)
            experience = extract_experience(extracted_text)
            projects = extract_projects(extracted_text)
            
            # Display fields in cards using Streamlit columns
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
            
            # Display Preview Section
            st.markdown("### 📄 Resume Preview")
            st.markdown("#### Raw Extracted Text")
            
            # Display extracted text in a large scrollable text area
            st.text_area(
                label="Extracted Text",
                value=extracted_text,
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )
            
        except ValueError as ve:
            # Handle empty PDF, image-based PDF, etc.
            st.error(f"⚠️ **Parsing Error:** {ve}")
        except Exception as e:
            # Handle corrupted or unsupported PDFs
            st.error(f"❌ **Failed to process PDF:** {e}")

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
