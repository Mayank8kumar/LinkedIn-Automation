import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def easy_apply(driver, csv_path='C:\\Users\\Mayank kumar\\Desktop\\LinkedIn_Auto_apply\\data\\job_details.csv'):
    wait = WebDriverWait(driver, 10)

    print("📂 Loading job data...")
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return

    easy_jobs = df[df['Easy Apply'] == 'Yes']
    print(f"🔎 Total Easy Apply jobs found: {len(easy_jobs)}")

    if easy_jobs.empty:
        print("⚠️ No Easy Apply jobs found. Exiting.")
        return

    for index, row in easy_jobs.iterrows():
        job_url = row.get('Job Link')
        if not job_url:
            continue

        print(f"\n➡️ Applying to job: {job_url}")
        driver.get(job_url)
        time.sleep(2)

        try:
            # Step 1: Click Easy Apply button
            easy_apply_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[6]/div/div/div/button"))
            )
            easy_apply_btn.click()
            print("✅ Clicked Easy Apply")
            time.sleep(2)

            # Loop to handle all steps (Next → Next → Review -> Submit)
            while True:
                
                try:
                    # Pause to allow manual form input (for additional questions)
                    # Check if additional question form/dialog is open
                    dialog_xpath = "//body/div/div[@data-test-modal-id='easy-apply-modal']/div[@role='dialog']/div/div[@aria-label]"
                    forms = driver.find_elements(By.XPATH, dialog_xpath)
                    if forms:
                        print("📄 Additional questions detected. Waiting for manual input...")
                        time.sleep(10)

                    # Try clicking 'Next'
                    next_button = driver.find_element(By.XPATH, "//span[normalize-space()='Next']")
                    
                    if next_button.is_enabled():
                        next_button.click()
                        print("➡️ Clicked Next")
                        time.sleep(2)
                    else:
                        print("⚠️ Next button disabled, breaking loop.")
                        break

                except NoSuchElementException:
                    print("⚠️ No Next button found, trying to proceed...")
                    break
                except Exception as e:
                    print(f"⚠️ Error in step loop: {e}")
                    break
                    
                try:
                    # Check if 'Review' button is available → exit loop if found
                    review_btn = driver.find_element(By.XPATH, "//span[normalize-space()='Review']")
                    
                    if review_btn.is_displayed():
                        review_btn.click()
                        print("📝 Review button is visible, exiting step loop.")
                        break
                except NoSuchElementException:
                    pass  # Review not available yet

            # Scroll to bottom
            try:
                modal = driver.find_element(By.CLASS_NAME, "jobs-easy-apply-modal")
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
                time.sleep(1)
            except:
                pass

            try:
                submit_btn = driver.find_element(By.XPATH, "//span[normalize-space()='Submit application']")
                submit_btn.click()
                print("🎯 Application submitted successfully.")
            except:
                print("❌ Submit button not found")

        except TimeoutException:
            print("❌ Easy Apply button not found or not clickable.")
        except Exception as e:
            print(f"❌ Failed to apply: {e}")

        time.sleep(2)
