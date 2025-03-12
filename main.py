from flask import Flask, render_template, request
import hashlib
from datetime import date
import urllib.parse

app = Flask(__name__)

# 運勢リスト
fortunes = [
    "大吉：最高の一日になります！",
    "吉：いいことがあるでしょう。",
    "中吉：普通に良い日です。",
    "小吉：何気ない幸せを感じられる日。",
    "末吉：落ち着いて過ごしましょう。",
    "凶：慎重に過ごしてください。",
]

def get_fortune(ip_address: str, date_today: str) -> str:
    combined = f"{ip_address}-{date_today}"
    hash_value = hashlib.sha256(combined.encode()).hexdigest()
    fortune_index = int(hash_value, 16) % len(fortunes)
    return fortunes[fortune_index]

@app.route("/")
def index():
    today = date.today().strftime("%Y-%m-%d")
    # クライアントのIPアドレス取得（プロキシ環境の場合は注意）
    user_ip = request.remote_addr or "unknown"
    fortune = get_fortune(user_ip, today)
    
    # ツイート用テキストと現在のページURLを取得
    tweet_text = f"今日の運勢: {fortune} (日付: {today}) #運勢 #今日の運勢"
    encoded_text = urllib.parse.quote(tweet_text)
    page_url = "https://aenie-s-oracle-585411739425.asia-northeast1.run.app/"
    encoded_url = urllib.parse.quote(page_url)
    twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}&url={encoded_url}"
    
    return render_template("index.html", today=today, fortune=fortune, twitter_url=twitter_url)

if __name__ == "__main__":
    app.run(debug=True)