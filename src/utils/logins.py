from selenium.webdriver.common.by import By

from src.config import AGAH_USERNAME, AGAH_PASSWORD


def agah_login(driver):
    driver.get('https://online.agah.com/')
    driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-login-page/section/div/div[1]/tse-built-in-login/form/div/label[3]/tse-captcha/div/div[2]/button[2]').click()
    driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-login-page/section/div/div[1]/tse-built-in-login/form/div/label[1]/input').send_keys(AGAH_USERNAME)
    driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-login-page/section/div/div[1]/tse-built-in-login/form/div/label[2]/input').send_keys(AGAH_PASSWORD)
    captcha = input('\nEnter captcha: ')
    driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-login-page/section/div/div[1]/tse-built-in-login/form/div/label[3]/tse-captcha/div/input').send_keys(captcha)
    driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-login-page/section/div/div[1]/tse-built-in-login/form/div/div[2]/button').click()

    return driver
