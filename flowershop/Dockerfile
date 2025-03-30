# Используем Python-образ
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app/

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Создаем папку для статических файлов, если её нет
RUN mkdir -p /app/bot_tools

# Сборка статики
RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8080

# Запускаем бота
CMD ["sh", "-c", "gunicorn flowershop.wsgi:application --bind 0.0.0.0:$PORT & python manage.py start_bot"]
