import csv
from os import listdir

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from src.akhza.akhza import Akhza


ARCHIVE_DIR = 'data/expired_akhza'

expired_akhza_files = listdir(ARCHIVE_DIR)
for file_name in expired_akhza_files:
    with open(ARCHIVE_DIR + '/' + file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                date = row[1]
                first = row[2]
                close = row[5]
                high = row[3]
                low = row[4]
                open_ = row[-1]
