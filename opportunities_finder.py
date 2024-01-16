# this function will work every day
def opportunities_finder(segment):
    months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
              'NOVEMBER', 'DECEMBER']
    for month in months:
        currently_price_for_segment = api(month, segment)
        history_price = get_historical_price(month, segment)
        profit_margin = calculate_profit_margin(currently_price_for_segment, history_price)
        return profit_margin


# calculate the profit by rules
def calculate_profit_margin(currently_price_for_segment, history_price):
    pass


# get the historical price form the db
def get_historical_price(month, segment):
    pass


# get the current price by apies
def api(month, segment):
    pass


# get the segment id from the db by segment name
def get_segment_id(segment):
    pass
