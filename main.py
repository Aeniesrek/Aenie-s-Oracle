import streamlit as st
import hashlib
from datetime import date
import os

fortunes = [
    "大吉：今日は絶好調！何をやってもうまくいきます。",
    "吉：今日はいい日です。前向きに過ごしましょう。",
    "中吉：穏やかな一日になりそうです。",
    "小吉：少し気をつけて行動すると良いでしょう。",
    "末吉：無理せず静かに過ごすのがおすすめです。",
    "凶：慎重に行動してください。"
]

# IPアドレス取得（Streamlitクラウド環境でも取得可能）
from streamlit.runtime.scriptrunner import get_script_run_ctx

def get_remote_ip():
    ctx = st.runtime.scriptrunner.get_script_run_ctx()
    if ctx := getattr(ctx, 'client', None):
        return ctx.request.remote_ip
    return "unknown"

def get_fortune(ip_address: str, date_today: str) -> str:
    import hashlib
    combined = f"{ip_address}-{date_today}"
    hash_value = hashlib.sha256(combined.encode()).hexdigest()
    fortune_index = int(hash_value, 16) % len(fortunes)
    return fortunes[fortune_index]

# Streamlitアプリの実装例
import streamlit as st
from datetime import date

# 運勢リスト
fortunes = [
    "大吉：最高の一日になります！",
    "吉：いいことがあるでしょう。",
    "中吉：普通に良い日です。",
    "小吉：何気ない幸せを感じられる日。",
    "末吉：落ち着いて過ごしましょう。",
    "凶：慎重に過ごしてください。",
]

# 本日の取得
today = date.today().strftime("%Y-%m-%d")

# ユーザーのIPアドレスを取得
ip_address = get_fortune(get_remote_ip(), today)

fortune = get_fortune(ip_address, today)

# Streamlit で表示
import streamlit as st
st.title("🌟今日のあなたの運勢🌟")
st.write(f"日付：{today}")
st.header(f"{fortune}")

st.caption("ページを再読み込みしても、今日の運勢は変わりません。")


