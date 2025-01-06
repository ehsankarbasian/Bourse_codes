import finpy_tse as fpy

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from settings import ACTIVE_AKHZA_LIST, Address


fpy.Build_PricePanel(
    ACTIVE_AKHZA_LIST,
    jalali_date=True,
    save_excel=True,
    save_path=Address.FINPY_TSE_RESULTS)
