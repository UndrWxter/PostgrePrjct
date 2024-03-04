# Используйте официальный образ Python в качестве базового образа
FROM python:3.9

# Устанавливаем переменную среды для отключения вывода байт-кодов Python
ENV PYTHONDONTWRITEBYTECODE 1

# Устанавливаем переменную среды для запуска в режиме не в интерактивном режиме
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код Django проекта в контейнер
COPY . .

# Опционально, выполняем миграции или другие команды
RUN python manage.py makemigrations
RUN python manage.py migrate

# Определяем порт, который будет использоваться внутри контейнера
EXPOSE 8000

# Запускаем сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
