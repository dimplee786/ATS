import os
import re
import docx2txt
import pdfminer.high_level
import spacy
import streamlit as st
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Define profession categories and related skills
PROFESSION_CATEGORIES = {
    "Software Developer": {"C","C++","JavaScript", "Python","Java","MERN Stack","HTML",".NET MVC",".NET Core","Flutter","Smart Contracts","Decentralized Applications","Selenium","Microservices",
                "API Development", "SQL Server"},
    "Data Scientist": {"Python", "Machine Learning", "Deep Learning", "TensorFlow", "Pandas", "NumPy", "Data Science", "SQL", "Statistics"},
    "Marketing": {"SEO", "Digital Marketing", "Google Analytics", "Social Media", "Content Marketing", "PPC", "Email Marketing"},
    "Finance": {"Accounting", "Financial Analysis", "Excel", "Budgeting", "Investment", "Risk Management", "QuickBooks", "Forecasting"},
    "Human Resources": {"Recruitment", "HR Policies", "Payroll", "Employee Engagement", "Training", "Performance Management"},
    
  }

# Function to classify resume based on extracted skills
def classify_resume(skills):
    for profession, skill_set in PROFESSION_CATEGORIES.items():
        if any(skill in skill_set for skill in skills):
            return profession
    return "Other"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    return pdfminer.high_level.extract_text(pdf_path)

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

# Function to extract key information
def extract_info(text):
    doc = nlp(text)

    # Extract email
    email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)

    # Extract phone number
    phone = re.findall(r'\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text)

    # Extract skills
    all_skills = set.union(*PROFESSION_CATEGORIES.values())
    found_skills = {token.text for token in doc if token.text in all_skills}

    # Classify profession
    profession = classify_resume(found_skills)

    return {
        "email": email[0] if email else "Not found",
        "phone": phone[0] if phone else "Not found",
        "skills": found_skills,
        "profession": profession,
    }

# Function to generate improvement suggestions
def generate_suggestions(similarity_score, profession):
    suggestions = []
    
    if similarity_score < 40:
        suggestions.append("🚨 **Critical Improvements Needed**")
        suggestions.append("- Rewrite work experience to match job requirements")
        suggestions.append("- Include measurable achievements (e.g., 'Increased X by Y%')")
        
    elif similarity_score < 70:
        suggestions.append("⚠️ **Moderate Improvements Suggested**")
        suggestions.append("- Add more relevant skills from your profession")
        suggestions.append("- Quantify your accomplishments with numbers")
    
    # Profession-specific suggestions
    if profession == "Software Developer":
        suggestions.append("- Add GitHub projects and technical certifications")
    elif profession == "Data Scientist":
        suggestions.append("- Showcase ML projects and data visualization examples")
    
    suggestions.append("\n💡 **General Tips**")
    suggestions.append("- Use standard section headers: 'Experience', 'Education', 'Skills'")
    suggestions.append("- Keep resume to 1-2 pages maximum")
    suggestions.append("- Use bullet points instead of paragraphs")
    
    return "\n\n".join(suggestions)

# Function to match resume to job description
def match_resume_to_job(resume_text, job_description):
    if not resume_text.strip() or not job_description.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(vectors)[0][1]
    return round(similarity * 100, 2)

# Function to process resume file
def process_resume(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file)
    elif ext == ".docx":
        return extract_text_from_docx(file)
    else:
        return None

# Streamlit UI
def main():
    st.title("📄 ATS Resume Optimizer")
    st.markdown("_Get your resume past automated tracking systems_")

    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    job_description = st.text_area("Paste Job Description", height=200)

    if uploaded_file is not None:
        resume_text = process_resume(uploaded_file)
        
        if resume_text is None:
            st.error("❌ Unsupported file format. Please upload PDF or DOCX.")
        else:
            extracted_info = extract_info(resume_text)
            
            # Calculate ATS score
            similarity_score = match_resume_to_job(resume_text, job_description) if job_description.strip() else 0
            
            # Display results
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📝 Resume Analysis")
                st.write(f"**Profession:** {extracted_info['profession']}")
                st.write(f"**Skills Found:** {', '.join(extracted_info['skills']) if extracted_info['skills'] else 'None'}")
            
            with col2:
                st.subheader("🎯 ATS Score")
                if job_description.strip():
                    st.metric("Match Score", f"{similarity_score}%")
                    st.progress(similarity_score / 100)
                else:
                    st.warning("No job description provided for scoring")
            
            # Improvement suggestions
            if job_description.strip():
                st.subheader("🔧 Improvement Suggestions")
                if similarity_score < 70:
                    suggestions = generate_suggestions(
                        similarity_score, 
                        extracted_info['profession']
                    )
                    st.markdown(suggestions)
                else:
                    st.success("✅ Strong match! Your resume aligns well with the job description.")
            
            # Debug view (optional)
            with st.expander("🔧 Developer View"):
                st.text_area("Extracted Resume Text", resume_text[:5000], height=200)

if __name__ == "__main__":
    main()