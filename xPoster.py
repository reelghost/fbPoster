import os
import sys
from time import sleep
# import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def login_to_x(driver, gui_instance):
    """Logins to Instagram"""
    gui_instance.status_label.configure(text="Posting on X", text_color="yellow")
    gui_instance.update()
    driver.get("https://x.com/login")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@aria-label="Grok"]')))
    except TimeoutException:
        # Wait for the login fields to load
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="username"]'))).send_keys(os.getenv('X_EMAIL'))
        driver.find_element(By.XPATH, '//span[text()="Next"]').click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))).send_keys(os.getenv('X_PASS'))
        driver.find_element(By.XPATH, '//button[@data-testid="LoginForm_Login_Button"]').click()
        # confirm login
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@aria-label="Grok"]')))
        gui_instance.status_label.configure(text="Logged in to X successfully", text_color="green")
        gui_instance.update()
    finally:
        sleep(3)  # Delay to observe browser behavior

def post_image(driver, media, caption, gui_instance):
    # check for we removed your photo popup
    driver.find_element(By.XPATH, '//a[@aria-label="Post"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]').send_keys(caption)
    file_input = driver.find_element(By.XPATH, '//input[@data-testid="fileInput"]')
    file_input.send_keys(media)
    sleep(2)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="endEditingButton"]'))).click()
    except TimeoutException:
        pass
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="tweetButton"]'))).click()
    sleep(2)
    gui_instance.status_label.configure(text="Successful Posted...", text_color="green")
    gui_instance.update()


def x_main(driver, media, caption, gui_instance):
    login_to_x(driver, gui_instance)
    post_image(driver, media, caption, gui_instance)
