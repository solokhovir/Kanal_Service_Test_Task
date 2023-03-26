# Установка базового образа Python
FROM python:3.9

# Копирование файлов проекта в Docker-контейнер
COPY . /app

# Установка зависимостей проекта
RUN pip install -r /app/requirements.txt

 # Запуск приложения при запуске контейнера
 CMD ["python", "/app/bot.py"]

# Запуск приложения при запуске контейнера
CMD ["python", "/app/google_sheets.py"]

 # Запуск приложения при запуске контейнера
 CMD ["python", "/app/main.py"]