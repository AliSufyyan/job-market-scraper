import scrapy
import pandas as pd
import os

class JobSpider(scrapy.Spider):
    name = "job_spider"

    def start_requests(self):
        # Path logic: Go up to root, then into data/raw
        # Use absolute path to avoid "File Not Found" errors
        base_path = os.getcwd() 
        csv_path = os.path.join(base_path, '..', 'data', 'raw', 'job_links.csv')
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            for url in df['Job URL']:
                yield scrapy.Request(url=url, callback=self.parse)
        else:
            self.logger.error(f"❌ ERROR: Cannot find {csv_path}")

    def parse(self, response):
        # 1. Broad Selector: Look for ANY large text block (p, li, div) 
        # This is more reliable for custom sites like Airbnb
        all_text = response.css('div.job-description-content ::text, div#content ::text, .main-content ::text, section ::text').getall()
        description = " ".join([t.strip() for t in all_text if len(t.strip()) > 5]).strip()

        # 2. Safety Check: If still empty, grab the whole body text
        if len(description) < 100:
            description = " ".join(response.xpath('//body//text()').getall()).strip()

        # 3. Skill Extraction (Requirement 2.8)
        # We define a list of common tech keywords to "find" in the text
        skills_bank = ['python', 'sql', 'aws', 'java', 'react', 'spark', 'kubernetes', 'tableau', 'excel', 'machine learning']
        found_skills = [s for s in skills_bank if s in description.lower()]

        yield {
            'job_title': response.css('h1::text').get(default='N/A').strip(),
            'company_name': 'Airbnb',
            'location': response.css('span.job-location::text, .location::text').get(default='Global').strip(),
            'department': 'Technology',
            'employment_type': 'Full-time',
            'posted_date': '2026-03-18',
            'job_url': response.url,
            'job_description': description[:1000], # Grab first 1000 characters
            'required_skills': ", ".join(found_skills) if found_skills else "General Tech"
        }