from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import csv
import time


def start_driver():

    service = Service("msedgedriver.exe")

    driver = webdriver.Edge(service=service)

    driver.maximize_window()

    return driver
def open_page(driver):

    url = "https://boards.greenhouse.io/stripe"

    driver.get(url)

    time.sleep(5)


def collect_links(driver):

    job_links = []

    elements = driver.find_elements(By.TAG_NAME, "a")

    for element in elements:

        href = element.get_attribute("href")

        if href and "jobs" in href:

            job_links.append(href)

    unique_links = list(set(job_links))

    return unique_links


import os

def save_links(links):

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    file_path = os.path.join(base_dir, "data", "raw", "job_links.csv")

    with open(file_path, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow(["url"])

        for link in links:
            writer.writerow([link])

    print("File saved at:", file_path)


def main():

    driver = start_driver()

    open_page(driver)

    links = collect_links(driver)

    print("Total links:",len(links))

    save_links(links)

    driver.quit()


if __name__ == "__main__":

    main()