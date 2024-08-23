from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Replace with the path to your WebDriver executable
driver_path = '/Users/namankhurpia/Desktop/Taxmann/chromedriver-mac-arm64/chromedriver'  # Update this path to your ChromeDriver

# Initialize the WebDriver using Service
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

try:
    # Open the login page
    driver.get('https://www.taxmann.com/gp/auth/login')

    # Wait for the page and JavaScript to load
    driver.implicitly_wait(30)

    # Click on the "Login with Email" button
    login_with_email_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='tab-links' and text()='Login with Email']"))
    )
    login_with_email_button.click()

    # Input Email
    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='email'].p-inputtext.p-component.form-control-t1"))
    )
    email_field.send_keys('gst.taxmann2022@gmail.com')

    # Add any further steps for the login process here (e.g., entering the password, clicking the login button)

finally:
    # Close the WebDriver
    driver.quit()
