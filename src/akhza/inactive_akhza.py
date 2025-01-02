import csv
from os import listdir

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from src.utils.chart import Chart
from src.utils.normalizer import normalize_percent


ARCHIVE_DIR = 'data/expired_akhza'
charts = []


def initialize_chart(file_name):
    chart = Chart(name=file_name)
    with open(ARCHIVE_DIR + '/' + file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            date = row[1]
            first = row[2].replace(' ', '')
            close = row[5].replace(' ', '')
            high = row[3].replace(' ', '')
            low = row[4].replace(' ', '')
            open_ = row[-1].replace(' ', '')
            chart.add_candle(open_, close, high, low, date)
    
    return chart


def get_chart_benefit(chart):
    return chart.annualized_benefit_percent


expired_akhza_files = listdir(ARCHIVE_DIR)
for file_name in expired_akhza_files:
    chart = initialize_chart(file_name)
    charts.append(chart)
    
charts.sort(key=get_chart_benefit)
for chart in charts:
    annualized_benefit_percent = chart.annualized_benefit_percent
    print(normalize_percent(annualized_benefit_percent), '%', '|', chart.file_name)
