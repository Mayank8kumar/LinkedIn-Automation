import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from Login import login_linkedin


def init_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--force-device-scale-factor=0.5")
    return webdriver.Chrome(options=options)


def extract_job_details(driver):
    # details = []
    # driver = login_linkedin()

    df_links = pd.read_csv('../data/recommended_jobs.csv')

    job_df = pd.DataFrame(columns=[
    "Job Profile",
    "Job Description",
    "Company Name",
    "Company Link",
    "Job Link",
    "Easy Apply"
    ])

    for index, row in df_links.iterrows():
        job_url = row['Job URL']
        print(f"\nOpening Job {index + 1}: {job_url}")
        driver.get(job_url)
        time.sleep(5)  # Wait for page load

        # Extract Job Profile
        try:
            job_profile = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/h1').text
        except:
            job_profile = "N/A"

        # Click "Show more" button to reveal full description
        try:
            show_more_btn = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[4]/footer/button')
            show_more_btn.click()
            time.sleep(1)
        except:
            print("Show more button not found or already expanded.")
        
        # Extract Job description
        try:
            job_description = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[4]/article').text
        except:
            job_description = "N/A"
        
        # Extract Company Details 
        try:
            company_element = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[1]/div[1]/a')
            company_name = company_element.text
            company_link = company_element.get_attribute("href")
        except:
            company_name = "N/A"
            company_link = "N/A"
        
        # Easy apply available or not ?
        try:
            easy_apply_btn = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[6]/div/div/div/button')
            easy_apply = "Yes" if "Easy Apply" in easy_apply_btn.text else "No"
        except:
            easy_apply = "No"

        # Add row to DataFrame
        job_df.loc[len(job_df)] = [
            job_profile,
            job_description,
            company_name,
            company_link,
            job_url,
            easy_apply
        ]

        # Ask before proceeding 
        # proceed = input("Proceed to next job? (y/n): ").strip().lower()
        # if proceed != 'y':
        #     print(" Stopped by user.")
        #     break

    job_df.to_csv("../data/Job_details.csv", index=False)
    print("\n All data saved to 'linkedin_job_data.csv'")


