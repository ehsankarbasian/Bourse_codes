import datetime


class _Candle:
    
    def __init__(self, first, close, high, low, date):
        try:
            first = int(first.split('.')[0])
            close = int(close.split('.')[0])
            high = int(high.split('.')[0])
            low = int(low.split('.')[0])
        except:
            pass
        
        validate_high = self.__validate_high_is_biggest(first, close, high, low)
        validate_low = self.__validate_low_is_smallest(first, close, high, low)
        self.is_valid = validate_high and validate_low
        
        if self.is_valid:
            year = int(date[:4])
            month = date[4:6]
            day = date[6:]
            if month[0] == '0':
                month = month.replace('0', '')
            if day[0] == '0':
                day = day.replace('0', '')
            month = int(month)
            day = int(day)
            date = datetime.date(year, month, day)
        
        self.open = first #open
        self.close = close
        self.high = high
        self.low = low
        self.date = date
    
    @staticmethod
    def __validate_high_is_biggest(first, close, high, low):
        return max([first, close, high, low]) == high
    
    @staticmethod
    def __validate_low_is_smallest(first, close, high, low):
        return min([first, close, high, low]) == low
    
    @property
    def mean_price(self):
        return (self.open + self.close + self.high + self.low) / 4


class Chart:
    
    def __init__(self, name, symbol=None):
        self.file_name = name
        self.symbol = symbol
        self.__candles = []
    
    def add_candle(self, first, close, high, low, date):
        candle = _Candle(first, close, high, low, date)
        if candle.is_valid:
            self.__candles = [candle] + self.__candles
    
    @property
    def __duration(self):
        first_candle = self.__candles[0]
        last_candle = self.__candles[-1]
        delta = last_candle.date - first_candle.date
        return delta.days
    
    
    @property
    def annualized_benefit_percent(self):
        FEE_FACTOR = 0.000725
        
        first_price = self.__candles[0].mean_price
        first_price += FEE_FACTOR * first_price
        # TODO: اگر موقع نقد شدن به قیمت اسمی کارمزد ندارد کارمزد حساب نکن
        last_price = self.__candles[-1].mean_price
        last_price = (1-FEE_FACTOR) * last_price
        
        benefit_factor = last_price / first_price
        annualized_factor = benefit_factor ** (365/self.__duration)
        annualized_percent = (annualized_factor-1)*100
        
        return annualized_percent
