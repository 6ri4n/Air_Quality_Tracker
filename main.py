# air quality tracker for the city of Renton

import mysql.connector
import requests
import json
import time
import calendar
import pandas as pd
import matplotlib.pyplot as plt

def connect_to_db():
    # TODO - connects to the 'AQI' database
    con = mysql.connector.connect(
        user = 'root',
        password = '',
        host = '127.0.0.1',
        database = 'AQI'
    )
    return con

def create_db_table(cursor):
    # TODO - creates a table named 'Renton' with a date and aqi column
    # date string value
    # aqi int value
    # create table if it doesn't exist
    q = '''CREATE TABLE IF NOT EXISTS Renton(date VARCHAR(15), aqi INT);'''
    query(cursor, q)

def query(cursor, query):
    # TODO - executes a query statement
    cursor.execute(query)
    return cursor

def load_api_data():
    # TODO - sends a http request method (a get request) to the api
    # https://aqicn.org/api/
    # https://aqicn.org/json-api/doc/#api-_
    api_key = '{INSERT API KEY HERE}'
    url = f'https://api.waqi.info/feed/Renton/?token={api_key}'
    response = requests.get(url)
    return json.loads(response.text)

def parse_date(dict):
    # TODO -
    #   creates a new dictionary
    #   reformat the date keys to only store the day (date keys excludes the year and month)
    parsed_dict = {}
    for key, value in dict.items():
        parsed_key = key[-2:]
        if parsed_key[0] == '0':
            parsed_key = parsed_key[1]
        parsed_dict[parsed_key] = value
    return parsed_dict

def graph(cursor, data):
    # TODO -
    #   graphs the air quality for the week and current month
    #   and saves an image of the graph (overrides previous saves)
    for key in data.keys():
        date = key
    title_year = date[:4]
    num_month_before = date[5:7]

    # TODO - convert into integer and remove leading zero
    if num_month_before[0] == '0':
        num_month_after = int(num_month_before[-1])
    else:
        num_month_after = int(num_month_before)
    title_month = calendar.month_name[num_month_after]

    week_dict = parse_date(data)
    graph_dict = {
        'Week': week_dict
    }

    # TODO - query for current month aqi
    q = f'SELECT date FROM Renton WHERE date LIKE \'{title_year}-{num_month_before}-%\' LIMIT 31'
    cur = query(cursor, q)
    fetch_key_list = cur.fetchall()
    key_list = []
    for key in fetch_key_list:
        key_list.append(key[0])

    q = f'SELECT aqi FROM Renton WHERE date LIKE \'{title_year}-{num_month_before}-%\' LIMIT 31'
    cur = query(cursor, q)
    fetch_value_list = cur.fetchall()
    value_list = []
    for value in fetch_value_list:
        value_list.append(value[0])

    month_dict = dict(zip(key_list, value_list))
    month_dict = parse_date(month_dict)
    graph_dict['Month'] = month_dict

    # TODO - create data structures for graph
    week = pd.Series(graph_dict["Week"].values(), index = graph_dict["Week"].keys())
    month = pd.Series(graph_dict["Month"].values(), index = graph_dict["Month"].keys())
    df1 = pd.DataFrame({'Week': week})
    df2 = pd.DataFrame({'Month': month})

    # TODO - create graph
    fig, graph = plt.subplots(nrows = 2, ncols = 1, figsize = [10, 8])
    df1.plot(ax = graph[0], marker = '.', markersize = 10, color = 'tab:orange')
    df2.plot(ax = graph[1], marker = '.', markersize = 10, color = 'tab:blue')
    graph[0].set(title = 'Average PM2.5 For The Week')
    graph[1].set(title = 'PM2.5 For The Month', xlabel = 'Day', ylabel = 'PM2.5')
    graph[1].yaxis.set_label_coords(-.08, 1.1)
    graph[1].xaxis.set_label_coords(.5, -0.18)
    fig.suptitle(f'Air Quality for {title_month} {title_year}', fontsize = 18, y = .95)
    fig.savefig('aqi_visual.png')

def add_to_table(cursor, data):
    # TODO - adds a row into the 'Renton' table
    # parse data - data is a dictionary
    for keys in data.keys():
        current_date = keys
    for values in data.values():
        current_aqi = values
    cursor.execute(
    'INSERT INTO Renton (date, aqi)'
    'VALUES (%s, %s)', (current_date, current_aqi)
)

def parse_forecast_data(api_data):
    # TODO - parses api_data for date and average pm25 and adds them to forcasted_dict
    forcasted_dict = {}
    forecast_data = api_data['data']['forecast']['daily']['pm25']
    for row in forecast_data:
        forcasted_dict[row['day']] = row['avg']
    return forcasted_dict

def check_if_day_exist(cursor, date):
    # TODO -
    #   returns true or false if the current day exist in the 'Renton' table
    q = f"SELECT date FROM Renton WHERE date = \'{date}\'"
    cursor = query(cursor, q)
    # fetchone returns None if no rows are retrieved
    if cursor.fetchone() is None:
        # the date is new
        return False
    # fetchone returns a row
    else:
        # the date exist in the table
        return True

def work(cursor):
    # parse api data (current and forecast) -
    api_data = load_api_data()
    current_aqi = api_data['data']['aqi']
    current_date = api_data['data']['time']['s'][:10]

    # use parse_forecasts_data to retrieve the current week's average aqi
    forcasted_dict = parse_forecast_data(api_data)

    # add current data to the 'Renton' table (only if the day hasn't been added yet)
    if not check_if_day_exist(cursor, current_date):
        add_to_table(cursor, {current_date: current_aqi})

    # pass the forcasted_dict into graph
    graph(cursor, forcasted_dict)

def main():
    con = connect_to_db()
    cursor = con.cursor()
    create_db_table(cursor)
    print('>> script: active')

    while True:
        work(cursor)
        # 21600 seconds = 6 hours
        time.sleep(21600)

if __name__ == '__main__':
    main()
