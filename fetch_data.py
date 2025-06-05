import requests
import psycopg2
from datetime import datetime
import time

# PostgreSQL connection info
conn_info = {
    'host': 'localhost',
    'port': 5432,
    'user': 'crypto_user',      
    'password': 'XXX',  
    'dbname': 'crypto_data'     
}

def fetch_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,dogecoin",
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)
    return response.json()

def insert_data(data):
    conn = psycopg2.connect(**conn_info)
    cursor = conn.cursor()

    for coin, value in data.items():
        price = value['usd']
        timestamp = datetime.now()
        cursor.execute(
            "INSERT INTO crypto_prices (timestamp, coin, price) VALUES (%s, %s, %s)",
            (timestamp, coin, price)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted at {timestamp}")

if __name__ == "__main__":
    while True:
        data = fetch_data()
        insert_data(data)
        time.sleep(10)
