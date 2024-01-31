import datetime
import pandas as pd
from datetime import date
from dbConnections import basic_sql_queries as sql_connection
from moduls.beProApi import bepro_api


def dates_in_year():
    dates = pd.date_range(date.today(), date(date.today().year, 12, 31), freq='D')
    dates = list(dates)
    return dates


def get_search_setting():
    search_settings = sql_connection.select_search_setting()
    search_settings_list = []
    for row in search_settings:
        search_settings_list.append({"search_key": row[0], "stars": row[1]})
    return search_settings_list


def get_daily_data():
    dates = dates_in_year()
    search_settings = get_search_setting()
    for search_setting in search_settings:
        for day in dates:
            next_day_date = day + datetime.timedelta(days=1)
            bepro_api.search_hotels(search_setting.get("search_key"), search_setting.get("stars"), day, next_day_date)


get_daily_data()
