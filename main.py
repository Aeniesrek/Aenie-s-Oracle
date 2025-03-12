import streamlit as st
import hashlib
import os
from datetime import date
import urllib.parse

# 運勢リスト
fortunes = [
    "大吉：最高の一日になります！",
    "吉：いいことがあるでしょう。",
    "中吉：普通に良い日です。",
    "小吉：何気ない幸せを感じられる日。",
    "末吉：落ち着いて過ごしましょう。",
    "凶：慎重に過ごしてください。",
]

# IPアドレス取得（Streamlitクラウド環境でも取得可能）
from streamlit.runtime.scriptrunner import get_script_run_ctx

def get_remote_ip():
    ctx = st.runtime.scriptrunner.get_script_run_ctx()
    if ctx := getattr(ctx, 'client', None):
        return ctx.request.remote_ip
    return "unknown"

def get_fortune(ip_address: str, date_today: str) -> str:
    combined = f"{ip_address}-{date_today}"
    hash_value = hashlib.sha256(combined.encode()).hexdigest()
    fortune_index = int(hash_value, 16) % len(fortunes)
    return fortunes[fortune_index]

# 本日の取得
today = date.today().strftime("%Y-%m-%d")

# ユーザーのIPアドレスを取得し、運勢を算出
user_ip = get_remote_ip()
fortune = get_fortune(user_ip, today)

# Streamlitで表示
st.title("🌟今日のあなたの運勢🌟")
st.write(f"日付：{today}")
st.header(f"{fortune}")
st.caption("ページを再読み込みしても、今日の運勢は変わりません。")

# ツイート用テキストの生成
tweet_text = f"今日の運勢: {fortune} (日付: {today}) #運勢 #今日の運勢"
encoded_text = urllib.parse.quote(tweet_text)
twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}"

# FontAwesomeのTwitterアイコンを用いたツイートボタンのHTMLコード
tweet_icon_html = f'''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<div style="margin-top:20px;">
    <a href="{twitter_url}" target="_blank" style="text-decoration:none;">
        <i class="fab fa-twitter" style="font-size:48px; color:#1DA1F2;"></i>
    </a>
</div>
'''

st.markdown(tweet_icon_html, unsafe_allow_html=True)

# CSS を利用して上部のメニューを非表示にする
hide_streamlit_style = """
    <style>
    /* 三点リーダ（ハンバーガーメニュー）の非表示 */
    #MainMenu {visibility: hidden;}
    /* ヘッダー全体（デプロイボタン含む）の非表示 */
    header {visibility: hidden;}
    /* フッターも非表示にする場合 */
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
