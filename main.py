import random
from flask import Flask, render_template, request,send_from_directory
import hashlib
from datetime import date
import urllib.parse

app = Flask(__name__, static_folder="static")



import random

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

def generate_combat_power(text: str) -> str:
    # 入力文字列の SHA-256 ハッシュ値を整数に変換し、乱数の種とする
    h = hashlib.sha256(text.encode()).hexdigest()
    seed = int(h, 16)
    random.seed(seed)
    
    # 基本単位：10^0 ～ 10^68
    basic_units = [
        ("一(いち)", 0),
        ("十(じゅう)", 1),
        ("百(ひゃく)", 2),
        ("千(せん)", 3),
        ("万(まん)", 4),
        ("億(おく)", 8),
        ("兆(ちょう)", 12),
        ("京(けい)", 16),
        ("垓(がい)", 20),
        ("𥝱(じょ)", 24),
        ("穣(じょう)", 28),
        ("溝(こう)", 32),
        ("澗(かん)", 36),
        ("正(せい)", 40),
        ("載(さい)", 44),
        ("極(ごく)", 48),
        ("恒河沙(ごうがしゃ)", 52),
        ("阿僧祇(あそうぎ)", 56),
        ("那由他(なゆた)", 60),
        ("不可思議(ふかしぎ)", 64),
        ("無量大数(むりょうたいすう)", 68)
    ]
    
    # 拡張単位：基本単位よりもさらに大きい値（各値は「10の○乗」として解釈）
    extended_units = [
        ("矜羯羅(こんがら)", 112),
        ("阿伽羅(あから)", 224),
        ("最勝(さいしょう)", 448),
        ("摩婆羅(まばら)", 896),
        ("阿婆羅(あばら)", 1792),
        ("多婆羅(たばら)", 3584),
        ("界分(かいぶん)", 7168),
        ("普摩(ふま)", 14336),
        ("禰摩(ねま)", 28672),
        ("阿婆鈐(あばけん)", 57344),
        ("弥伽婆(みかば)", 114688),
        ("毘攞伽(びらか)", 229376),
        ("毘伽婆(びかば)", 458752),
        ("僧羯邏摩(そうがらま)", 917504),
        ("毘薩羅(びさら)", 1835008),
        ("毘贍婆(びせんば)", 3670016),
        ("毘盛伽(びじょうが)", 7340032),
        ("毘素陀(びすだ)", 14680064),
        ("毘婆訶(びばか)", 29360128),
        ("毘薄底(びばてい)", 58720256),
        ("毘佉擔(びきゃたん)", 117440512),
        ("称量(しょうりょう)", 234881024),
        ("一持(いちじ)", 469762048),
        ("異路(いろ)", 939524096),
        ("顛倒(てんどう)", 1879048192),
        ("三末耶(さんまや)", 3758096384),
        ("毘睹羅(びとら)", 7516192768),
        ("奚婆羅(けいばら)", 15032385536),
        ("伺察(しさつ)", 30064771072),
        ("周広(しゅうこう)", 60129542144),
        ("高出(こうしゅつ)", 120259084288),
        ("最妙(さいみょう)", 240518168576),
        ("泥羅婆(ないらば)", 481036337152),
        ("訶理婆(かりば)", 962072674304),
        ("一動(いちどう)", 1924145348608),
        ("訶理蒲(かりぼ)", 3848290697216),
        ("訶理三(かりさん)", 7696581394432),
        ("奚魯伽(けいろか)", 15393162788864),
        ("達攞歩陀(たつらほだ)", 30786325577728),
        ("訶魯那(かろな)", 61572651155456),
        ("摩魯陀(まろだ)", 123145302310912),
        ("懺慕陀(ざんぼだ)", 246290604621824),
        ("瑿攞陀(えいらだ)", 492581209243648),
        ("摩魯摩(まろま)", 985162418487296),
        ("調伏(ちょうぶく)", 1970324836974592),
        ("離憍慢(りきょうまん)", 3940649673949184),
        ("不動(ふどう)", 7881299347898368),
        ("極量(ごくりょう)", 15762598695796736),
        ("阿麼怛羅(あまたら)", 31525197391593472),
        ("勃麼怛羅(ぼまたら)", 63050394783186944),
        ("伽麼怛羅(がまたら)", 126100789566373888),
        ("那麼怛羅(なまたら)", 252201579132747776),
        ("奚麼怛羅(けいまたら)", 504403158265495552),
        ("鞞麼怛羅(べいまたら)", 1008806316530991104),
        ("鉢羅麼怛羅(はらまたら)", 2017612633061982208),
        ("尸婆麼怛羅(しばまたら)", 4035225266123964416),
        ("翳羅(えいら)", 8070450532247928832),
        ("薜羅(べいら)", 16140901064495857664),
        ("諦羅(たいら)", 32281802128991715328),
        ("偈羅(げら)", 64563604257983430656),
        ("窣歩羅(そほら)", 129127208515966861312),
        ("泥羅(ないら)", 258254417031933722624),
        ("計羅(けいら)", 516508834063867445248),
        ("細羅(さいら)", 1033017668127734890496),
        ("睥羅(へいら)", 2066035336255469780992),
        ("謎羅(めいら)", 4132070672510939561984),
        ("娑攞荼(しゃらだ)", 8264141345021879123968),
        ("謎魯陀(めいろだ)", 16528282690043758247936),
        ("契魯陀(けいろだ)", 33056565380087516495872),
        ("摩睹羅(まとら)", 66113130760175032991744),
        ("娑母羅(しゃもら)", 132226261520350065983488),
        ("阿野娑(あやしゃ)", 264452523040700131966976),
        ("迦麼羅(かまら)", 528905046081400263933952),
        ("摩伽婆(まかば)", 1057810092162800527867904),
        ("阿怛羅(あたら)", 2115620184325601055735808),
        ("醯魯耶(けいろや)", 4231240368651202111471616),
        ("薜魯婆(べいろば)", 8462480737302404222943232),
        ("羯羅波(からは)", 16924961474604808445886464),
        ("訶婆婆(かばば)", 33849922949209616891772928),
        ("毘婆羅(びばら)", 67699845898419233783545856),
        ("那婆羅(なばら)", 135399691796838467567091712),
        ("摩攞羅(まらら)", 270799383593676935134183424),
        ("娑婆羅(しゃばら)", 541598767187353870268366848),
        ("迷攞普(めいらふ)", 1083197534374707740536733696),
        ("者麼羅(しゃまら)", 2166395068749415481073467392),
        ("駄麼羅(だまら)", 4332790137498830962146934784),
        ("鉢攞麼陀(はらまだ)", 8665580274997661924293869568),
        ("毘迦摩(びかま)", 17331160549995323848587739136),
        ("烏波跋多(うはばた)", 34662321099990647697175478272),
        ("演説(えんぜつ)", 69324642199981295394350956544),
        ("無尽(むじん)", 138649284399962590788701913088),
        ("出生(しゅっしょう)", 277298568799925181577403826176),
        ("無我(むが)", 554597137599850363154807652352),
        ("阿畔多(あばんた)", 1109194275199700726309615304704),
        ("青蓮華(しょうれんげ)", 1109194275199700726309615304704),
        ("鉢頭摩(はどま)", 1109194275199700726309615304704),
        ("僧祇(そうぎ)", 8873554201597605810476922437632),
        ("趣(しゅ)", 17747108403195211620953844875264),
        ("至(し)", 35494216806390423241907689750528),
        ("阿僧祇(あそうぎ)", 70988433612780846483815379501056),
        ("阿僧祇転(あそうぎてん)", 141976867225561692967630759002112),
        ("無量(むりょう)", 283953734451123385935261518004224),
        ("無量転(むりょうてん)", 567907468902246771870523036008448),
        ("無辺(むへん)", 1135814937804493543741046072016896),
        ("無辺転(むへんてん)", 2271629875608987087482092144033792),
        ("無等(むとう)", 4543259751217974174964184288067584),
        ("無等転(むとうてん)", 9086519502435948349928368576135168),
        ("不可数(ふかすう)", 18173039004871896699856737152270336),
        ("不可数転(ふかすうてん)", 36346078009743793399713474304540672),
        ("不可称(ふかしょう)", 72692156019487586799426948609081344),
        ("不可称転(ふかしょうてん)", 145384312038975173598853897218162688),
        ("不可思(ふかし)", 290768624077950347197707794436325376),
        ("不可思転(ふかしてん)", 581537248155900694395415588872650752),
        ("不可量(ふかりょう)", 1163074496311801388790831177745301504),
        ("不可量転(ふかりょうてん)", 2326148992623602777581662355490603008),
        ("不可説(ふかせつ)", 4652297985247205555163324710981206016),
        ("不可説転(ふかせつてん)", 9304595970494411110326649421962412032),
        ("不可説不可説(ふかせつふかせつ)", 18609191940988822220653298843924824064),
        ("不可説不可説転(ふかせつふかせつてん)", 37218383881977644441306597687849648128)
    ]
    
    # 小数単位：10^-1 ～ 10^-24
    fractional_units = [
        ("分(ぶ)", -1),
        ("厘(りん)", -2),
        ("毛(もう)", -3),
        ("糸(し)", -4),
        ("忽(こつ)", -5),
        ("微(び)", -6),
        ("繊(せん)", -7),
        ("沙(しゃ)", -8),
        ("塵(じん)", -9),
        ("埃(あい)", -10),
        ("渺(びょう)", -11),
        ("漠(ばく)", -12),
        ("模糊(もこ)", -13),
        ("逡巡(しゅんじゅん)", -14),
        ("須臾(しゅゆ)", -15),
        ("瞬息(しゅんそく)", -16),
        ("弾指(だんし)", -17),
        ("刹那(せつな)", -18),
        ("六徳(りっとく)", -19),
        ("虚空(こくう)", -20),
        ("清浄(しょうじょう)", -21),
        ("阿頼耶(あらや)", -22),
        ("阿摩羅(あまら)", -23),
        ("涅槃寂静(ねはんじゃくじょう)", -24)
    ]
    
    # すべての単位を 1 つのリストに統合
    all_units = basic_units + extended_units + fractional_units
    
    # その中からランダムにひとつ選ぶ（同じ入力なら同じ結果になります）
    chosen_unit = random.choice(all_units)
    coef = random.randint(1, 9)
    
    return f"{coef}{chosen_unit[0]} (10の{chosen_unit[1]}乗)"


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
    power = generate_combat_power(fortune)
    # ツイート用テキストと現在のページURLを取得
    tweet_text = f"今日の運勢: {fortune} 戦闘力:{power} (日付: {today}) #運勢 #今日の運勢"
    encoded_text = urllib.parse.quote(tweet_text)
    page_url = "https://aenie-s-oracle-585411739425.asia-northeast1.run.app/"
    encoded_url = urllib.parse.quote(page_url)
    twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}&url={encoded_url}"

    return render_template("index.html", 
                           today=today, 
                           fortune=fortune, 
                           twitter_url=twitter_url, 
                           power=power)

if __name__ == "__main__":
    app.run(debug=True)