import os
import sys
from time import sleep
# import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def login_to_instagram(driver, gui_instance):
    """Logins to Instagram"""
    gui_instance.status_label.configure(text="Posting on instagram", text_color="green")
    gui_instance.update()
    driver.get("https://www.instagram.com/accounts/login/")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Profile')]")))
    except TimeoutException:
        # Wait for the login fields to load
        wait = WebDriverWait(driver, 15)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = driver.find_element(By.NAME, "password")
        
        # Enter credentials
        username_field.send_keys(os.getenv('INSTA_EMAIL'))
        password_field.send_keys(os.getenv('INSTA_PASS'))
        # Submit the form
        password_field.send_keys(Keys.RETURN)

        # check if password is correct
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Sorry, your password was incorrect. Please double-check your password."]')))
            gui_instance.status_label.configure(text="Your password is incorrect", text_color="red")
            gui_instance.update()
            sys.exit()
        except:
            pass
        # check for captcha
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Help us confirm")]')))
            gui_instance.status_label.configure(text="Captcha Found...exiting", text_color="green")
            gui_instance.update()
            sys.exit()
        except:
            pass

        # Wait to ensure login is successful
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Profile')]")))
    finally:
        sleep(3)  # Delay to observe browser behavior

def post_image(driver, media, caption, gui_instance):
    # check for we removed your photo popup
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'see why')]")))
        sleep(2)
    except:
        pass

    driver.find_element(By.XPATH, '//span[contains(text(), "Create")]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//span[contains(text(), "Post")]').click()
    sleep(3)
    file_input = driver.find_element(By.XPATH, '//input[@accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime"]')
    file_input.send_keys(media)
    sleep(1)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@role="button" and text()="Next"]'))).click()
    sleep(1)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@role="button" and text()="Next"]'))).click()
    # input caption
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))).send_keys(caption)
    
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div[@role="button" and text()="Share"]'))).click()
    try:
        share_success = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Your post has been shared."]')))
        gui_instance.status_label.configure(text=f"{share_success.text}", text_color="green")
        gui_instance.update()
    except TimeoutException:
        share_success = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Boost")]')))
        gui_instance.status_label.configure(text=f"{share_success.text}", text_color="green")
        gui_instance.update()

def insta_main(driver, media, caption, gui_instance):
    login_to_instagram(driver, gui_instance)
    post_image(driver, media, caption, gui_instance)
