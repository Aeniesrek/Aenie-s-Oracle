import random
from flask import Flask, render_template, request
import hashlib
from datetime import date
import urllib.parse

app = Flask(__name__)

import random

# 運勢の種類
prefixes = ["大吉", "吉", "中吉", "小吉", "末吉", "凶"]

# prefix用の形容詞をエピックとトリビアルに分割
epic_prefix_adjectives = [
    "究極の", "極限の", "激烈な", "無限の", "狂気の", 
    "炸裂する", "燃え上がる", "超絶の", "衝撃的な", "天才的な", "壮大な"
]
trivial_prefix_adjectives = [
    "わけわからん", "かわいい", "頭おかしい", "しょーもない", "くだらない", "茶番な"
]

# 本文で使用する形容詞をエピックとトリビアルに分割
epic_adjectives = [
    "銀河の", "時空を超えた", "神々しい", "壮麗な", "無限の", 
    "天空の", "神秘的な", "超越した", "宇宙的な", "伝説の"
]
trivial_adjectives = [
    "くだらない", "しょぼい", "茶番の", "雑な", "ボロボロの", 
    "なんでもない", "つまらない", "ふにゃふにゃの", "安っぽい"
]

# コネクタ（形容詞同士を連続的にブレンドするための接続詞）
connectors = ["でありながらも", "かつ", "と共に", "ながら", "の両面を持つ", "融合した", "一方で", "そして"]

# その他、本文用の要素
nouns = [
    "奇跡", "運命", "未来", "星々", "伝説", "光",
    "情熱", "嵐", "革命", "英雄伝説", "宇宙", "神話",
    "おにぎり", "バナナ", "靴下", "ペットボトル", "コーヒー",
    "ゴミ", "電球", "雑誌", "スマホ", "鉛筆", "日常"
]

verbs = [
    "舞い上がる", "炸裂する", "煌めく", "咲き誇る", "燃え上がる",
    "輝く", "轟く", "駆け抜ける", "昇天する", "啓示する",
    "グニャグニャする", "ゆるゆるする", "チラリと光る", "ポロリと落ちる", "のそのそ歩く",
    "ダラダラする", "グルグル回る", "もたもたする", "ぼんやりする", "おっとりする"
]

exclamations = [
    # 壮大な感動
    "！全宇宙が祝福する！", "！運命の扉が開かれる！", "！輝く奇跡が訪れる！",
    "！時空が交錯する！", "！無限の力を感じる！", "！壮大な物語が始まる！",
    "！奇跡が連鎖する！", "！未来がここに刻まれる！", "！すべてが奇跡に染まる！",
    # しょーもない感じ
    "！なんだか微妙だね…", "！まあ、こんな感じ？", "！今日はごく普通かも！",
    "！どうせいつも通り！", "！ぼんやりした一日だね！", "！ふーん、そうかもね！"
]

templates = [
    "今日という日が、{adj}{noun}の如く{verb}{excl}",
    "星々が瞬く中、{adj}{noun}が{verb}{excl}",
    "運命の波が、{adj}{noun}の如く{verb}、あなたを包み込む{excl}",
    "{adj}{noun}が突如現れ、{verb}瞬間が訪れる{excl}",
    "世界がざわめく中、{adj}{noun}が{verb}、新たな伝説が始まる{excl}",
    "神秘的な{adj}{noun}が、あなたに{verb}未来を示す{excl}",
    "全ての星が揺れる夜、{adj}{noun}が{verb}、運命が再構築される{excl}",
    "闇夜に光る{adj}{noun}が、ひとしずくの希望となり、{verb}！",
    "時の彼方から{adj}{noun}が降臨し、{verb}瞬間を創り出す{excl}",
    "嵐のような{adj}{noun}が、心の奥深くで{verb}、未知なる旅が始まる{excl}"
]

# 連続的な形容詞を生成する関数（エピックとトリビアルの両側面をブレンド）
def generate_continuous_adjective():
    """
    確率50%で単一の形容詞、またはエピックとトリビアルな形容詞をコネクタで融合した複合表現を返す。
    """
    if random.random() < 0.5:
        # 複合表現
        connector = random.choice(connectors)
        if random.random() < 0.5:
            # エピック → トリビアルの順
            return random.choice(epic_adjectives) + connector + random.choice(trivial_adjectives)
        else:
            # トリビアル → エピックの順
            return random.choice(trivial_adjectives) + connector + random.choice(epic_adjectives)
    else:
        # 単一の形容詞（エピックとトリビアルの混合）
        return random.choice(epic_adjectives + trivial_adjectives)

def generate_continuous_prefix_adjective():
    """
    運勢の種類に付く形容詞も、確率50%で単一またはエピックとトリビアルを融合した表現で生成する。
    """
    if random.random() < 0.5:
        connector = random.choice(connectors)
        if random.random() < 0.5:
            return random.choice(epic_prefix_adjectives) + connector + random.choice(trivial_prefix_adjectives)
        else:
            return random.choice(trivial_prefix_adjectives) + connector + random.choice(epic_prefix_adjectives)
    else:
        return random.choice(epic_prefix_adjectives + trivial_prefix_adjectives)

def generate_fortune():
    # 運勢の種類（例："究極のかつかわいい大吉" や "しょーもないと共に激烈な凶" など）
    prefix = random.choice(prefixes)
    prefix_adj = generate_continuous_prefix_adjective()
    full_prefix = f"{prefix_adj}{prefix}"
    # 本文の形容詞は連続的に生成
    adj = generate_continuous_adjective()
    noun = random.choice(nouns)
    verb = random.choice(verbs)
    excl = random.choice(exclamations)
    template = random.choice(templates)
    message = template.format(adj=adj, noun=noun, verb=verb, excl=excl)
    return f"{full_prefix}：{message}"

# 2000パターンの運勢メッセージを生成
fortunes = [generate_fortune() for _ in range(2000)]


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