import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import telegramBot.config as config


def load_inst_img_by_link(link):
    try:
        driver = webdriver.Chrome()
        driver.get('https://www.instagram.com/p/ClCUTF1pKzJ/?igshid=Zjc2ZTc4Nzk=')
        # driver.get(link)
        time.sleep(10)
        _login = driver.find_element(By.NAME, "username")
        _login.clear()
        _login.send_keys('EmoDec05')

        time.sleep(2)
        _password = driver.find_element(By.NAME, "password")
        _password.clear()
        _password.send_keys('Leleka270795')
        _password.send_keys(Keys.ENTER)

        time.sleep(5)
        _not_now_button = driver.find_element(By.CSS_SELECTOR, 'button[type="button"]')
        _not_now_button.click()

        time.sleep(7)
        file_name = 'inst_screenshot'
        file_extension = '.png'
        file_full_name = file_name + file_extension
        driver.save_screenshot(file_full_name)
        driver.quit()
        return [file_name, file_extension]

    except:
        return 'Error'

