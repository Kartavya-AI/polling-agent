"""
Simple LinkedIn Post Script
Posts "Hello" to LinkedIn using Selenium
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback

def post_to_linkedin(email, password, message="Hello"):
    """Simple function to post a message to LinkedIn"""
    
    # Setup Chrome driver
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # Comment out the next line if you want to see the browser
    # options.add_argument('--headless')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20)
    
    try:
        print("Opening LinkedIn...")
        driver.get("https://www.linkedin.com/login")
        
        # Login
        print("Logging in...")
        email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_field.send_keys(email)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Wait for login to feed page
        wait.until(EC.url_contains("feed"))
        print("Successfully logged in!")
        
        # Go to feed page (redundant but ensures proper page)
        driver.get("https://www.linkedin.com/feed/")
        time.sleep(3)
        
        # Scroll down a bit to ensure button visibility
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(1)
        
        # Take screenshot for debugging UI state
        driver.save_screenshot("linkedin_feed.png")
        print("Saved screenshot: linkedin_feed.png")
        
        # Click "Start a post" using aria-label for better robustness
        print("Creating post...")
        start_post = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@aria-label, 'Start a post')]"
        )))
        start_post.click()
        
        # Wait for post editor to appear
        post_editor = wait.until(EC.presence_of_element_located((
            By.XPATH, "//div[@data-placeholder='What do you want to talk about?']"
        )))
        
        # Click and enter message
        post_editor.click()
        post_editor.send_keys(message)
        time.sleep(2)
        
        # Click the Post button
        post_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(text(), 'Post')]"
        )))
        post_button.click()
        
        print(f"Successfully posted: '{message}'")
        time.sleep(3)
        
    except Exception as e:
        print("Error occurred:")
        traceback.print_exc()
        
    finally:
        driver.quit()


# # Usage
# if __name__ == "__main__":
#     # Replace with your LinkedIn credentials
#     EMAIL = "your_email@example.com"
#     PASSWORD = "your_password"
    
#     # Post "Hello" to LinkedIn
#     post_to_linkedin(EMAIL, PASSWORD, "Hello")
# Usage
if __name__ == "__main__":
    # Replace with your LinkedIn credentials
    EMAIL = "varunrao924@gmail.com"
    PASSWORD = "platitun$924"
    
    # Post "Hello" to LinkedIn
    post_to_linkedin(EMAIL, PASSWORD, "Hello")