FROM python:3.12-slim

WORKDIR /app

# FlaskとGunicornのインストール
RUN pip install flask gunicorn

COPY . /app

EXPOSE 5000

# Gunicornを使ってFlaskアプリを起動
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]