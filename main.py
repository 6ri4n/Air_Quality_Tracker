# air quality api project

import mysql.connector
import requests
import json
import time

def connect_to_db():
    # TODO - connects to the 'cne340_finalproject' database
    con = mysql.connector.connect(
        user = 'root',
        password = '',
        host = '127.0.0.1',
        database = 'cne340_finalproject'
    )
    return con

def create_db_table(cursor):
    # TODO - creates a table in the 'cne340_finalproject' database
    pass

def query(cursor, query):
    # TODO - executes a query statement to a table in the 'cne340_finalproject' database
    cursor.execute(query)
    return cursor

def load_api_data():
    # TODO - sends a http request method (a get request) to the api
    api_key = '{INSERT API KEY HERE}'
    url = f'http://api.airvisual.com/v2/city?city=Renton&state=Washington&country=USA&key={api_key}'
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def graph():
    # TODO -
    #   graphs the air quality for the week and current month
    #   and saves an image of the graph in a folder (overrides previous saves)
    columns = ['Week', 'Month']

def add_to_table(cursor, data):
    # TODO - adds a row into a table in the 'cne340_finalproject' database
    pass

def work():
    # TODO - main loop of the script
    pass

def main():
    con = connect_to_db()
    cursor = con.cursor()
    create_db_table(cursor)
    print('>> script: active')

    #while True:
        # TODO -
        #   work
        #   graph

        # 3600 seconds = 1 hour
        #time.sleep(10)

if __name__ == '__main__':
    main()
