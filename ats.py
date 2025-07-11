# import os
# import re
# import docx2txt
# import pdfminer.high_level
# import spacy
# import shutil
# import streamlit as st
# from pathlib import Path
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Load NLP model
# nlp = spacy.load("en_core_web_sm")

# # Define profession categories and related skills
# PROFESSION_CATEGORIES = {
#     "Software Developer": {"Python", "Java", "C++", "JavaScript", "React", "Node.js", "Django", "Flask"},
#     "Data Scientist": {"Python", "Machine Learning", "Deep Learning", "TensorFlow", "Pandas", "NumPy", "Data Science"},
#     "Marketing": {"SEO", "Digital Marketing", "Google Analytics", "Social Media", "Content Marketing"},
#     "Finance": {"Accounting", "Financial Analysis", "Excel", "Budgeting", "Investment", "Risk Management"},
#     "Human Resources": {"Recruitment", "HR Policies", "Payroll", "Employee Engagement", "Training"},
# }

# # Function to classify resume based on extracted skills
# def classify_resume(skills):
#     for profession, skill_set in PROFESSION_CATEGORIES.items():
#         if any(skill in skill_set for skill in skills):
#             return profession
#     return "Other"

# # Function to extract text from PDF
# def extract_text_from_pdf(pdf_path):
#     return pdfminer.high_level.extract_text(pdf_path)

# # Function to extract text from DOCX
# def extract_text_from_docx(docx_path):
#     return docx2txt.process(docx_path)

# # Function to extract key information
# def extract_info(text):
#     doc = nlp(text)

#     #  email
#     email = re.findall(r'\S+@\S+', text)

#     #  phone number
#     phone = re.findall(r'?\d{3}?[-.\s]?\d{3}[-.\s]?\d{4}', text)

#     #  skills
#     found_skills = {token.text for token in doc if token.text in sum(PROFESSION_CATEGORIES.values(), set())}

#     # Classify profession
#     profession = classify_resume(found_skills)

#     return {
#         "email": email[0] if email else "Not found",
#         "phone": phone[0] if phone else "Not found",
#         "skills": ", ".join(found_skills) if found_skills else "Not found",
#         "profession": profession,
#     }

# # Function to match resume to job description
# def match_resume_to_job(resume_text, job_description):
#     vectorizer = TfidfVectorizer()
#     vectors = vectorizer.fit_transform([resume_text, job_description])
#     similarity = cosine_similarity(vectors)[0][1]
#     return round(similarity * 100, 2)  # Return percentage

# # Function to process resume file
# def process_resume(file):
#     ext = os.path.splitext(file.name)[1].lower()
#     if ext == ".pdf":
#         text = extract_text_from_pdf(file)
#     elif ext == ".docx":
#         text = extract_text_from_docx(file)
#     else:
#         return "Unsupported file format"
#     return text

# # Function to save resume in categorized folders
# def save_resume(file, profession):
#     folder_path = Path(f"Resumes/{profession}")
#     folder_path.mkdir(parents=True, exist_ok=True)
#     file_path = folder_path / file.name

#     with open(file_path, "wb") as f:
#         f.write(file.read())

#     return str(file_path)

# # Streamlit UI
# st.title("ATS Resume Reader with Profession Categorization")

# uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
# job_description = st.text_area("Enter Job Description")

# if uploaded_file is not None:
#     resume_text = process_resume(uploaded_file)
#     if resume_text != "Unsupported file format":
#         extracted_info = extract_info(resume_text)
#         similarity_score = match_resume_to_job(resume_text, job_description) if job_description else "N/A"

#         # Save resume in categorized folder
#         resume_path = save_resume(uploaded_file, extracted_info["profession"])

#         st.subheader("Extracted Information")
#         st.write(f"Email: {extracted_info['email']}")
#         st.write(f"Phone: {extracted_info['phone']}")
#         st.write(f"Skills: {extracted_info['skills']}")
#         st.write(f"Profession: {extracted_info['profession']}")
#         st.write(f"Resume saved at: {resume_path}")
#     if job_description:
#             st.subheader("Job Matching Score")
#             st.write(f"Match Score: {similarity_score}%")
#     else:
#         st.error("Unsupported file format. Please upload a PDF or DOCX.")