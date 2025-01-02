
def normalize_percent(percent):
    percent *= 100
    percent = int(percent)
    percent = str(percent)
    percent = percent[:2] + '.' + percent[2:]
    return percent
