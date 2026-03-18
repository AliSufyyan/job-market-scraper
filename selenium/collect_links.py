import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By


def run_selenium():
    print("🚀 Starting Selenium for Airbnb...")

    # Path to local Edge driver
    driver_path = os.path.join(os.path.dirname(__file__), "msedgedriver.exe")

    service = Service(driver_path)
    driver = webdriver.Edge(service=service)

    url = "https://careers.airbnb.com/positions/"
    driver.get(url)

    time.sleep(5)  # wait for page load

    # Scroll to load dynamic jobs
    print("Scrolling to load dynamic content...")
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Extract job links
    links = []
    elements = driver.find_elements(By.TAG_NAME, "a")

    for el in elements:
        href = el.get_attribute("href")
        text = el.text.lower()

        if href and "/positions/" in href and any(i.isdigit() for i in href):
            if any(role in text for role in ["engineer", "data", "intern", "analyst"]):
                links.append(href)

    filtered_links = list(set(links))

    # Create folder if not exists
    os.makedirs("../data/raw", exist_ok=True)

    # Save CSV
    df = pd.DataFrame(filtered_links, columns=["Job URL"])
    df.to_csv("../data/raw/job_links.csv", index=False)

    print(f"✅ Success! Saved {len(filtered_links)} links to data/raw/job_links.csv")

    driver.quit()


if __name__ == "__main__":
    run_selenium()