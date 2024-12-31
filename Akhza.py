import time
import jdatetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

all_active_akhza = []
COLUMN_HEADERS = 'benefit_factor | name | deadline_date | deadline_monthes'


class Akhza:
    DEADLINE_PRICE = 10**6

    def __init__(self, name, price):
        self.name = name
        self.current_price = price
        date_digits = name.split('-')[-1]
        self.pay_date = self.__gat_date_from_digits(date_digits)
    
    
    @staticmethod
    def __gat_date_from_digits(digits):
        digits = str(digits)
        year = int('14' + digits[:2])
        month = int(digits[2:4])
        day = int(digits[4:])
        
        date = jdatetime.date(year, month, day)
        return date
    

    @property
    def __deadline_days(self):
        now = jdatetime.date.today()
        delta = self.pay_date - now
        return delta.days
    
    
    @property
    def is_expired(self):
        return self.__deadline_days <= 0
    

    @property
    def __benefit_factor(self):
        return self.DEADLINE_PRICE / self.current_price


    @property
    def annualized_benefit_percent(self):
        # TODO: Calculate trade fee
        annualized_factor = self.__benefit_factor**(365/self.__deadline_days)
        annualized_percent = (annualized_factor-1)*100
        return annualized_percent


    @staticmethod
    def __normalize_percent(percent):
        percent *= 100
        percent = int(percent)
        percent = str(percent)
        percent = percent[:2] + '.' + percent[2:]
        return percent


    def __str__(self):
        name_items = [8*' ' + self.__normalize_percent(self.annualized_benefit_percent) + '%',
                      self.name.split('-')[0].replace('اخزا', '').replace(' ', '') + ' ',
                      ' ' + str(self.pay_date).replace('-', '/') + '  ',
                      str(self.__deadline_days//30)]
        return ' | '.join(name_items)


driver = webdriver.Firefox()
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
        return Akhza.DEADLINE_PRICE


current_akhza_div_id = 1
current_akhza = get_next_akhza_link(current_akhza_div_id)
current_akhza_span_text = get_next_akhza_span(current_akhza_div_id).text

print(COLUMN_HEADERS)
while '(نماد قدیمی حذف شده)' not in current_akhza_span_text:
    current_akhza.click()
    name = current_akhza.text
    driver.switch_to.window(driver.window_handles[1])
    price = get_price(driver)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
    akhza = Akhza(name, price)
    if price < Akhza.DEADLINE_PRICE and not akhza.is_expired:
        print(akhza)
        all_active_akhza.append(akhza)
    
    current_akhza_div_id += 1
    current_akhza = get_next_akhza_link(current_akhza_div_id)
    current_akhza_span_text = get_next_akhza_span(current_akhza_div_id).text

driver.close()


def get_akhza_annualized_benefit(akhza):
    return akhza.annualized_benefit_percent

all_active_akhza.sort(key=get_akhza_annualized_benefit)

print(80*'_')
print('Sorted by benefit all active akhza:')
print(COLUMN_HEADERS)
for akhza in all_active_akhza:
    print(akhza)

print(80*'_')
print('The best akhza for today:')
print(COLUMN_HEADERS)
print(all_active_akhza[-1])
