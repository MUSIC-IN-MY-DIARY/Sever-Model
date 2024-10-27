FROM python:3.8-slim-buster

WORKDIR /app

COPY .env /app/.env

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "main.py"]