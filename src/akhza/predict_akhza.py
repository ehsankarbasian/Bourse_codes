import finpy_tse as fpy
import jdatetime

from pandas import read_excel

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from src.akhza.akhza import Akhza
from src.utils.chart import ChartToPredict
from src.utils.directory_tools import make_folder_empty
from settings import ACTIVE_AKHZA_LIST, ACTIVE_AKHZA_DEADLINE_DAYS, PREDICTOR_DIRECTORY, UPDATE_MODE


if UPDATE_MODE:
    make_folder_empty(PREDICTOR_DIRECTORY)
    fpy.Build_PricePanel(
        ACTIVE_AKHZA_LIST,
        jalali_date=True,
        save_excel=True,
        save_path=PREDICTOR_DIRECTORY)


all_charts = []

for akhza_name, akhza_deadline_days in zip(ACTIVE_AKHZA_LIST, ACTIVE_AKHZA_DEADLINE_DAYS):
    akhza_df = read_excel(f'{PREDICTOR_DIRECTORY}/{akhza_name}.xlsx')
    columns = akhza_df.columns
    
    chart = ChartToPredict(name=akhza_name,
                           deadline_days=akhza_deadline_days,
                           deadline_price=Akhza.DEADLINE_PRICE_AFTER_FEE)
    for index, row in akhza_df.iterrows():
        chart.add_candle(first=row['Open'],
                         close=row['Close'],
                         high=row['High'],
                         low=row['Low'],
                         date=row['J-Date'])
    
    all_charts.append(chart)
    print(chart.name)
    print(chart.tomorrow_price_prediction)
