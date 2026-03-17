import scrapy
import csv
from scrapy_project.items import JobItem
import os

class JobSpider(scrapy.Spider):
    name = "job_spider"

    def start_requests(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        links_file = os.path.join(base_dir, "data", "raw", "job_links.csv")

        with open(links_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            urls = [row["url"] for row in reader]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_job)

    def parse_job(self, response):
        item = JobItem()

        # Update selectors depending on the website structure
        item["job_title"] = response.css("h1::text").get(default="").strip()
        item["company_name"] = response.css("meta[name='application-name']::attr(content)").get(default="").strip()
        item["location"] = response.css(".location::text, .job-location::text").get(default="").strip()
        item["department"] = response.css(".department::text").get(default="").strip()
        item["employment_type"] = response.css(".employment-type::text").get(default="").strip()
        item["posted_date"] = response.css(".posted-date::text").get(default="").strip()
        item["job_url"] = response.url
        item["job_description"] = " ".join(response.css(".description *::text").getall()).strip()
        item["required_skills"] = ", ".join(response.css(".skills li::text, .requirements li::text").getall())
        item["experience_level"] = response.css(".experience-level::text").get(default="").strip()
        item["salary"] = response.css(".salary::text").get(default="").strip()

        yield item