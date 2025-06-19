from Login import login_linkedin

driver = login_linkedin()
if driver:
    input("Press Enter to close browser...")
    driver.quit()
