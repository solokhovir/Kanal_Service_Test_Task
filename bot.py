import asyncio
import os
import time
import telegram
from datetime import datetime
import google_sheets
import gspread
from dotenv import load_dotenv
from telegram.error import TelegramError

load_dotenv()
# Токен бота в Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID чата, куда будут отправляться уведомления
CHAT_ID = os.getenv("CHAT_ID")

# Создание объекта бота
bot = telegram.Bot(token=BOT_TOKEN)

CLIENT = gspread.authorize(google_sheets.creds)


async def send_notification(product_name, delivery_date):
    # Отправляет уведомление о просроченной поставке в Telegram.
    message = f'Заказ № "{product_name}" должен был быть доставлен {delivery_date}, но срок уже прошел.'
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except TelegramError as e:
        print(f"Ошибка отправки уведомления в Telegram: {e}")


async def check_delivery_dates():
    # Проверяет сроки поставки для каждой записи в таблице.
    worksheet = CLIENT.open_by_key('19pUZNGNTkiphOKn6WPsyvrDWLSsnnLTuwRuurcct9V0').get_worksheet(0)
    records = worksheet.get_all_records()
    for record in records:
        if record['срок поставки']:
            delivery_date = datetime.strptime(record['срок поставки'], '%d.%m.%Y')
        else:
            delivery_date = None
        if delivery_date and delivery_date.date() < datetime.today().date():
            await send_notification(record['заказ №'], record['срок поставки'])
            # asyncio.create_task(send_notification(record['заказ №'], record['срок поставки']))
    print("Проверка сроков поставки завершена.")


async def main():
    while True:
        await check_delivery_dates()
        time.sleep(30)

if __name__ == '__main__':
    asyncio.run(main())