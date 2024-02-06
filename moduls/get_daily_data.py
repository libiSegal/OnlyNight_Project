import asyncio
import nest_asyncio
import datetime
import pandas as pd
from datetime import date
from dbConnections import sql_queries as sql_connection
from moduls.beProApi import bepro_api

nest_asyncio.apply()


def dates_in_year():
    dates = pd.date_range(date.today(), date(date.today().year, 12, 31), freq='D')
    dates = list(dates)
    return dates


def get_search_setting():
    search_settings = sql_connection.select_search_setting()
    search_settings_list = []
    for row in search_settings:
        print(row)
        search_settings_list.append({"search_key": row[0], "stars": row[1]})
    return search_settings_list


def get_daily_data():
    dates = dates_in_year()
    search_settings = get_search_setting()
    loop = asyncio.get_event_loop()
    for search_setting in search_settings:
        async_loop(dates, search_setting)


def async_loop(dates, search_setting):
    for day in dates:
        print(day)
        next_day_date = day + datetime.timedelta(days=1)
        import time
        start_time = time.time()
        bepro_api.search_hotels("hotels", search_setting.get("search_key"), search_setting.get("stars"), day,
                                next_day_date)
        end_time = time.time()
        print(end_time - start_time)


# asyncio.run(get_daily_data())
get_daily_data()

# 492355
# 16:24
