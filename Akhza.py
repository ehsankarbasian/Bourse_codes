import jdatetime


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
