import csv
from os import listdir

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from src.utils.chart import Chart


ARCHIVE_DIR = 'data/expired_akhza'
charts = []


def initialize_chart(file_name):
    chart = Chart(name=file_name)
    with open(ARCHIVE_DIR + '/' + file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            date = row[1]
            first = row[2]
            close = row[5]
            high = row[3]
            low = row[4]
            open_ = row[-1]
            chart.append_candle(open_, close, high, low, date)
    
    return chart


expired_akhza_files = listdir(ARCHIVE_DIR)
for file_name in expired_akhza_files:
    chart = initialize_chart(file_name)
    charts.append(chart)
