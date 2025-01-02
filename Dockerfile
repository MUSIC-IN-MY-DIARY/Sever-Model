FROM python:3.9-slim-buster

WORKDIR /app

# pip 먼저 업그레이드
RUN pip install --no-cache-dir --upgrade pip

COPY .env .env
COPY service/ .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]