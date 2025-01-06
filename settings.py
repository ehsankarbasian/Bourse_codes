
# Excel data archive
ARCHIVE_DATA_DIR = 'data/expired_akhza'


# File addresses
class Address:
    AKHZA_ACTIVE_LIST = 'results/Akhza/active_akhza_list.txt'
    AKHZA_SORTED_BENEFIT = 'results/Akhza/sorted_by_benefit.txt'
    AKHZA_SORTED_DEADLINE = 'results/Akhza/sorted_by_deadline.txt'


# INACTIVE and AKCIVE Akhza lists
INACTIVE_AKHZA_LIST = []
ACTIVE_AKHZA_LIST = []
with open(Address.AKHZA_ACTIVE_LIST) as active_akhza:
    for line in active_akhza.readlines():
        ACTIVE_AKHZA_LIST.append(line.replace('\n', ''))
