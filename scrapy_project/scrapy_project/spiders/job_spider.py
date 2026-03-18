import scrapy
import os
from scrapy_project.items import JobItem


class JobSpider(scrapy.Spider):

    name = "jobs"


    def start_requests(self):

        import csv

        # Construct absolute path to job_links.csv
        spider_dir = os.path.dirname(os.path.abspath(__file__))
        job_market_dir = os.path.dirname(os.path.dirname(os.path.dirname(spider_dir)))
        links_file = os.path.join(job_market_dir, "data", "raw", "job_links.csv")

        with open(links_file, newline="", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            for row in reader:

                url = row["url"]

                yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        item = JobItem()

        item["job_title"] = response.css("h1::text").get()

        item["company_name"] = "Stripe"

        item["location"] = response.css(".location::text").get()

        item["department"] = response.css(".department::text").get()

        item["employment_type"] = response.css(".employment-type::text").get()

        item["posted_date"] = response.css("time::text").get()

        item["job_url"] = response.url

        description = response.css("p::text").getall()

        item["description"] = " ".join(description)

        item["skills"] = None

        yield item