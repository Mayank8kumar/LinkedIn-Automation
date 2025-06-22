import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_USER = os.getenv("LINKEDIN_USER")
LINKEDIN_PASS = os.getenv("LINKEDIN_PASS")

def login_linkedin():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("force-device-scale-factor=0.4")
    options.add_argument("high-dpi-support=0.4")
    # options.add_argument("--headless")  # Uncomment if headless mode is needed
    # options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.maximize_window()
    
    driver.get("https://www.linkedin.com/login")

    wait = WebDriverWait(driver, 5)

    # Login in the account 
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="username"]')))
    email_field.send_keys(LINKEDIN_USER)  # This is your email address

    password_field = driver.find_element(By.XPATH, '//input[@id="password"]')
    password_field.send_keys(LINKEDIN_PASS)  # This is your password

    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()

    # time.sleep(13)  # Let the page load after login to handle security

    if "feed" in driver.current_url:
        print("✅ Logged in to LinkedIn successfully.")
        # time.sleep(10)
        return driver
    else:
        print("❌ Login failed.")
        # time.sleep(10)
        driver.quit()
        return None
