from Login import login_linkedin
from Job_links_scraper import Job_links
from Job_details_extractor import extract_job_details
import csv
import os
import time

start_time = time.time()

driver = login_linkedin()
if driver:
    links = Job_links(driver)

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "recommended_jobs.csv")

    with open(output_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Job URL"])
        for link in links:
            writer.writerow([link])
    
    print("The file has been successfully Stored. ")

extract_job_details(driver)
print("The total time takes", time.time() - start_time)
input("Press ENTER to stop the driver.")
driver.quit()

