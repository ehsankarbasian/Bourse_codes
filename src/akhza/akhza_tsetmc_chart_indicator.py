from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from settings import Address


INDICATORS_XPATH = '/html/body/div[2]/div[3]/div[1]/div[2]/div[5]/a/i'
INDICATORS_XPATH = '/html/body/div[2]/div[3]/div[1]/div[2]/div[5]/a'
MA_XPATH = '/html/body/div[3]/div[2]/div[2]/div[3]/div/ul[2]/li[18]/span[1]'
MA_SETTINGS_XPATHES = ['/html/body/div[2]/div[3]/div[2]/div/div/table[2]/tbody/tr[3]/td/span[2]/a[2]',
                       '/html/body/div[2]/div[3]/div[2]/div/div/table[2]/tbody/tr[4]/td/span[2]/a[2]',
                       '/html/body/div[2]/div[3]/div[2]/div/div/table[2]/tbody/tr[5]/td/span[2]/a[2]']
MA_LENGTHES = [3, 6, 9]

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.set_window_position(x=1450, y=150)
driver.maximize_window()


def open_charts():
    counter = 0
    with open(Address.AKHZA_ACTIVE_TSETMC_URLS, "r") as f:
        for line in f.readlines():
            akhza_url = line[:-1]
            chart_url = akhza_url.replace('instInfo', 'DynamicChart')
            
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[counter])  
            driver.get(chart_url)
            counter += 1
            
            # TODO: delete this if
            if counter == 2:
                break

    driver.switch_to.window(driver.window_handles[counter])
    driver.close()
    counter -= 1
    return counter


def activate_indicators(count):
    for tab_index in range(count):
        driver.switch_to.window(driver.window_handles[tab_index])
        driver.find_element(by=By.XPATH, value=INDICATORS_XPATH).click()
        moving_average = driver.find_element(by=By.XPATH, value=MA_XPATH)
        moving_average.click()
        moving_average.click()
        moving_average.click()
        for ma_setting_xpath, ma_length in zip(MA_SETTINGS_XPATHES, MA_LENGTHES):
            driver.find_element(by=By.XPATH, value=ma_setting_xpath).click()
            driver.find_element(by=By.XPATH, value='/html/body/div[6]/div[4]/div[2]/table/tbody/tr/td[2]/input').send_keys(ma_length)
            driver.find_element(by=By.XPATH, value='/html/body/div[6]/div[4]/div[5]/div/a[2]').click()


chart_count = open_charts()
activate_indicators(chart_count)
