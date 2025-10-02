📄 AI Research Paper Maker

Automatically generate structured research papers in plain text using AI-powered services.

Project Overview

This project allows users to input a research topic and automatically generate a structured research paper with the following sections:

Abstract

Introduction

Literature Review

Methodology

Results

Discussion

Conclusion

References

The backend is built with FastAPI, and the frontend uses Streamlit. Jobs are tracked asynchronously, and plain-text output ensures readability.

Folder Structure : 
                research-paper-maker/
│── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI entrypoint
│   ├── services.py      # LLM & Tavily API integration
│   ├── workflow.py      # Paper generation workflow
│   ├── jobs.py          # Job state storage
│   └── utils.py         # Helpers, LangSmith tracking
│
│── frontend.py           # Streamlit UI
│── README.md
│── requirements.txt
│── .gitignore
│── .env                 


Setup Instructions

1. Clone the repository

git clone https://github.com/rarihant14/research-paper-maker.git
cd research-paper-maker


2. Create virtual environment

python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows




3. Install dependencies

pip install -r requirements.txt



4. Create .env file in project root with your API keys:

TAVILY_API_KEY=your-tavily-key
GROQ_API_KEY=your-groq-key
GEMINI_API_KEY=your-gemini-key
LANGSMITH_API_KEY=your-langsmith-key