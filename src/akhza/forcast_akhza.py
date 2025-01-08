import finpy_tse as fpy
import pandas as pd
import jdatetime

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from src.akhza.akhza import Akhza
from src.utils.chart import Chart
from settings import ACTIVE_AKHZA_LIST, ACTIVE_AKHZA_DEADLINE_DAYS, Address


# fpy.Build_PricePanel(
#     ACTIVE_AKHZA_LIST,
#     jalali_date=True,
#     save_excel=True,
#     save_path=Address.FINPY_TSE_RESULTS)


def gat_date_from_digits(digits):
    digits = str(digits)
    year = int('14' + digits[:2])
    month = int(digits[2:4])
    day = int(digits[4:])
    
    date = jdatetime.date(year, month, day)
    return date


all_charts = []

for akhza_name, akhza_deadline_days in zip(ACTIVE_AKHZA_LIST, ACTIVE_AKHZA_DEADLINE_DAYS):
    akhza_df = pd.read_excel(f'{Address.FINPY_TSE_RESULTS}/{akhza_name}.xlsx')
    print(akhza_name, ' --- ', akhza_deadline_days)
    columns = akhza_df.columns
    
    chart = Chart(name=akhza_name, symbol=akhza_name)
    chart.__setattr__('deadline_days', akhza_deadline_days)
    for index, row in akhza_df.iterrows():
        chart.add_candle(first=row['Open'],
                         close=row['Close'],
                         high=row['High'],
                         low=row['Low'],
                         date=row['J-Date'])
    
    all_charts.append(chart)


print(all_charts[0].deadline_days)
