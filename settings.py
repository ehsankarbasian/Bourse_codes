
#
UPDATE_MODE = False


# Excel data archive
ARCHIVE_DATA_DIR = 'data/expired_akhza'


# File addresses
class Address:
    AKHZA_ACTIVE_URLS = 'results/Akhza/active_akhza_urls.txt'
    AKHZA_ACTIVE_LIST = 'results/Akhza/active_akhza_list.txt'
    AKHZA_SORTED_BENEFIT = 'results/Akhza/sorted_by_benefit.txt'
    AKHZA_SORTED_DEADLINE = 'results/Akhza/sorted_by_deadline.txt'
    
    FINPY_TSE_RESULTS = 'results/finpy_tse'

PREDICTOR_DIRECTORY = f'{Address.FINPY_TSE_RESULTS}/predictor'


# INACTIVE and AKCIVE Akhza lists
INACTIVE_AKHZA_LIST = []
ACTIVE_AKHZA_LIST = []
ACTIVE_AKHZA_DEADLINE_DAYS = []
with open(Address.AKHZA_ACTIVE_LIST) as active_akhza:
    for line in active_akhza.readlines():
        line = line.replace('\n', '').split('-')
        ACTIVE_AKHZA_LIST.append(line[0])
        ACTIVE_AKHZA_DEADLINE_DAYS.append(int(line[1]))
