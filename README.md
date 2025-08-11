# 🚀 Autonomous Job Application Assistant

An AI-powered tool that helps you apply to jobs with tailored resumes, cover letters, and automated tracking. Built with LangChain, GPT, Streamlit, and various APIs for a complete job application workflow.

## ✨ Features

- **Resume Analysis**: Upload PDF, DOCX, or TXT resumes and get intelligent parsing
- **Job Matching**: Analyze how well your resume matches job descriptions
- **AI Cover Letters**: Generate tailored cover letters using GPT-3.5/4
- **Company Research**: Automatic company research using SerpAPI and web scraping
- **Email Integration**: Send applications directly via email
- **Job Tracking**: Track applications in Airtable with status updates
- **Bullet Point Matching**: Extract and highlight relevant resume bullets for each job

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/LLM**: LangChain + OpenAI GPT
- **Document Processing**: PyPDF2, python-docx
- **Web Scraping**: BeautifulSoup4, requests
- **Company Research**: SerpAPI (optional)
- **Email**: SMTP with SSL
- **Job Tracking**: Airtable API
- **Environment**: python-dotenv

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd job-application-assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your API keys and configurations:
   - **OpenAI API Key** (required): Get from https://platform.openai.com/
   - **Email credentials** (optional): For sending applications
   - **Airtable API** (optional): For job tracking
   - **SerpAPI Key** (optional): For enhanced company research

## 🚀 Usage

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Upload your resume**: Support for PDF, DOCX, and TXT formats

3. **Enter job description**: Paste the job posting you're applying for

4. **Generate materials**:
   - Analyze resume-job match
   - Generate tailored cover letter
   - Research company information (if SerpAPI configured)

5. **Send application**: 
   - Configure email settings
   - Send directly through the app
   - Track in Airtable

## 🔧 Configuration

### Required API Keys

- **OpenAI API Key**: For AI-powered cover letter generation
  - Get from: https://platform.openai.com/
  - Cost: ~$0.01-0.05 per cover letter

### Optional Integrations

- **SerpAPI** (Enhanced company research):
  - Get from: https://serpapi.com/
  - Free tier: 100 searches/month

- **Airtable** (Job tracking):
  - Get API key from: https://airtable.com/account
  - Create a base with "Job Applications" table

### Email Configuration

For Gmail, use an App Password instead of your regular password:
1. Enable 2-factor authentication
2. Generate App Password: https://support.google.com/accounts/answer/185833
3. Use the App Password in your `.env` file

## 📊 Airtable Setup

Create a table called "Job Applications" with these fields:

| Field Name | Field Type |
|------------|------------|
| Company | Single line text |
| Position | Single line text |
| Status | Single select (Applied, Interview, Rejected, Offer) |
| Application Date | Date |
| Job Description URL | URL |
| Notes | Long text |
| Salary Range | Single line text |
| Contact Person | Single line text |
| Follow-up Date | Date |

## 📁 Project Structure

```
job-application-assistant/
├── app.py                          # Main Streamlit application
├── components/                     # Core modules
│   ├── __init__.py
│   ├── resume_parser.py           # Resume text extraction
│   ├── cover_letter_generator.py  # AI cover letter generation
│   ├── email_sender.py           # Email functionality
│   ├── airtable_tracker.py       # Job tracking
│   └── company_researcher.py     # Company research
├── requirements.txt              # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                   # This file
```

## 🤖 How It Works

1. **Resume Parsing**: Extracts text and identifies key sections (experience, skills, education)

2. **Job Analysis**: Uses GPT to analyze resume-job match and extract relevant bullet points

3. **Cover Letter Generation**: 
   - Identifies top relevant achievements from resume
   - Incorporates company research (if available)
   - Generates personalized, professional cover letter

4. **Company Research**: 
   - Uses SerpAPI for comprehensive company information
   - Falls back to web scraping if no API key provided
   - Finds recent news, company culture, and values

5. **Application Tracking**: 
   - Stores all applications in Airtable
   - Tracks status updates and follow-up dates
   - Generates application summaries

## 💡 Tips for Best Results

1. **Resume Quality**: Use a well-formatted resume with clear sections
2. **Job Description**: Copy the complete job posting for better analysis  
3. **Company Name**: Provide accurate company names for better research
4. **Review Output**: Always review and customize generated cover letters
5. **API Limits**: Be mindful of OpenAI and SerpAPI usage limits

## ⚠️ Important Notes

- **Review Generated Content**: Always review AI-generated cover letters before sending
- **API Costs**: OpenAI API usage incurs costs (~$0.01-0.05 per cover letter)
- **Email Security**: Use App Passwords, not regular passwords for email
- **Rate Limits**: Respect rate limits for web scraping and APIs

## 🔒 Security

- Never commit API keys to version control
- Use environment variables for sensitive data
- Enable 2FA on all service accounts
- Use App Passwords for email authentication

## 🛟 Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**: Check your `.env` file and API key
2. **Email sending fails**: Verify SMTP settings and use App Password
3. **Airtable connection error**: Confirm API key and base ID
4. **Resume parsing issues**: Ensure file is not password-protected

### Getting Help

- Check the `.env.example` file for proper configuration format
- Verify all required dependencies are installed
- Test API connections using the built-in test functions

## 🚀 Future Enhancements

- [ ] Support for more file formats (Pages, Google Docs)
- [ ] Integration with job boards (LinkedIn, Indeed)
- [ ] Resume optimization suggestions
- [ ] Interview preparation materials
- [ ] Salary negotiation assistance
- [ ] Application analytics and insights

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Disclaimer**: This tool assists with job applications but human review is always recommended. Be mindful of API costs and usage limits.