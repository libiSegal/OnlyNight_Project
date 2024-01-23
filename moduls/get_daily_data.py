import pandas as pd
import datetime
from datetime import date
from moduls.beProApi import bepro_api

def dates_in_year():
    dates = pd.date_range(date.today(), date(date.today().year, 12, 31), freq='D')
    dates = list(dates)
    return dates

def get_search_setting():
    pass
def get_daily_data():
    dates = dates_in_year()
    for date in dates:
        next_day_date = datetime.datetime.today() + datetime.timedelta(days=1)
        serch_settings_from_db = get_search_setting()
        bepro_api.search_hotels()




