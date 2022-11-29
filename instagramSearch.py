import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import config

import markers


def load_instagram_image(link):
    try:
        driver = webdriver.Chrome()
        # driver.get('https://www.instagram.com/p/ClCUTF1pKzJ/?igshid=Zjc2ZTc4Nzk=')
        driver.get(link)
        time.sleep(10)
        _login = driver.find_element(By.NAME, "username")
        _login.clear()
        _login.send_keys(config.instagram_username)

        time.sleep(2)
        _password = driver.find_element(By.NAME, "password")
        _password.clear()
        _password.send_keys(config.instagram_password)
        _password.send_keys(Keys.ENTER)

        time.sleep(5)
        _not_now_button = driver.find_element(By.CSS_SELECTOR, 'button[type="button"]')
        _not_now_button.click()

        time.sleep(7)
        file_name = markers.Instagram_screenshot_name
        file_extension = markers.Instagram_screenshot_extension
        file_full_name = file_name + file_extension
        driver.save_screenshot(file_full_name)
        driver.quit()
        return [file_name, file_extension]

    except:
        return markers.Error


load_instagram_image(markers.Instagram_link_example)
