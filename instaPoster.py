import os
import sys
import glob
import shutil
import pickle
from time import sleep
from dotenv import load_dotenv, set_key
# import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


load_dotenv()
def save_cookies(driver, file_path):
    '''Save the cookies'''
    with open(file_path, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, file_path):
    '''Load the cookies'''
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        return True
    return False

def get_first_image_path(folder_path='images'):
    image_extensions = ('*.png', '*.jpg', '*.jpeg')
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))
    image_files.sort()
    return os.path.abspath(image_files[0]) if image_files else None

def move_image_to_posted(image_path, destination_folder=os.getenv('POSTED_FOLDER')):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    shutil.move(image_path, os.path.join(destination_folder, os.path.basename(image_path)))
    # print("Posted image moved to folder.")

def login_to_instagram(driver):
    try:
        # Navigate to Instagram login page
        driver.get("https://www.instagram.com/accounts/login/")
        
        # Wait for the login fields to load
        wait = WebDriverWait(driver, 15)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = driver.find_element(By.NAME, "password")
        
        # Enter credentials
        username_field.send_keys(os.getenv('INSTA_USER'))
        password_field.send_keys(os.getenv('INSTA_PASS'))
        # Submit the form
        password_field.send_keys(Keys.RETURN)

        # check if password is correct
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Sorry, your password was incorrect. Please double-check your password."]')))
            print("The password is incorrect")
            sys.exit()
        except:
            pass
        # check for captcha
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Help us confirm")]')))
            print("Captcha Found")
            sys.exit()
        except:
            pass

        # Wait to ensure login is successful
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Profile')]")))
        print("Login successful!")
        save_cookies(driver, f'cookies/{os.getenv("INSTA_USER")}.pkl')
    except Exception as e:
        print(f"An error occurred during login: {e}")
    finally:
        sleep(3)  # Delay to observe browser behavior

def post_image(driver, media):
    driver.find_element(By.XPATH, '//span[contains(text(), "Create")]').click()
    driver.find_element(By.XPATH, '//span[contains(text(), "Post")]').click()
    sleep(3)
    file_input = driver.find_element(By.XPATH, '//input[@accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"]')
    file_input.send_keys(media)
    sleep(1)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@role="button" and text()="Next"]'))).click()
    sleep(1)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@role="button" and text()="Next"]'))).click()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div[@role="button" and text()="Share"]'))).click()
    try:
        share_success = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Your post has been shared."]')))
        print(share_success.text)
    except:
        share_success = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Boost")]')))
        print(share_success.text)
    sleep(3)

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-geolocation")
    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,  # Disable password manager
        'profile.password_manager_enabled': False  # Disable password saving prompt
    })
    driver = webdriver.Chrome(options=options)

    try:
        media = get_first_image_path(os.getenv('IMAGES_FOLDER'))
        login_to_instagram(driver)
        post_image(driver, media)
        
    finally:
        driver.quit()  # Close the browser after the script ends

if __name__ == "__main__":
    main()
