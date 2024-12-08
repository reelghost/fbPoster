import os
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def post_to_fb(driver, media, gui_instance):
    """Posts to fb"""
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Create a post"]')))
    driver.find_element(By.XPATH, '//span[contains(text(), "Photo/video")]').click()
    sleep(5)
    image_box = driver.find_element(By.XPATH, '//div/input[@type="file"]')
    image_box.send_keys(media) 
    sleep(5)
    driver.find_element(By.XPATH, '//div[@aria-label="Next"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//div[@aria-label="Post"]').click()
    sleep(7)
    gui_instance.status_label.configure(text="Posted successfully", text_color="green")
    gui_instance.update()

def login_to_facebook(driver, gui_instance):
    """Logins to fb if not yet logged in"""
    driver.get("https://web.facebook.com/login")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Your profile"]')))
        print("Already logged in")
    except TimeoutException:
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, 'loginbutton')))
        driver.find_element(By.ID, 'email').send_keys(os.getenv('FB_EMAIL'))
        driver.find_element(By.ID, 'pass').send_keys(os.getenv('FB_PASS'))
        sleep(1)
        driver.find_element(By.ID, 'loginbutton').click()

        # Check for WhatsApp 2FA
        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//span[text()="Enter the code that we sent to your WhatsApp account."]')))
            gui_instance.status_label.configure(text="You have 2FA enabled", text_color="green")
            gui_instance.update()
            fa_code = gui_instance.get_user_input("Enter the code sent to WhatsApp:")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'input'))).send_keys(fa_code)
            sleep(1)
            driver.find_element(By.XPATH, '//*[contains(text(),"Continue")]').click()
        except:
            pass

        # Check for regular 2FA via text message
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'approvals_code')))
            fa_code = gui_instance.get_user_input("Please enter the 2FA code sent via SMS")
            driver.find_element(By.ID, 'approvals_code').send_keys(fa_code)
            sleep(0.5)
            driver.find_element(By.ID, 'checkpointSubmitButton').click()
        except:
            pass

        # Trust this device prompt
        try:
            # WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[text()="If other people have access to this device, it’s best to always confirm it’s you."]')))
            WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Trust this device"]'))).click()
        except:
            pass
        # Wait for the login to complete
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Create a post"]')))

def fb_main(driver, media, gui_instance):
    login_to_facebook(driver, gui_instance)
    post_to_fb(driver, media, gui_instance)