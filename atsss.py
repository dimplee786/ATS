# import os
# import re
# import docx2txt
# import pdfminer.high_level
# import spacy
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

#     # Extract email
#     email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)

#     # Extract phone number
#     phone = re.findall(r'\b\d{12}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text)

#     # Extract skills
#     all_skills = set.union(*PROFESSION_CATEGORIES.values())  # Merge all skill sets
#     found_skills = {token.text for token in doc if token.text in all_skills}

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
#     if not resume_text.strip() or not job_description.strip():
#         return 0.0
#     vectorizer = TfidfVectorizer(stop_words='english')
#     vectors = vectorizer.fit_transform([resume_text, job_description])
#     similarity = cosine_similarity(vectors)[0][1]
#     return round(similarity * 100, 2)  # Return percentage

# # Function to process resume file
# def process_resume(file):
#     ext = os.path.splitext(file.name)[1].lower()
#     if ext == ".pdf":
#         return extract_text_from_pdf(file)
#     elif ext == ".docx":
#         return extract_text_from_docx(file)
#     else:
#         return None

# # Function to save resume in categorized folders
# def save_resume(file, profession):
#     folder_path = Path(f"Resumes/{profession}")
#     folder_path.mkdir(parents=True, exist_ok=True)
#     file_path = folder_path / file.name
    
#     with open(file_path, "wb") as f:
#         f.write(file.getbuffer())  # Use getbuffer() for in-memory files
    
#     return str(file_path)

# # Streamlit UI
# def main():
#     st.title("ATS Resume Reader with Profession Categorization")

#     uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
#     job_description = st.text_area("Enter Job Description")

#     if uploaded_file is not None:
#         resume_text = process_resume(uploaded_file)
        
#         if resume_text is None:
#             st.error("Unsupported file format. Please upload a PDF or DOCX.")
#         else:
#             extracted_info = extract_info(resume_text)
            
#             # Calculate ATS score only if job description is provided
#             if job_description.strip():
#                 similarity_score = match_resume_to_job(resume_text, job_description)
#             else:
#                 similarity_score = "N/A (No Job Description Provided)"

#             # Save resume in categorized folder
#             resume_path = save_resume(uploaded_file, extracted_info["profession"])

#             # Display extracted information
#             st.subheader("Extracted Information")
#             st.write(f"**Email:** {extracted_info['email']}")
#             st.write(f"**Phone:** {extracted_info['phone']}")
#             st.write(f"**Skills:** {extracted_info['skills']}")
#             st.write(f"**Profession Category:** {extracted_info['profession']}")
#             st.write(f"**Resume saved at:** {resume_path}")

#             # Display ATS score if job description exists
#             if job_description.strip():
#                 st.subheader("ATS Matching Score")
#                 st.write(f"**Match Score:** {similarity_score}%")
#                 # Visual representation
#                 st.progress(similarity_score / 100)
                
#                 # Interpretation
#                 if similarity_score >= 70:
#                     st.success("Strong Match! This resume is well-aligned with the job description.")
#                 elif similarity_score >= 40:
#                     st.warning("Moderate Match. Consider reviewing for potential fit.")
#                 else:
#                     st.error("Weak Match. This resume may not be a good fit for the role.")

# if __name__ == "__main__":
#     main()