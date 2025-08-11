import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List
import os

class EmailSender:
    def __init__(self, email_address: str, password: str, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        self.email_address = email_address
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_application_email(self, 
                             recipient_email: str,
                             subject: str,
                             cover_letter: str,
                             applicant_name: str,
                             position: str,
                             company_name: str,
                             attachments: Optional[List[str]] = None) -> bool:
        """
        Send a job application email with cover letter and attachments
        
        Args:
            recipient_email: HR or hiring manager email
            subject: Email subject line
            cover_letter: Generated cover letter content
            applicant_name: Name of the applicant
            position: Job position title
            company_name: Company name
            attachments: List of file paths to attach (resume, portfolio, etc.)
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Create email body
            email_body = self._create_email_body(cover_letter, applicant_name, position, company_name)
            msg.attach(MIMEText(email_body, 'plain'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        self._attach_file(msg, file_path)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.password)
                text = msg.as_string()
                server.sendmail(self.email_address, recipient_email, text)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def _create_email_body(self, cover_letter: str, applicant_name: str, position: str, company_name: str) -> str:
        """
        Create the email body with the cover letter
        """
        # Clean up the cover letter (remove placeholder brackets if they exist)
        clean_cover_letter = cover_letter.replace('[Your Name]', applicant_name)
        clean_cover_letter = clean_cover_letter.replace('[Company Name]', company_name)
        clean_cover_letter = clean_cover_letter.replace('[Position]', position)
        
        email_body = f"""Dear Hiring Manager,

I hope this email finds you well. I am writing to express my strong interest in the {position} position at {company_name}.

{clean_cover_letter}

I have attached my resume for your review. I would welcome the opportunity to discuss how my background and enthusiasm can contribute to your team.

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,
{applicant_name}

---
This application was generated using an AI-powered job application assistant to ensure optimal matching and personalization.
"""
        
        return email_body
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """
        Attach a file to the email message
        """
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            filename = os.path.basename(file_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            
            msg.attach(part)
            
        except Exception as e:
            print(f"Error attaching file {file_path}: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Test the email connection and credentials
        """
        try:
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.password)
            
            return True
            
        except Exception as e:
            print(f"Email connection test failed: {str(e)}")
            return False
    
    def send_simple_email(self, recipient_email: str, subject: str, body: str) -> bool:
        """
        Send a simple text email
        """
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.email_address
            msg['To'] = recipient_email
            
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email_address, self.password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Error sending simple email: {str(e)}")
            return False