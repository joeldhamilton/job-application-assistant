import streamlit as st
import os
from dotenv import load_dotenv
from components.resume_parser import ResumeParser
from components.cover_letter_generator import CoverLetterGenerator
from components.email_sender import EmailSender
from components.airtable_tracker import AirtableTracker
from components.company_researcher import CompanyResearcher

load_dotenv()

st.set_page_config(
    page_title="Job Application Assistant",
    page_icon="💼",
    layout="wide"
)

st.title("🚀 Autonomous Job Application Assistant")
st.markdown("Upload your resume and job description to get tailored application materials!")

# Sidebar for configuration
st.sidebar.header("Configuration")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
airtable_api_key = st.sidebar.text_input("Airtable API Key", type="password", value=os.getenv("AIRTABLE_API_KEY", ""))
serpapi_key = st.sidebar.text_input("SerpAPI Key (Optional)", type="password", value=os.getenv("SERPAPI_KEY", ""))

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📄 Upload Your Resume")
    resume_file = st.file_uploader(
        "Choose your resume file",
        type=['pdf', 'docx', 'txt'],
        help="Upload your resume in PDF, DOCX, or TXT format"
    )
    
    if resume_file:
        st.success(f"Resume uploaded: {resume_file.name}")

with col2:
    st.header("💼 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Copy and paste the job description you're applying for..."
    )
    
    company_name = st.text_input("Company Name (Optional)", placeholder="e.g., Google, Microsoft")
    job_title = st.text_input("Job Title", placeholder="e.g., Software Engineer, Data Scientist")

# Action buttons
st.header("🎯 Generate Application Materials")

col3, col4, col5 = st.columns([1, 1, 1])

with col3:
    if st.button("🔍 Analyze Resume & Job Match", use_container_width=True):
        if resume_file and job_description:
            with st.spinner("Analyzing your resume against the job description..."):
                parser = ResumeParser()
                resume_text = parser.extract_text(resume_file)
                
                generator = CoverLetterGenerator(openai_api_key)
                match_analysis = generator.analyze_job_match(resume_text, job_description)
                
                st.subheader("📊 Match Analysis")
                st.write(match_analysis)
        else:
            st.error("Please upload a resume and enter a job description first!")

with col4:
    if st.button("✍️ Generate Cover Letter", use_container_width=True):
        if resume_file and job_description:
            with st.spinner("Generating tailored cover letter..."):
                parser = ResumeParser()
                resume_text = parser.extract_text(resume_file)
                
                generator = CoverLetterGenerator(openai_api_key)
                
                # Optional company research
                company_info = ""
                if company_name and serpapi_key:
                    researcher = CompanyResearcher(serpapi_key)
                    company_info = researcher.research_company(company_name)
                
                cover_letter = generator.generate_cover_letter(
                    resume_text, 
                    job_description, 
                    company_name or "the company",
                    company_info
                )
                
                st.subheader("📝 Generated Cover Letter")
                st.text_area("Your tailored cover letter:", cover_letter, height=400)
                
                # Download button
                st.download_button(
                    label="📥 Download Cover Letter",
                    data=cover_letter,
                    file_name=f"cover_letter_{job_title.replace(' ', '_').lower()}.txt",
                    mime="text/plain"
                )
        else:
            st.error("Please upload a resume and enter a job description first!")

with col5:
    if st.button("📧 Send Application", use_container_width=True):
        st.info("Email sending functionality - configure your email settings in the sidebar first!")

# Email configuration (expandable section)
with st.expander("📧 Email Configuration"):
    email_address = st.text_input("Your Email Address", value=os.getenv("EMAIL_ADDRESS", ""))
    email_password = st.text_input("Email Password/App Password", type="password", value=os.getenv("EMAIL_PASSWORD", ""))
    smtp_server = st.text_input("SMTP Server", value=os.getenv("SMTP_SERVER", "smtp.gmail.com"))
    smtp_port = st.number_input("SMTP Port", value=int(os.getenv("SMTP_PORT", "587")))
    
    recipient_email = st.text_input("Recipient Email (HR/Hiring Manager)")
    email_subject = st.text_input("Email Subject", value=f"Application for {job_title} Position")

# Airtable tracking
with st.expander("📊 Job Tracking"):
    if st.button("📝 Save to Airtable"):
        if airtable_api_key and company_name and job_title:
            tracker = AirtableTracker(airtable_api_key)
            result = tracker.add_job_application({
                'Company': company_name,
                'Position': job_title,
                'Status': 'Applied',
                'Application Date': str(st.date_input("Application Date"))
            })
            if result:
                st.success("Job application saved to Airtable!")
            else:
                st.error("Failed to save to Airtable. Check your API key and base configuration.")
        else:
            st.error("Please provide Airtable API key, company name, and job title.")

# Footer
st.markdown("---")
st.markdown("💡 **Tips**: Make sure to review and customize the generated cover letter before sending!")