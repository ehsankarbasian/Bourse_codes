import jdatetime


class Akhza:
    __FEE_FACTOR = 0.000725
    __DEADLINE_PRICE = 10**6
    # TODO: اگر موقع نقد شدن به قیمت اسمی کارمزد ندارد کارمزد حساب نکن
    DEADLINE_PRICE_AFTER_FEE = (1 - __FEE_FACTOR) * __DEADLINE_PRICE
    # DEADLINE_PRICE is normalized with the transaction fee factor
    
    COLUMN_HEADERS = 'benefit_factor | name | deadline_date | deadline_monthes'

    def __init__(self, name, price, base_symbol='اخزا'):
        self.name = name
        self.__current_price = price
        self.current_price_after_fee = (1 + self.__FEE_FACTOR) * self.__current_price
        date_digits = name.split('-')[-1]
        self.pay_date = self.__gat_date_from_digits(date_digits)
        self.base_symbol = base_symbol
    
    
    @staticmethod
    def __gat_date_from_digits(digits):
        digits = str(digits)
        year = int('14' + digits[:2])
        month = int(digits[2:4])
        day = int(digits[4:])
        
        date = jdatetime.date(year, month, day)
        return date
    

    @property
    def deadline_days(self):
        now = jdatetime.date.today()
        delta = self.pay_date - now
        return delta.days
    
    
    @property
    def is_expired(self):
        return self.deadline_days <= 0
    

    @property
    def __benefit_factor_after_fee(self):
        # before_fee = self.__DEADLINE_PRICE / self.__current_price
        return self.DEADLINE_PRICE_AFTER_FEE / self.current_price_after_fee
    

    @property
    def annualized_benefit_percent(self):
        annualized_factor = (self.__benefit_factor_after_fee)**(365/self.deadline_days)
        annualized_percent = (annualized_factor-1)*100
        return annualized_percent


    @staticmethod
    def __normalize_percent(percent):
        percent *= 100
        percent = int(percent)
        percent = str(percent)
        percent = percent[:2] + '.' + percent[2:]
        return percent


    def __str__(self, deadline_by_day=False):
        monthes = str(self.deadline_days//30)
        name_items = [8*' ' + self.__normalize_percent(self.annualized_benefit_percent) + '%',
                      self.name.split('-')[0].replace('اخزا', '').replace(' ', '') + ' ',
                      ' ' + str(self.pay_date).replace('-', '/') + '  ',
                      str(monthes)]
        preview = ' | '.join(name_items)
        if deadline_by_day:
            s = (4-len(str(self.deadline_days))) * ' '
            preview += (4-len(monthes))*' ' + f'| {self.deadline_days}{s} days'
        return preview
