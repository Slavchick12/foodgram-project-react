FROM python:3.7.4-slim

WORKDIR /app

COPY requirements.txt .

RUN apt update && \
    apt upgrade -y && \
    python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn==20.0.4

COPY . .

CMD ["gunicorn", "foodgram.wsgi", "-t", "600", "-b", "0.0.0.0:8000"]
