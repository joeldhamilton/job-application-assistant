from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import re
from typing import List, Dict

class CoverLetterGenerator:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            api_key=api_key,
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )
    
    def analyze_job_match(self, resume_text: str, job_description: str) -> str:
        """
        Analyze how well the resume matches the job description
        """
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert recruiter and career advisor. 
            Analyze how well the candidate's resume matches the job description.
            
            Provide:
            1. Match percentage (0-100%)
            2. Top 5 matching qualifications
            3. Top 3 gaps or areas for improvement
            4. 3 specific bullet points from the resume that should be highlighted
            
            Be constructive and specific in your analysis."""),
            HumanMessage(content=f"""
            RESUME:
            {resume_text}
            
            JOB DESCRIPTION:
            {job_description}
            
            Please analyze the match between this resume and job description.
            """)
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        return response.content
    
    def extract_resume_bullets(self, resume_text: str, job_description: str) -> List[str]:
        """
        Extract and identify the most relevant resume bullet points for the job
        """
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert at identifying the most relevant 
            experience bullets from a resume for a specific job application.
            
            Extract 5-8 of the most relevant bullet points from the resume that align 
            with the job description. Focus on:
            - Quantifiable achievements
            - Relevant technical skills
            - Leadership experience
            - Projects that match the job requirements
            
            Return only the bullet points, one per line, starting with •"""),
            HumanMessage(content=f"""
            RESUME:
            {resume_text}
            
            JOB DESCRIPTION:
            {job_description}
            
            Extract the most relevant bullet points:
            """)
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        
        # Extract bullet points from response
        bullets = []
        for line in response.content.split('\n'):
            line = line.strip()
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                bullets.append(line)
        
        return bullets
    
    def generate_cover_letter(self, resume_text: str, job_description: str, 
                            company_name: str, company_info: str = "") -> str:
        """
        Generate a tailored cover letter using LangChain and GPT
        """
        # First, get relevant bullet points
        relevant_bullets = self.extract_resume_bullets(resume_text, job_description)
        bullets_text = '\n'.join(relevant_bullets[:5])  # Use top 5 bullets
        
        company_context = f"\n\nCOMPANY RESEARCH:\n{company_info}" if company_info else ""
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert cover letter writer who creates 
            compelling, personalized cover letters that get results.
            
            Write a professional cover letter that:
            1. Has a strong, engaging opening paragraph
            2. Incorporates specific achievements from the resume
            3. Addresses the job requirements directly
            4. Shows genuine interest in the company
            5. Has a confident, professional closing
            6. Is 3-4 paragraphs long
            7. Uses active voice and quantifiable achievements
            
            Do NOT use generic templates. Make it personal and specific.
            Include the candidate's name as [Your Name] and company details as provided."""),
            HumanMessage(content=f"""
            JOB DESCRIPTION:
            {job_description}
            
            COMPANY: {company_name}
            {company_context}
            
            CANDIDATE'S RELEVANT ACHIEVEMENTS:
            {bullets_text}
            
            FULL RESUME CONTEXT:
            {resume_text}
            
            Write a compelling cover letter for this application:
            """)
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        return self._format_cover_letter(response.content)
    
    def _format_cover_letter(self, cover_letter: str) -> str:
        """
        Format the cover letter with proper structure
        """
        # Add header if not present
        if not cover_letter.strip().startswith('[Your Name]') and not cover_letter.strip().startswith('Dear'):
            header = """[Your Name]
[Your Address]
[Your Email]
[Your Phone Number]
[Date]

[Hiring Manager's Name]
[Company Name]
[Company Address]

"""
            cover_letter = header + cover_letter
        
        # Ensure proper closing if not present
        if not any(closing in cover_letter.lower() for closing in ['sincerely', 'best regards', 'thank you']):
            cover_letter += "\n\nSincerely,\n[Your Name]"
        
        return cover_letter.strip()
    
    def customize_for_company(self, base_cover_letter: str, company_info: str) -> str:
        """
        Further customize the cover letter with company-specific information
        """
        if not company_info:
            return base_cover_letter
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are tasked with enhancing a cover letter 
            by incorporating specific company information. 
            
            Add 1-2 sentences that show you've researched the company and explain 
            why you're specifically interested in working there. 
            
            Integrate this naturally into the existing cover letter without making it longer than 4 paragraphs."""),
            HumanMessage(content=f"""
            CURRENT COVER LETTER:
            {base_cover_letter}
            
            COMPANY INFORMATION:
            {company_info}
            
            Enhance the cover letter with this company information:
            """)
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        return response.content