from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import signal
import csv

from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

file = None  # Define file at the top

# Setup a signal handler to close the driver on CTRL+C
def signal_handler(sig, frame):
    logout()
    if file is not None:
        file.close() 
    
    print('You pressed Ctrl+C! Closing the driver properly.')
    driver.quit()

def logout():
    try:
        # Wait for the profile icon and click it
        profile_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.active-user"))
        )
        profile_icon.click()

        # Wait for the logout link and click it
        logout_link = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Logout')]"))
        )
        logout_link.click()
        # Wait for the page and JavaScript to load
        time.sleep(30)

        print("Logged out successfully.")
    except Exception as e:
        print(f"Error during logout: {e}")



#signal.signal(signal.SIGINT, signal_handler)

# Replace with the path to your WebDriver executable
driver_path = '/Users/namankhurpia/Desktop/Taxmann/chromedriver-mac-arm64/chromedriver'  # Update this path to your ChromeDriver

# Initialize the WebDriver using Service
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

try:
    
    # Open the webpage
    driver.get('https://www.taxmann.com/gp/auth/login')

    # Wait for the page and JavaScript to load
    driver.implicitly_wait(30)

    login_with_email_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='tab-links' and text()='Login with Email']"))
    )
    login_with_email_button.click()

    # Input Email
    email_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='email'].p-inputtext.p-component.form-control-t1"))
    )
    email_field.send_keys('gst.taxmann2022@gmail.com')

    # Input Password
    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password'][name='password'].p-inputtext.p-component.form-control-t1"))
    )
    password_field.send_keys('Gst@2022')

    # Click the 'Sign In' button
    sign_in_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Sign In' and @type='submit' and contains(@class, 'button-primary')]")))
    sign_in_button.click()





    # Wait for the page to load after login
    WebDriverWait(driver, 30).until(
        EC.url_changes(driver.current_url)  # Wait for the URL to change after login
    )

    # After login, navigate to the GST caselaws page
    driver.get('https://www.taxmann.com/research/gst/caselaws')

    # Wait for the page to load and ensure it is fully loaded
    WebDriverWait(driver, 90).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )







    # Find the 'Category' span and hover over it
    category_span = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//span[@title='Category']"))
    )
    ActionChains(driver).move_to_element(category_span).perform()

    time.sleep(2)  # Wait for the dropdown to load



        # Attempt to click 'GST' option by targeting the enclosing <a> tag
    try:
        gst_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'dropdown-item') and .//label[@title='GST']]"))
        )
        gst_link.click()
    except TimeoutException:
        print("GST option not clickable using normal methods, attempting JavaScript click.")
        driver.execute_script("arguments[0].click();", gst_link)



    time.sleep(10)  

    # Wait for the titles to load
    titles = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list-h-1"))
    )


    # Open a CSV file to write the case data
    file = open('case_data.csv', 'w', newline='', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(['Title', 'Content'])


    for title in titles:
        title_text = title.text
        title.click()  # Click on the title
        time.sleep(5)
        
        # Wait to ensure the page has loaded the content
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='home' and not(@hidden)]"))
        )

        # Extract the content using BeautifulSoup
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the active content that does not have the hidden attribute
        content_div = soup.find("div", {"id": "home", "hidden": False})

        if content_div:
            content_text = content_div.text.strip()
            print(f"Added: {title_text} with content: {content_text[:100]}")

            # Write data to CSV immediately
            writer.writerow([title_text, content_text])
        else:
            print(f"Content not found for: {title_text}")

        time.sleep(20)  # Allow time for the page to reload the list

        # Refresh the titles list after each iteration
        titles = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list-h-1"))
        )
    

finally:
    logout()
    if 'driver' in locals() or 'driver' in globals():
        if driver is not None:
            driver.quit()
    if file is not None:
        file.close()

    print('Driver closed successfully.')





#driver.quit()