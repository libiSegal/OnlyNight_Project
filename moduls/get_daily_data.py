import datetime
import time

import pandas as pd
from datetime import date

import schedule

from dbConnections import sql_queries as sql_connection
from moduls.beProApi import bepro_api


def get_dates_in_year():
    return list(pd.date_range(date.today(), date(date.today().year, 12, 31), freq='D'))


def get_search_setting():
    search_settings_list = []
    for row in sql_connection.select_search_setting():
        search_settings_list.append({"id": row[0], "search_key": row[1], "stars": row[2]})
    return search_settings_list


def get_daily_data():
    dates = get_dates_in_year()
    search_settings = get_search_setting()
    for search_setting in search_settings[1:]:
        async_loop(dates, search_setting)


def async_loop(dates, search_setting):
    print(search_setting)
    for day in dates:
        print(day)
        next_day_date = day + datetime.timedelta(days=1)
        import time
        start_time = time.time()
        bepro_api.search_hotels("hotels", search_setting.get("id"), search_setting.get("search_key"),
                                search_setting.get("stars"), day, next_day_date)
        end_time = time.time()
        print(end_time - start_time)


# schedule.every().day.at('00:00').do(get_daily_data())
# while True:
#     schedule.run_pending()
#     time.sleep(1)

get_daily_data()
