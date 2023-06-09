Разработанный скрипт на языке Python 3 выполняет следующие функции:

1. Получает данные с документа при помощи Google API.

2. Данные добавляются в БД, в том же виде, что и в файле–источнике, с добавлением колонки «стоимость в руб.». Данные для перевода $ в рубли необходимо получать по курсу [ЦБ РФ](https://www.cbr.ru/development/SXML/).
    
3. Скрипт работает постоянно для обеспечения обновления данных в онлайн режиме (необходимо учитывать, что строки в Google Sheets таблицу могут удаляться, добавляться и изменяться).

4. Разработан функционал проверки соблюдения «срока поставки» из таблицы. В случае, если срок прошел, скрипт отправляет уведомление в Telegram.

Запуск происходит следующим образом:
1. google_sheets.py;
Получение данных с документа
```sh
python google_sheets.py
```
2. main.py;
Добавление данных в базу PostgreSQL
```sh
python main.py
```
3. bot.py;
Запуск бота для отправки уведомлений в Telegram
```sh
python bot.py
```

Docker-контейнеры:
1. Контейнер для авторизации в Google Sheets
```sh
docker push solokhovir/google_sheets:latest
```

2. Контейнер для записи данных в базу
```sh
docker push solokhovir/main:latest
```

3. Контейнер для запуска проверки просроченных поставок
```sh
docker push solokhovir/bot:latest
```