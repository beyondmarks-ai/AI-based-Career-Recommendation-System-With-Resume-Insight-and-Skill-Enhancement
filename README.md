
<!-- Banner -->
<p align="center">
  <img src="https://img.shields.io/badge/Beyond%20Marks%20AI%20Academy-Streamlit%20App-blueviolet?style=for-the-badge&logo=streamlit" alt="Beyond Marks AI Academy" />
</p>

# 🧠 Beyond Marks AI Academy

Beyond Marks AI Academy is a GenAI-powered Streamlit application that helps job seekers evaluate, improve, and align their resumes to specific roles using LLMs. It also includes an ATS (Applicant Tracking System) compatibility checker, personalized recommendations, and detailed scoring.

---

## 🚀 Features

- 📄 Upload resume (PDF/DOCX) and extract raw text
- 🎯 Input desired job role (e.g., "Backend Engineer", "Product Manager")
- 🌍 Select output language (English, Hindi, French)
- 🤖 Powered by Groq API using LLaMA3-70B via LangChain
- 💬 AI-generated resume evaluation, feedback, and rating out of 10
- 📌 Actionable bullet-point suggestions & formatting fixes
- ⚙️ ATS-compliance check for keyword optimization and structure
- 📋 One-click copy of evaluation to clipboard
- ☁️ Deployed on Streamlit Cloud

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **LLM:** LLaMA3-70B via Groq API + LangChain
- **Resume Parsing:** PyPDF2, python-docx
- **Security:** `.env` + Streamlit Secrets for key management
- **Deployment:** Streamlit Cloud + GitHub

---

## 📂 Folder Structure

```
├── main.py
├── llm_helper.py
├── resume_parser.py
├── roadmap_generator.py
├── .env                  # Not pushed to GitHub (ignored)
├── requirements.txt
└── README.md
```

---
## 💡 How It Works

1. User uploads resume and enters target role.
2. Resume text is extracted using `PyPDF2` or `python-docx`.
3. Prompt is generated and sent to Groq’s LLaMA3 via LangChain.
4. AI analyzes tone, relevance, structure, keywords, etc.
5. An ATS check is also performed for compatibility with job boards.
6. Feedback + score is rendered in Streamlit UI with copy option.

---
## 🌟 Live Demo

🧪 Try it live: [Beyond Marks AI Academy Streamlit App](https://ai-resume-analyzer-p7c3u8xfbcnbfrpm5ra7zy.streamlit.app/)

---
## © Copyright

Copyright © 2026 **Beyond Marks AI Academy**. All rights reserved.

---
# AI-based-Career-Recommendation-System-With-Resume-Insight-and-Skill-Enhancement

# AI-based-Career-Recommendation-System-With-Resume-Insight-and-Skill-Enhancement
