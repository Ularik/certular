FROM python:3.12-slim

# 1. Устанавливаем системные зависимости В САМОМ НАЧАЛЕ
# и сразу очищаем кэш apt для уменьшения размера образа
RUN apt-get update && apt-get install -y --no-install-recommends \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# 2. Обновляем pip
RUN python -m pip install --upgrade pip

# 3. Задаем рабочую директорию (она создастся автоматически)
WORKDIR /usr/www

# 4. Сначала копируем ТОЛЬКО requirements.txt и ставим зависимости
# Это позволит Docker использовать кэш и не переустанавливать библиотеки при изменении кода
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Создаем нужные папки под медиа и логи
RUN mkdir -p logs media

# 6. Копируем исходный код проекта
COPY . .

# EXPOSE 8000

# 7. Команда запуска приложения (раскомментируйте и подставьте свою)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

