import os
import time
from datetime import datetime
import google_sheets
import psycopg2
import requests
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
SPREAD_SHEET_ID = os.getenv("SPREAD_SHEET_ID")

while True:
    # Получение данных из Google Sheets
    service = build('sheets', 'v4', credentials=google_sheets.creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREAD_SHEET_ID, range='Лист1').execute()
    rows = result.get('values')
    print(rows)

    # Получение данных с Банка России
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    data = response.content.decode('windows-1251')
    usd_rate = float(data.split('<Valute ID="R01235">')[1].split('<Value>')[1].split('</Value>')[0].replace(',', '.'))

    # Создание соединения с базой данных
    conn = psycopg2.connect(dbname="orders", user="postgres", password="1234", host="localhost", port="5432")
    cur = conn.cursor()

    # Получение последней записи в таблице
    cur.execute("SELECT MAX(num) FROM order_info_1")
    max_id = cur.fetchone()[0]

    if max_id is None:
        max_id = 0

    for i, row in enumerate(rows):
        if i == 0:
            row.append('стоимость в руб.')
        else:
            row.append(float(row[2].replace('$', '')) * usd_rate)
        if i > max_id:
            cur.execute("INSERT INTO order_info (num, order_num, cost_usd, delivery_date, cost_rub) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (row[0], row[1], row[2],
                         datetime.strptime(row[3], '%d.%m.%Y').date(),
                         row[4]))

    conn.commit()

    cur.close()
    conn.close()
    time.sleep(15)