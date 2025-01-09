import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.firefox import GeckoDriverManager

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from src.akhza.akhza import Akhza
from settings import Address


all_active_akhza = []


driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.set_window_position(x=1450, y=150)
driver.get('http://tsetmc.ir')
driver.maximize_window()
driver.find_element(by=By.XPATH, value='//*[@id="search"]').click()
driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[3]/div/input').send_keys('اخزا')
time.sleep(3)


def get_akhza_link_xpath(div_id):
    return f'/html/body/div[2]/div[3]/div/div/div[2]/div/div/div/div[1]/div[2]/div[3]/div[2]/div/div/div[{div_id}]/div[1]/span/a'

def get_akhza_span_xpath(div_id):
    return f'/html/body/div[2]/div[3]/div/div/div[2]/div/div/div/div[1]/div[2]/div[3]/div[2]/div/div/div[{div_id}]/div[1]/span'

def get_next_akhza_link(div_id):
    return driver.find_element(by=By.XPATH, value=get_akhza_link_xpath(div_id))

def get_next_akhza_span(div_id):
    return driver.find_element(by=By.XPATH, value=get_akhza_span_xpath(div_id))

def get_price(driver):
    status_delay = 5
    status_xpath = '//*[@id="d01"]'
    status_locator = (By.XPATH, status_xpath)
    
    price_delay = 1
    best_seller_price_xpath = '/html/body/div/div/div[2]/div[3]/div[3]/div[2]/div[2]/div/table/tbody/tr[1]/td[4]'
    last_deal_price_xpath = '/html/body/div/div/div[2]/div[3]/div[3]/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[2]/div/div'
    best_seller_price_locator = (By.XPATH, best_seller_price_xpath)
    last_deal_price_locator = (By.XPATH, last_deal_price_xpath)
    
    try:
        time.sleep(2)
        status = WebDriverWait(driver, status_delay).until(EC.presence_of_element_located(status_locator))
        price = 0
        if status.text == 'مجاز':
            price = WebDriverWait(driver, price_delay).until(EC.presence_of_element_located(best_seller_price_locator))
            time.sleep(0.5)
            price = int(price.text.replace(',', ''))
        else:
            price = WebDriverWait(driver, price_delay).until(EC.presence_of_element_located(last_deal_price_locator))
            time.sleep(0.5)
            price = int(price.text.split()[0].replace(',', ''))
        if price == 0:
            price = WebDriverWait(driver, price_delay).until(EC.presence_of_element_located(last_deal_price_locator))
            time.sleep(0.5)
            price = int(price.text.split()[0].replace(',', ''))
        return price
    except TimeoutException:
        print("Loading took too much time!")
        return Akhza.DEADLINE_PRICE_AFTER_FEE


def print_headers(subject=None):
    print()
    print(80*'_')
    if subject:
        print(subject)
    print(Akhza.COLUMN_HEADERS)


current_akhza_div_id = 1
current_akhza = get_next_akhza_link(current_akhza_div_id)
current_akhza_span_text = get_next_akhza_span(current_akhza_div_id).text

print_headers()
while '(نماد قدیمی حذف شده)' not in current_akhza_span_text:
    current_akhza.click()
    name = current_akhza.text
    driver.switch_to.window(driver.window_handles[1])
    price = get_price(driver)
    current_url = driver.current_url
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
    akhza = Akhza(name, price, url=current_url)
    if price < Akhza.DEADLINE_PRICE_AFTER_FEE and not akhza.is_expired:
        print(akhza)
        all_active_akhza.append(akhza)
    
    current_akhza_div_id += 1
    current_akhza = get_next_akhza_link(current_akhza_div_id)
    current_akhza_span_text = get_next_akhza_span(current_akhza_div_id).text

driver.close()


def get_akhza_deadline_days(akhza):
    return akhza.deadline_days

def get_akhza_annualized_benefit(akhza):
    return akhza.annualized_benefit_percent

all_active_akhza.sort(key=get_akhza_deadline_days)
with open(Address.AKHZA_SORTED_DEADLINE, "w") as output_file:
    output_file.write(Akhza.COLUMN_HEADERS + '\n')
    for akhza in all_active_akhza:
        output_file.write(akhza.__str__(deadline_by_day=True) + '\n')
    output_file.write(Akhza.COLUMN_HEADERS)

all_active_akhza.sort(key=get_akhza_annualized_benefit, reverse=True)
with open(Address.AKHZA_SORTED_BENEFIT, "w") as output_file:
    output_file.write(Akhza.COLUMN_HEADERS + '\n')
    for akhza in all_active_akhza:
        output_file.write(akhza.__str__() + '\n')
    output_file.write(Akhza.COLUMN_HEADERS)

with open(Address.AKHZA_ACTIVE_LIST, "w") as akhza_list_file:
    for akhza in all_active_akhza:
        akhza_list_file.write(akhza.symbol + '-' + str(akhza.deadline_days) + '\n')

with open(Address.AKHZA_ACTIVE_URLS, "w") as akhza_list_file:
    for akhza in all_active_akhza:
        akhza_list_file.write(akhza.url + '\n')

print('\nSorted results has been written in the folder: "results/Akhza"')

print_headers('The best akhza for today:')
print(all_active_akhza[0])
