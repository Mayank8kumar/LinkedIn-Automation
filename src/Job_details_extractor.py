import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from Login import login_linkedin


def extract_job_details(driver):
    # details = []
    # driver = login_linkedin()

    df_links = pd.read_csv('../data/recommended_jobs.csv')
    output_file = '../data/Job_details.csv'

    job_df = pd.DataFrame(columns=[
    "Job Profile",
    "Job Description",
    "Company Name",
    "Company Link",
    "Job Link",
    "Easy Apply"
    ]).to_csv(output_file, index=False)

    for index, row in df_links.iterrows():
        job_url = row['Job URL']
        print(f"\nOpening Job {index + 1}: {job_url}")
        driver.get(job_url)
        time.sleep(2)  # Wait for page load

        # Job profile extraction
        try:
            job_profile = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/h1').text
        except:
            job_profile = "N/A"
            
        # Company name extraction
        try:
            company_element = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/main/div/div/div/div/div/div/div/div[1]/div[1]')
            company_name = company_element.text

        except:
            company_name = "N/A"

        # Company link extraction
        try:
            company_link_element = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[1]/div[1]/a')
            company_link = company_link_element.get_attribute("href")
        except:
            company_link = "N/A"

        # Easy apply button available or not
        try:
            easy_apply_btn = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[6]/div/div/div/button')
            easy_apply = "Yes" if "Easy Apply" in easy_apply_btn.text else "No"
        except:
            easy_apply = "No"
        
        # Click "Show more" button to expand full description
        time.sleep(2)
        try:
            show_more_btn = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[4]/footer/button')
            show_more_btn.click()
            time.sleep(1)  # Give it time to expand
        except:
            print("Show more button not found or already expanded.")
        
        # Job description extraction
        try:
            job_description = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[4]/article').text
        except:
            job_description = "N/A"

        # Ask before proceeding 
        # proceed = input("Proceed to next job? (y/n): ").strip().lower()
        # if proceed != 'y':
        #     print(" Stopped by user.")
        #     break

        row_data = pd.DataFrame([{
            "Job Profile": job_profile,
            "Job Description": job_description,
            "Company Name": company_name,
            "Company Link": company_link,
            "Job Link": job_url,
            "Easy Apply": easy_apply
        }])

        row_data.to_csv(output_file, mode='a', header=False, index=False)
        print(f"✅ Saved Job {index + 1}")



    print("\n All data saved to 'job_details.csv'")


