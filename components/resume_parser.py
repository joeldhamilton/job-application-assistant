import PyPDF2
import docx
import io
from typing import Union, BinaryIO

class ResumeParser:
    def __init__(self):
        self.supported_formats = ['pdf', 'docx', 'txt']
    
    def extract_text(self, file) -> str:
        """
        Extract text from uploaded resume file
        Supports PDF, DOCX, and TXT formats
        """
        try:
            file_extension = file.name.split('.')[-1].lower()
            
            if file_extension == 'pdf':
                return self._extract_from_pdf(file)
            elif file_extension == 'docx':
                return self._extract_from_docx(file)
            elif file_extension == 'txt':
                return self._extract_from_txt(file)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
                
        except Exception as e:
            raise Exception(f"Error extracting text from resume: {str(e)}")
    
    def _extract_from_pdf(self, file) -> str:
        """Extract text from PDF file"""
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    def _extract_from_docx(self, file) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(file)
        text = ""
        
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text.strip()
    
    def _extract_from_txt(self, file) -> str:
        """Extract text from TXT file"""
        return file.read().decode('utf-8')
    
    def extract_key_sections(self, resume_text: str) -> dict:
        """
        Extract key sections from resume text using simple keyword matching
        Returns a dictionary with identified sections
        """
        sections = {
            'contact': '',
            'summary': '',
            'experience': '',
            'education': '',
            'skills': '',
            'projects': ''
        }
        
        lines = resume_text.split('\n')
        current_section = None
        section_content = []
        
        # Keywords to identify sections
        section_keywords = {
            'contact': ['contact', 'phone', 'email', 'address'],
            'summary': ['summary', 'objective', 'profile', 'about'],
            'experience': ['experience', 'employment', 'work history', 'professional'],
            'education': ['education', 'degree', 'university', 'college', 'school'],
            'skills': ['skills', 'technical', 'competencies', 'technologies'],
            'projects': ['projects', 'portfolio', 'achievements']
        }
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line indicates a new section
            section_found = None
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords) and len(line.strip()) < 50:
                    section_found = section
                    break
            
            if section_found:
                # Save previous section content
                if current_section and section_content:
                    sections[current_section] = '\n'.join(section_content)
                
                # Start new section
                current_section = section_found
                section_content = []
            elif current_section and line.strip():
                section_content.append(line)
        
        # Save the last section
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content)
        
        return sections
    
    def extract_skills_keywords(self, resume_text: str) -> list:
        """
        Extract potential skill keywords from resume
        """
        # Common technical skills and keywords
        common_skills = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mysql', 'postgresql',
            'mongodb', 'aws', 'azure', 'docker', 'kubernetes', 'git', 'html', 'css',
            'machine learning', 'data science', 'tensorflow', 'pytorch', 'pandas', 'numpy',
            'api', 'rest', 'graphql', 'agile', 'scrum', 'ci/cd', 'devops', 'linux',
            'project management', 'leadership', 'communication', 'problem solving'
        ]
        
        resume_lower = resume_text.lower()
        found_skills = []
        
        for skill in common_skills:
            if skill in resume_lower:
                found_skills.append(skill.title())
        
        return found_skills