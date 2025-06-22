from selenium.webdriver.common.by import By
import time

def Job_links(driver):
    """
    Scrapes job links from the job container.
    """

    driver.get("https://www.linkedin.com/jobs/collections/recommended/")
    time.sleep(3)
    
    print(" Extracting job cards inside the container...")
 
    job_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/jobs/view/')]")

    # Clean and print all unique job links
    all_links = []
    for link in job_links:
        url = link.get_attribute("href")
        if url and '/jobs/view/' in url:
            all_links.append(url)
    
    print(f"✅ Found {len(list(set(all_links)))} unique job links.")
    return list(set(all_links))
