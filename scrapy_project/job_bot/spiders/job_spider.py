import scrapy
import pandas as pd
import os

class JobSpider(scrapy.Spider):
    name = "job_spider"

    # Read links from CSV
    def start_requests(self):
        csv_path = os.path.join(os.getcwd(), 'data', 'raw', 'job_links.csv')
        if not os.path.exists(csv_path):
            self.logger.error(f"❌ ERROR: Cannot find {csv_path}")
            return

        links = pd.read_csv(csv_path)['Job URL'].tolist()
        for url in links:
            yield scrapy.Request(url=url, callback=self.parse_job)

    # Parse each job page
    def parse_job(self, response):
        # Adjust the selectors below to match Airbnb job pages
        title = response.css('h1::text').get(default='N/A').strip()
        location = response.css('span.job-location::text').get(default='N/A').strip()
        posted_date = response.css('span.posted-date::text').get(default='N/A').strip()

        yield {
            'Job Title': title,
            'Location': location,
            'Posted Date': posted_date,
            'Job URL': response.url
        }