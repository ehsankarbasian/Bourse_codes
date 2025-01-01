import time
import jdatetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.firefox import GeckoDriverManager

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from src.config import AGAH_USERNAME, AGAH_PASSWORD


years = 7

ALL = []
counter = 0
f = open('results/Pazireh/all.txt', "a")


def get_all_pages_count():
    time.sleep(2)
    p = driver.find_element(by=By.XPATH, value='//*[@id="ag-484-of-page-number"]').text
    return int(p.replace(',', ''))

def go_next_year():
    driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-main-area/tse-global/section/div/div/tse-messages-page/div/tse-mdp-messages-page/tse-message-center/div/as-split/as-split-area[1]/tse-message-list/div/div[1]/tse-date-filter/button').click()
    driver.find_element(by=By.XPATH, value='/html/body/div/div/form/div[1]/button[2]').click()
    driver.find_element(by=By.XPATH, value='/html/body/div/div/form/div[2]/button[1]').click()

def go_first_page():
    driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-main-area/tse-global/section/div/div/tse-messages-page/div/tse-mdp-messages-page/tse-message-center/div/as-split/as-split-area[1]/tse-message-list/div/div[2]/ag-grid-angular/div/div[4]/span[3]/div[1]').click()

def get_get_filter(text):
    if 'پذیره نویسی' in text:
        hagh_taghadom = 'حق تقدم' in text
        edame = 'ادامه' in text
        etmam = 'اتمام' in text
        payan = 'پایان' in text
        tamdid = 'تمدید' in text
        dar_khosose = 'درخصوص' in text or 'در خصوص' in text
        morabehe = 'مرابحه' in text
        eslahiye = 'اصلاحیه' in text
        is_dirty = hagh_taghadom or edame or etmam or payan or tamdid or dar_khosose or morabehe or eslahiye
        return not is_dirty
    else:
        return False

ALL_ROWS_XPATHES = []
for row in range(1, 26):
    r = f'/html/body/tse-root/div/tse-main-area/tse-global/section/div/div/tse-messages-page/div/tse-mdp-messages-page/tse-message-center/div/as-split/as-split-area[1]/tse-message-list/div/div[2]/ag-grid-angular/div/div[2]/div[2]/div[3]/div[1]/div[2]/div/div[{row}]/div[2]'
    ALL_ROWS_XPATHES.append(str(r))

def get_one():
    col = []
    for row_xpath in ALL_ROWS_XPATHES:
        try:
            row = driver.find_element(by=By.XPATH, value=row_xpath)
            col.append(row.text)
        except:
            pass
    return col
    
def get_all():
    global counter, f
    pages = get_all_pages_count()
    for _ in range(pages-1):
        col = get_one()
        for text in col:
            if get_get_filter(text):
                if text not in ALL:
                    ALL.append(text)
                    f.write(text + '\n')
                    counter += 1
                    print(counter)
        driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-main-area/tse-global/section/div/div/tse-messages-page/div/tse-mdp-messages-page/tse-message-center/div/as-split/as-split-area[1]/tse-message-list/div/div[2]/ag-grid-angular/div/div[4]/span[3]/div[3]').click()
        
        time.sleep(0.5)


driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.set_window_position(x=1450, y=150)
driver.get('https://online.agah.com/')
driver.maximize_window()
driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-login-page/section/div/div[1]/tse-built-in-login/form/div/label[1]/input').send_keys(AGAH_USERNAME)
driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-login-page/section/div/div[1]/tse-built-in-login/form/div/label[2]/input').send_keys(AGAH_PASSWORD)
captcha = input('Enter captcha: ')
driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-login-page/section/div/div[1]/tse-built-in-login/form/div/label[3]/tse-captcha/div/input').send_keys(captcha)
driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-login-page/section/div/div[1]/tse-built-in-login/form/div/div[2]/button').click()
time.sleep(3)
driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-main-area/tse-global/section/div/tse-widget-bar/div/div[1]/span[2]').click()
driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-main-area/tse-global/section/div/tse-widget-bar/div/div[2]/h2/div/button[2]').click()
driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-main-area/tse-global/section/div/div/tse-messages-page/div/tse-mdp-messages-page/tse-message-center/div/as-split/as-split-area[1]/tse-message-list/div/div[1]/div/select').send_keys('نمایش منقضی شده ها')
driver.find_element(by=By.XPATH, value='/html/body/tse-root/div/tse-main-area/tse-global/section/div/div/tse-messages-page/div/tse-mdp-messages-page/tse-message-center/div/as-split/as-split-area[1]/tse-message-list/div/div[1]/tse-date-filter/button').click()
driver.find_element(by=By.XPATH, value='/html/body/div/div/form/select').send_keys('سالانه')
for _ in range(years):
    driver.find_element(by=By.XPATH, value='/html/body/div/div/form/div[1]/button[1]').click()
driver.find_element(by=By.XPATH, value='/html/body/div/div/form/div[2]/button[1]').click()

for _ in range(years):
    get_all()
    go_next_year()
    go_first_page()
get_all()


print('END')


# driver.find_element(by=By.XPATH, value='').click()



