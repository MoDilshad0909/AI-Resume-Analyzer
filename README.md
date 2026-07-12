# AI Resume Analyzer

![Project Status](https://img.shields.io/badge/Status-In%20Development-blue)
![Python Version](https://img.shields.io/badge/Python-3.12%2B-green)

A professional, industry-level AI-powered Resume Analyzer designed to optimize resumes for Applicant Tracking Systems (ATS) and provide actionable feedback using state-of-the-art Generative AI and NLP models.

## 🚀 Features (Coming Soon)
- **PDF Resume Parsing:** Extract text, skills, and experience seamlessly from PDF resumes.
- **ATS Scoring:** Evaluate resume compatibility against job descriptions.
- **Skill Extraction:** Identify core competencies using NLP (spaCy).
- **Semantic Search:** Match resumes with job requirements using Sentence Transformers and FAISS.
- **AI Feedback:** Generate tailored improvement suggestions via the Google Gemini API.

## 🛠 Tech Stack
- **Language:** Python 3.12+
- **Frontend/UI:** Streamlit
- **Data Manipulation:** Pandas
- **PDF Processing:** PyMuPDF
- **NLP & Embeddings:** spaCy, Sentence Transformers
- **Vector Search:** FAISS
- **Generative AI:** Google Gemini API
- **Environment Management:** python-dotenv

## 📁 Folder Structure
```text
AI-Resume-Analyzer/
├── app.py                 # Main Streamlit application entry point
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── assets/                # Images, logos, and UI assets
├── config/                # Configuration files and constants
├── data/                  # Sample data and datasets
├── models/                # Downloaded or fine-tuned ML models
├── reports/               # Generated analysis reports
├── resumes/               # Uploaded resume files (temporary storage)
├── tests/                 # Unit and integration tests
└── utils/                 # Helper functions and modules
```

## ⚙️ Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Add your Google Gemini API key to the `.env` file.

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 📸 Screenshots
*(Screenshots of the web interface will be added here once development progresses)*

## 🗺 Future Roadmap
- [x] Day 1: Project Setup and UI scaffolding.
- [ ] Day 2: Implement PDF Parsing (PyMuPDF).
- [ ] Day 3: NLP processing and Skill Extraction (spaCy).
- [ ] Day 4: Vector Embeddings and Semantic Search (FAISS).
- [ ] Day 5: Integrate Generative AI for Feedback (Gemini API).
- [ ] Day 6: Finalize UI, Testing, and Deployment preparation.

## 📄 License
This project is licensed under the MIT License.
