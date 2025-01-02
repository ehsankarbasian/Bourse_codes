class _Candle:
    
    def __init__(self, first, close, high, low, date):
        validate_high = self.__validate_high_is_biggest(first, close, high, low)
        validate_low = self.__validate_low_is_smallest(first, close, high, low)
        self.is_valid = validate_high and validate_low

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


class Chart:
    
    def __init__(self, name, symbol=None):
        self.name = name
        self.symbol = symbol
        self.__candles = []
    
    def append_candle(self, first, close, high, low, date):
        candle = _Candle(first, close, high, low, date)
        if candle.is_valid:
            self.__candles.append(candle)
