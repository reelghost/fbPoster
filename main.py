# Made by iha for iha
'''
Automate posting on facebook
'''

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import pickle
import os

# Constants
FACEBOOK_URL = 'https://web.facebook.com/login'

EMAIL = ''
PASSWORD = ''
COOKIES_FILE_PATH = f'cookies/{EMAIL}.pkl'

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

def login_to_facebook(driver):
    '''Login to facebook'''
    driver.get(FACEBOOK_URL)
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, 'loginbutton')))  # wait for the page to load

    driver.find_element(By.ID, 'email').send_keys(EMAIL)
    driver.find_element(By.ID, 'pass').send_keys(PASSWORD)
    sleep(1)
    driver.find_element(By.ID, 'loginbutton').click()

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//span[text()="The password you\'ve entered is incorrect."]')))
        print("Incorrect password")
    except:
        pass

    # check for 2FA
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'approvals_code')))
        print("Your account has 2FA enabled..sending text message")
        
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[text()="Need another way to confirm that it\'s you?"]'))).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[text()="Text me a login code"]'))).click()
            sleep(1)
            driver.find_element(By.XPATH, '//a[@data-testid="dialog_title_close_button"]').click()
        except:
            print("You will need to pass the 2FA manually")
        x = input("Please enter the 2FA code sent: ")
        driver.find_element(By.ID, 'approvals_code').send_keys(x)
        sleep(0.5)
        driver.find_element(By.ID, 'checkpointSubmitButton').click()
    except:
        pass
    # TODO:Add the two checkpoints here
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Create a post"]'))) # wait for the login to complete
    save_cookies(driver, COOKIES_FILE_PATH)

def post(driver, p_message, media):
    '''
    Post to facebook
        p_message : What's on your mind text
        media : An absolute path to the media to be uploaded
    '''
    # Start post dialog box
    driver.find_element(By.XPATH, '//span[contains(text(), "Photo/video")]').click()
    sleep(5)
    post_box = driver.find_element(By.XPATH, '//div[@aria-label="What\'s on your mind, Deadbone?"]')
    post_box.send_keys(p_message)

    image_box = driver.find_element(By.XPATH, '//div/input[@type="file"]')
    image_box.send_keys(media) # use an absolute path
    sleep(5)
    driver.find_element(By.XPATH, '//div[@aria-label="Next"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//div[@aria-label="Post"]').click()
    sleep(10)

    print("Your post has been posted")

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get('https://web.facebook.com/')
    sleep(3)  # wait for the page to load

    if not load_cookies(driver, COOKIES_FILE_PATH):
        print('Logging in and saving cookies...')
        login_to_facebook(driver)
    else:
        print('Cookies loaded. Refreshing the page...')
        driver.refresh()
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "You must log in to continue.")]')))
            print("Logging in again")
            login_to_facebook(driver)
        except:
            pass

        # check for password again
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h2[text()="Please enter your password to continue"]')))
            driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(PASSWORD)
            sleep(0.5)
            driver.find_element(By.XPATH, '//input[@value="Continue"]').click()
        except:
            pass
        sleep(5)  # wait for the page to load with cookies

    # Posting
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Create a post"]'))) # wait for the login to complete

    post_message = "Life is like a sandwich. No matter how you flip it, the bread comes first."
    media = "D:\githubProjects\\fbPoster\post_images\\flipit.jpeg"
    post(driver=driver, p_message=post_message, media=media)
    

    driver.quit()

if __name__ == '__main__':
    main()
