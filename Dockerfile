FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# В контейнере у нас папка /app/output, где будут CSV-файлы
RUN mkdir -p /app/output

# ENTRYPOINT вместо CMD, чтобы параметры можно было передавать напрямую:
ENTRYPOINT ["python", "parser.py"]
