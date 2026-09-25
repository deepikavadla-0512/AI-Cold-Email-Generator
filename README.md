# 📧 AI Cold Email Generator

An AI-powered cold email generator that extracts job information from a careers or job-posting webpage and creates personalized, professional cold emails based on the job role and the candidate's verified portfolio projects.

The application uses **LangChain, Groq, ChromaDB, and Streamlit** to combine job information extraction with portfolio-based project matching and AI-generated email writing.

---

## 🚀 Project Overview

Applying to multiple job opportunities often requires writing a customized email for each position.

The **AI Cold Email Generator** automates this process.

The user provides a job or careers page URL. The application:

1. Fetches the webpage content.
2. Cleans the extracted text.
3. Uses an LLM to identify job postings.
4. Extracts the role, skills, and job description.
5. Searches a portfolio vector database for relevant projects.
6. Generates a personalized cold email.
7. Displays the generated email directly in the Streamlit application.

The generated email is designed to be professional, concise, and based only on the candidate's provided information and verified portfolio projects.

---

## ✨ Features

- 🔗 Accepts job or careers page URLs
- 🧠 AI-powered job information extraction
- 📋 Extracts job roles, skills, and descriptions
- 🔎 Semantic portfolio project matching using ChromaDB
- ✉️ Generates personalized cold emails
- 🛡️ Uses factual constraints to reduce unsupported claims
- 💻 Simple Streamlit web interface
- ☁️ Deployable using Streamlit Community Cloud
- 🔐 API keys handled through environment variables / Streamlit Secrets

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **LangChain**
- **Groq**
- **LLM:** `openai/gpt-oss-120b` through Groq
- **ChromaDB**
- **Pandas**
- **BeautifulSoup**
- **Selenium**
- **python-dotenv**
- **Git & GitHub**

---

## 🏗️ Project Workflow

```text
Job / Careers Page URL
          │
          ▼
   Web Page Loader
          │
          ▼
     Text Cleaning
          │
          ▼
   Job Information Extraction
          │
          ├── Role
          ├── Skills
          └── Description
          │
          ▼
    ChromaDB Portfolio Search
          │
          ▼
 Relevant Portfolio Projects
          │
          ▼
     Groq LLM + Prompt
          │
          ▼
 Personalized Cold Email
          │
          ▼
      Streamlit UI