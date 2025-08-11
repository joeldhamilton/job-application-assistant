from airtable import Airtable
from datetime import datetime
from typing import Dict, List, Optional

class AirtableTracker:
    def __init__(self, api_key: str, base_id: str = None, table_name: str = "Job Applications"):
        """
        Initialize Airtable tracker for job applications
        
        Args:
            api_key: Airtable API key
            base_id: Airtable base ID (you'll need to create this)
            table_name: Name of the table to store job applications
        """
        self.api_key = api_key
        self.base_id = base_id
        self.table_name = table_name
        
        # Initialize Airtable connection if base_id is provided
        if base_id:
            self.airtable = Airtable(base_id, table_name, api_key)
        else:
            self.airtable = None
    
    def setup_base_instructions(self) -> str:
        """
        Return instructions for setting up Airtable base
        """
        return """
        To use Airtable tracking, please:
        
        1. Go to https://airtable.com and create a new base
        2. Create a table called 'Job Applications' with these fields:
           - Company (Single line text)
           - Position (Single line text) 
           - Status (Single select: Applied, Interview Scheduled, Rejected, Offer)
           - Application Date (Date)
           - Job Description URL (URL)
           - Notes (Long text)
           - Salary Range (Single line text)
           - Contact Person (Single line text)
           - Follow-up Date (Date)
        3. Get your Base ID from the API documentation
        4. Update the base_id in your configuration
        """
    
    def add_job_application(self, application_data: Dict) -> bool:
        """
        Add a new job application record to Airtable
        
        Args:
            application_data: Dictionary with application details
            
        Expected fields:
            - Company (required)
            - Position (required)
            - Status (default: 'Applied')
            - Application Date (default: today)
            - Job Description URL (optional)
            - Notes (optional)
            - Salary Range (optional)
            - Contact Person (optional)
        """
        if not self.airtable:
            print("Airtable not initialized. Please set base_id.")
            return False
        
        try:
            # Set defaults
            record_data = {
                'Company': application_data.get('Company', ''),
                'Position': application_data.get('Position', ''),
                'Status': application_data.get('Status', 'Applied'),
                'Application Date': application_data.get('Application Date', datetime.now().strftime('%Y-%m-%d')),
                'Job Description URL': application_data.get('Job Description URL', ''),
                'Notes': application_data.get('Notes', ''),
                'Salary Range': application_data.get('Salary Range', ''),
                'Contact Person': application_data.get('Contact Person', ''),
            }
            
            # Add follow-up date (1 week from application date)
            if 'Follow-up Date' not in application_data:
                from datetime import datetime, timedelta
                follow_up = datetime.now() + timedelta(days=7)
                record_data['Follow-up Date'] = follow_up.strftime('%Y-%m-%d')
            
            result = self.airtable.insert(record_data)
            return True
            
        except Exception as e:
            print(f"Error adding job application to Airtable: {str(e)}")
            return False
    
    def update_application_status(self, record_id: str, new_status: str, notes: str = "") -> bool:
        """
        Update the status of a job application
        
        Args:
            record_id: Airtable record ID
            new_status: New status (Applied, Interview Scheduled, Rejected, Offer)
            notes: Additional notes
        """
        if not self.airtable:
            return False
        
        try:
            update_data = {'Status': new_status}
            if notes:
                update_data['Notes'] = notes
            
            self.airtable.update(record_id, update_data)
            return True
            
        except Exception as e:
            print(f"Error updating application status: {str(e)}")
            return False
    
    def get_all_applications(self) -> List[Dict]:
        """
        Get all job applications from Airtable
        """
        if not self.airtable:
            return []
        
        try:
            records = self.airtable.get_all()
            return [record['fields'] for record in records]
            
        except Exception as e:
            print(f"Error retrieving applications: {str(e)}")
            return []
    
    def get_applications_by_status(self, status: str) -> List[Dict]:
        """
        Get applications filtered by status
        """
        if not self.airtable:
            return []
        
        try:
            formula = f"{{Status}} = '{status}'"
            records = self.airtable.get_all(formula=formula)
            return [record['fields'] for record in records]
            
        except Exception as e:
            print(f"Error retrieving applications by status: {str(e)}")
            return []
    
    def get_applications_needing_followup(self) -> List[Dict]:
        """
        Get applications that need follow-up (follow-up date is today or past)
        """
        if not self.airtable:
            return []
        
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            formula = f"{{Follow-up Date}} <= '{today}'"
            records = self.airtable.get_all(formula=formula)
            return [record['fields'] for record in records]
            
        except Exception as e:
            print(f"Error retrieving follow-up applications: {str(e)}")
            return []
    
    def generate_application_summary(self) -> Dict:
        """
        Generate a summary of all applications
        """
        if not self.airtable:
            return {}
        
        applications = self.get_all_applications()
        
        if not applications:
            return {}
        
        summary = {
            'total_applications': len(applications),
            'status_breakdown': {},
            'companies_applied_to': set(),
            'recent_applications': []
        }
        
        for app in applications:
            # Count by status
            status = app.get('Status', 'Unknown')
            summary['status_breakdown'][status] = summary['status_breakdown'].get(status, 0) + 1
            
            # Track companies
            company = app.get('Company', '')
            if company:
                summary['companies_applied_to'].add(company)
            
            # Recent applications (last 7 days)
            app_date = app.get('Application Date', '')
            if app_date:
                try:
                    app_datetime = datetime.strptime(app_date, '%Y-%m-%d')
                    if (datetime.now() - app_datetime).days <= 7:
                        summary['recent_applications'].append(app)
                except:
                    pass
        
        summary['companies_applied_to'] = list(summary['companies_applied_to'])
        
        return summary
    
    def test_connection(self) -> bool:
        """
        Test the Airtable connection
        """
        if not self.airtable:
            return False
        
        try:
            # Try to get the first record
            self.airtable.get_all(max_records=1)
            return True
            
        except Exception as e:
            print(f"Airtable connection test failed: {str(e)}")
            return False