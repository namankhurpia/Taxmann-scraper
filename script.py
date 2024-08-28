from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


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


    # Find the 'Category' span and hover over it
    category_span = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//span[@title='Court']"))
    )
    ActionChains(driver).move_to_element(category_span).perform()

    time.sleep(2)  # Wait for the dropdown to load


    # Attempt to click 'GST' option by targeting the enclosing <a> tag
    try:
        supreme = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'dropdown-item') and .//label[@title='SC']]"))
        )
        supreme.click()
    except TimeoutException:
        print("GST option not clickable using normal methods, attempting JavaScript click.")
        driver.execute_script("arguments[0].click();", supreme)

    time.sleep(10)  



    # Wait for the titles to load
    titles = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list-h-1"))
    )



    #my indexing approach
    """

    num_articles = 200

    for i in range(num_articles):
        try:
            # Wait for the preloader to disappear (adjust the selector if needed)
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".preloader.ng-star-inserted"))
            )
            
            # Refresh the titles list to ensure the element is clickable
            titles = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list-h-1"))
            )
            
            # Find and click on the title
            titles[0].click()
            #time.sleep(20)
            
            # Wait for the download button to be clickable
            download_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='home' and not(@hidden)]//span[contains(@class, 'menu-box-list') and .//img[@title='download']]"))
            )
            download_button.click()

            # Wait for the PDF download link to be clickable in the visible part of the new tab
            pdf_download_link = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='home' and not(@hidden)]//li/a[contains(text(), 'PDF')]"))
            )
            pdf_download_link.click()
            
            # Wait for the download to complete
            #time.sleep(15)  # Adjust as needed

            # Scroll to the next title
            if i < num_articles - 1:
                next_title = titles[i + 1]
                driver.execute_script("arguments[0].scrollIntoView(true);", next_title)
                #driver.execute_script("window.scrollBy(0, -20);")
        

        except Exception as e:
            print(f"An error occurred for article {i+1}: {e}")

         """

    num_articles = 200

    for i in range(num_articles):
        try:
            # Wait for the page to stabilize and reload necessary elements
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".preloader.ng-star-inserted"))
            )
            
            # Dynamically find each title during each iteration
            titles = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list-h-1"))
            )

            if i < len(titles):
                # Scroll the current title into view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", titles[i])
                time.sleep(2)  # Adjust time as needed for the scrolling to finish
                
                # Click on the current title
                WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable(titles[i])
                )
                titles[i].click()
                
                # Handle download in the new context
                # Code for handling the download button and PDF link goes here...

                # Wait and prepare for the next title
                time.sleep(10)  # Allow time for download and any UI reset


                # Wait for the download button to be clickable
                download_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@id='home' and not(@hidden)]//span[contains(@class, 'menu-box-list') and .//img[@title='download']]"))
                )
                download_button.click()

                # Wait for the PDF download link to be clickable in the visible part of the new tab
                pdf_download_link = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@id='home' and not(@hidden)]//li/a[contains(text(), 'PDF')]"))
                )
                pdf_download_link.click()

        except Exception as e:
            print(f"An error occurred for article {i+1}: {e}")
            # Optionally, break or continue based on the type of error
            
        
        
                
        # Wait for the download to complete (this may need adjustment depending on your download process)
        #time.sleep(10)  # Adjust this time as needed
        
        # Scroll to the next title
        #if i < num_articles - 1:
        #    next_title = titles[i + 1]
        #    driver.execute_script("arguments[0].scrollIntoView(true);", next_title)
        
        #time.sleep(2)  # Give time for the scroll and any transitions
        
        # Refresh the titles list to ensure proper indexing
        #titles = WebDriverWait(driver, 30).until(
        #    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".list-h-1"))
        #)

    

finally:
    logout()
    if 'driver' in locals() or 'driver' in globals():
        if driver is not None:
            driver.quit()
    if file is not None:
        file.close()

    print('Driver closed successfully.')





#driver.quit()