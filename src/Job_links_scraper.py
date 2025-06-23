from selenium.webdriver.common.by import By
import time

def Job_links(driver, pages_to_scrape=5):
    """
    Scrapes job links from the job container.
    """

    driver.get("https://www.linkedin.com/jobs/collections/recommended/")
    
    all_links = []
    for page in range(pages_to_scrape):
        print(f"\n📄 Scraping Page {page + 1}...")
        print(" Extracting job cards inside the container...")

        time.sleep(3)
        job_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/jobs/view/')]")

        
        # Job links extraction one by one
        for link in job_links:
            url = link.get_attribute("href")
            if url and '/jobs/view/' in url:
                all_links.append(url)
        
        print(f"Page {page + 1}: Found {len(job_links)} links, total unique: {len(set(all_links))}")

        # Try clicking "Next Page" button
        try:
            next_button = driver.find_element(By.XPATH, "//button[@aria-label='View next page']")
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            time.sleep(1)
            next_button.click()
        except Exception as e:
            print("🚫 Could not go to the next page or no more pages.")
            break

    print(f"Found {len(list(set(all_links)))} unique job links.")
    return list(set(all_links))
