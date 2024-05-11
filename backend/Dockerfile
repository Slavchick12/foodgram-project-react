FROM python:3.7.4-buster
WORKDIR /foodgram
COPY requirements.txt .
RUN apt update && \
    apt upgrade -y && \
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn==20.0.4
COPY . .
ENTRYPOINT ["make", "run"]
