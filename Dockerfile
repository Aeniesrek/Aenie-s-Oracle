FROM python:3.12-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール
RUN pip install streamlit

# アプリのソースコードをコピー
COPY . /app

# Streamlitのデフォルトポート
EXPOSE 8501

# Streamlitの起動コマンドを指定
CMD ["streamlit", "run", "main.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
