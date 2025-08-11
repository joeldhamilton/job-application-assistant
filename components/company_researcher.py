import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import time

# Try to import GoogleSearch, handle if not available
try:
    from serpapi.google_search import GoogleSearch
except ImportError:
    try:
        from serpapi import GoogleSearch
    except ImportError:
        GoogleSearch = None

class CompanyResearcher:
    def __init__(self, serpapi_key: Optional[str] = None):
        """
        Initialize company researcher with optional SerpAPI key
        If no key provided, will fall back to basic web scraping
        """
        self.serpapi_key = serpapi_key
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def research_company(self, company_name: str) -> str:
        """
        Research company information using multiple sources
        Returns a formatted string with company insights
        """
        company_info = {
            'basic_info': '',
            'recent_news': [],
            'company_culture': '',
            'size_and_industry': '',
            'recent_achievements': []
        }
        
        try:
            # Try SerpAPI first if available
            if self.serpapi_key:
                company_info.update(self._research_with_serpapi(company_name))
            else:
                # Fallback to basic web scraping
                company_info.update(self._research_with_scraping(company_name))
            
            return self._format_company_info(company_name, company_info)
            
        except Exception as e:
            return f"Limited company information available for {company_name}. Consider researching the company manually for better personalization."
    
    def _research_with_serpapi(self, company_name: str) -> Dict:
        """
        Research company using SerpAPI (more reliable and comprehensive)
        """
        info = {}
        
        try:
            # General company search
            search = GoogleSearch({
                "q": f"{company_name} company about",
                "api_key": self.serpapi_key,
                "num": 5
            })
            results = search.get_dict()
            
            if "organic_results" in results:
                # Extract basic information
                organic_results = results["organic_results"][:3]
                basic_info_parts = []
                
                for result in organic_results:
                    if "snippet" in result:
                        basic_info_parts.append(result["snippet"])
                
                info['basic_info'] = " ".join(basic_info_parts)
            
            # Recent news search
            news_search = GoogleSearch({
                "q": f"{company_name} news 2024",
                "api_key": self.serpapi_key,
                "tbm": "nws",
                "num": 3
            })
            news_results = news_search.get_dict()
            
            if "news_results" in news_results:
                info['recent_news'] = []
                for news in news_results["news_results"][:3]:
                    if "title" in news:
                        info['recent_news'].append(news["title"])
            
            # Company culture/careers search
            culture_search = GoogleSearch({
                "q": f"{company_name} company culture careers values",
                "api_key": self.serpapi_key,
                "num": 3
            })
            culture_results = culture_search.get_dict()
            
            if "organic_results" in culture_results:
                culture_parts = []
                for result in culture_results["organic_results"][:2]:
                    if "snippet" in result and ("culture" in result["snippet"].lower() or "values" in result["snippet"].lower()):
                        culture_parts.append(result["snippet"])
                
                info['company_culture'] = " ".join(culture_parts)
            
        except Exception as e:
            print(f"SerpAPI research error: {str(e)}")
        
        return info
    
    def _research_with_scraping(self, company_name: str) -> Dict:
        """
        Basic web scraping fallback (less reliable but free)
        """
        info = {}
        
        try:
            # Try to scrape company's main website
            search_url = f"https://www.google.com/search?q={company_name}+official+website"
            response = requests.get(search_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for website links in search results
                links = soup.find_all('a', href=True)
                company_website = None
                
                for link in links[:10]:
                    href = link.get('href', '')
                    if 'url?q=' in href:
                        actual_url = href.split('url?q=')[1].split('&')[0]
                        if company_name.lower().replace(' ', '') in actual_url.lower():
                            company_website = actual_url
                            break
                
                # If we found a website, try to scrape basic info
                if company_website:
                    info.update(self._scrape_company_website(company_website))
            
            # Add delay to be respectful
            time.sleep(1)
            
        except Exception as e:
            print(f"Web scraping error: {str(e)}")
        
        return info
    
    def _scrape_company_website(self, website_url: str) -> Dict:
        """
        Scrape basic information from company website
        """
        info = {}
        
        try:
            response = requests.get(website_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for about us or company description
                about_sections = soup.find_all(['p', 'div'], string=lambda text: text and 
                    any(keyword in text.lower() for keyword in ['about us', 'our company', 'our mission']))
                
                if about_sections:
                    # Get the parent containers of these sections
                    for section in about_sections[:2]:
                        parent = section.find_parent()
                        if parent:
                            text_content = parent.get_text(strip=True)
                            if len(text_content) > 50:
                                info['basic_info'] = text_content[:500]  # Limit length
                                break
                
                # Look for recent news or press releases
                news_links = soup.find_all('a', href=True, string=lambda text: text and 
                    any(keyword in text.lower() for keyword in ['news', 'press', 'announcement']))
                
                if news_links:
                    info['recent_news'] = [link.get_text(strip=True) for link in news_links[:3]]
                
        except Exception as e:
            print(f"Website scraping error: {str(e)}")
        
        return info
    
    def _format_company_info(self, company_name: str, info: Dict) -> str:
        """
        Format the researched company information into a readable string
        """
        formatted_info = f"Company Research: {company_name}\n\n"
        
        if info.get('basic_info'):
            formatted_info += f"About the Company:\n{info['basic_info'][:300]}...\n\n"
        
        if info.get('recent_news') and len(info['recent_news']) > 0:
            formatted_info += "Recent News/Updates:\n"
            for news in info['recent_news'][:3]:
                formatted_info += f"• {news}\n"
            formatted_info += "\n"
        
        if info.get('company_culture'):
            formatted_info += f"Company Culture/Values:\n{info['company_culture'][:200]}...\n\n"
        
        if info.get('size_and_industry'):
            formatted_info += f"Industry & Size:\n{info['size_and_industry']}\n\n"
        
        if info.get('recent_achievements') and len(info['recent_achievements']) > 0:
            formatted_info += "Recent Achievements:\n"
            for achievement in info['recent_achievements'][:2]:
                formatted_info += f"• {achievement}\n"
        
        # Add a note about using this information
        formatted_info += "\n[Use this information to show genuine interest and knowledge about the company in your cover letter]"
        
        return formatted_info
    
    def get_company_linkedin_info(self, company_name: str) -> Optional[str]:
        """
        Try to find company LinkedIn page information
        """
        if not self.serpapi_key:
            return None
        
        try:
            search = GoogleSearch({
                "q": f"{company_name} site:linkedin.com/company",
                "api_key": self.serpapi_key,
                "num": 1
            })
            results = search.get_dict()
            
            if "organic_results" in results and len(results["organic_results"]) > 0:
                result = results["organic_results"][0]
                if "snippet" in result:
                    return result["snippet"]
            
        except Exception as e:
            print(f"LinkedIn search error: {str(e)}")
        
        return None
    
    def research_industry_trends(self, industry: str) -> str:
        """
        Research current trends in the company's industry
        """
        if not self.serpapi_key:
            return f"Manual research recommended for {industry} industry trends."
        
        try:
            search = GoogleSearch({
                "q": f"{industry} trends 2024 outlook",
                "api_key": self.serpapi_key,
                "num": 3
            })
            results = search.get_dict()
            
            if "organic_results" in results:
                trend_info = []
                for result in results["organic_results"][:3]:
                    if "snippet" in result:
                        trend_info.append(result["snippet"])
                
                return f"Industry Trends in {industry}:\n" + "\n".join(trend_info[:2])
            
        except Exception as e:
            print(f"Industry research error: {str(e)}")
        
        return f"Manual research recommended for {industry} industry trends."