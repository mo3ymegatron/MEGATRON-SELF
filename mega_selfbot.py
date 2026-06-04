import asyncio
import datetime
import time
import jdatetime
import os
import json
import random
import re
import threading
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired

# ═══════════════════════════════════════
# ⚙️ تنظیمات اصلی
# ═══════════════════════════════════════
API_ID = 30479174
API_HASH = "f7116f16ed02b404785a4cfe8d2468d3"
BOT_TOKEN = "8925694222:AAFF3AF44idSIvfb9LHEqucyEBr0UJOBFvE"
OWNER_USERNAME = "Mo3y_MEGATRON"

# ═══════════════════════════════════════
# 🤖 کلاینت‌ها
# ═══════════════════════════════════════
main_self = Client("mega_self", api_id=API_ID, api_hash=API_HASH)
bot_client = Client("mega_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ═══════════════════════════════════════
# 📂 فایل‌ها
# ═══════════════════════════════════════
FRIENDS_FILE = "friends.json"
ENEMIES_FILE = "enemies.json"
REPLIES_FILE = "replies.txt"
MAHVI_FILE = "mahvi.txt"
SETTINGS_FILE = "settings.json"
CHATTED_USERS_FILE = "chatted_users.json"
SUBSCRIBERS_FILE = "subscribers.json"
USER_SESSIONS_FILE = "user_sessions.json"
BACKUP_FILE = "backup.json"
REPORT_LOG_FILE = "report_log.json"

def load_list(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_list(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(filename, default={}):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_replies():
    if os.path.exists(REPLIES_FILE):
        try:
            with open(REPLIES_FILE, "r", encoding="utf-8-sig") as f:
                return [line.strip() for line in f if line.strip()]
        except UnicodeDecodeError:
            with open(REPLIES_FILE, "r", encoding="cp1256") as f:
                return [line.strip() for line in f if line.strip()]
    return [f"جواب {i}" for i in range(1, 301)]

def save_replies(reply_list):
    with open(REPLIES_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(reply_list))

def load_mahvi():
    if os.path.exists(MAHVI_FILE):
        try:
            with open(MAHVI_FILE, "r", encoding="utf-8-sig") as f:
                return [line.strip() for line in f if line.strip()]
        except UnicodeDecodeError:
            with open(MAHVI_FILE, "r", encoding="cp1256") as f:
                return [line.strip() for line in f if line.strip()]
    return [f"محوی {i}" for i in range(1, 101)]

def save_mahvi(mahvi_list):
    with open(MAHVI_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(mahvi_list))

def backup_data():
    data = {
        "friends": friends,
        "enemies": enemies,
        "settings": settings,
        "subscribers": subscribers,
        "chatted_users": chatted_users,
        "timestamp": str(datetime.datetime.now())
    }
    save_json(BACKUP_FILE, data)
    print("🛟 پشتیبان خودکار انجام شد!")
    return True

def restore_backup():
    global friends, enemies, settings, subscribers, chatted_users
    data = load_json(BACKUP_FILE)
    if data:
        friends = data.get("friends", [])
        enemies = data.get("enemies", [])
        settings = data.get("settings", {})
        subscribers = data.get("subscribers", [])
        chatted_users = data.get("chatted_users", [])
        save_list(FRIENDS_FILE, friends)
        save_list(ENEMIES_FILE, enemies)
        save_list(SUBSCRIBERS_FILE, subscribers)
        save_list(CHATTED_USERS_FILE, chatted_users)
        save_json(SETTINGS_FILE, settings)
        return True
    return False

def auto_backup_loop():
    while True:
        time.sleep(1800)
        try:
            backup_data()
        except Exception as e:
            print(f"⚠️ خطا در پشتیبان خودکار: {e}")

def log_report(reporter_id, target_id, chat_id):
    reports = load_json(REPORT_LOG_FILE, [])
    reports.append({
        "reporter": reporter_id,
        "target": target_id,
        "chat": chat_id,
        "time": str(datetime.datetime.now())
    })
    save_json(REPORT_LOG_FILE, reports)
    print(f"⚠️ ریپورت تشخیص داده شد! گزارش‌دهنده: {reporter_id}")

# ═══════════════════════════════════════
# 🎨 سیستم فونت‌ها (۲۰ فونت)
# ═══════════════════════════════════════

FONTS = {
    1: {
        "name": "𝗕𝗼𝗹𝗱",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
    },
    2: {
        "name": "𝐼𝑡𝑎𝑙𝑖𝑐",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧0123456789"
    },
    3: {
        "name": "𝑩𝒐𝒍𝒅 𝑰𝒕𝒂𝒍𝒊𝒄",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛0123456789"
    },
    4: {
        "name": "𝙼𝚘𝚗𝚘𝚜𝚙𝚊𝚌𝚎",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"
    },
    5: {
        "name": "𝒞𝓊𝓇𝓈𝒾𝓋𝑒",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏0123456789"
    },
    6: {
        "name": "🅂🅀🅄🄰🅁🄴",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "fancy": "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉"
    },
    7: {
        "name": "ⓒⓘⓡⓒⓛⓔ",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨"
    },
    8: {
        "name": "S̶t̶r̶i̶k̶e̶",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "A̶B̶C̶D̶E̶F̶G̶H̶I̶J̶K̶L̶M̶N̶O̶P̶Q̶R̶S̶T̶U̶V̶W̶X̶Y̶Z̶a̶b̶c̶d̶e̶f̶g̶h̶i̶j̶k̶l̶m̶n̶o̶p̶q̶r̶s̶t̶u̶v̶w̶x̶y̶z̶0̶1̶2̶3̶4̶5̶6̶7̶8̶9̶"
    },
    9: {
        "name": "丂ㄥ卂几ㄒ",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "卂乃匚刀乇千厶卄丨丁长乚从𠘨口尸㔿尺丂丅凵リ山乂丫乙卂乃匚刀乇千厶卄丨丁长乚从𠘨口尸㔿尺丂丅凵リ山乂丫乙0123456789"
    },
    10: {
        "name": "𝕯𝖔𝖚𝖇𝖑𝖊",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟0123456789"
    },
    11: {
        "name": "ᵗⁱⁿʸ",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᵠᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹"
    },
    12: {
        "name": "uʍopǝpᴉsd∩",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "∀𐐒ƆᗡƎℲ⅁HIſ⋊⅂WNOԀΌᴚS⊥∩ΛMX⅄Zɐqɔpǝɟɓɥᴉɾʞʃɯuodbɹsʇnʌʍxʎz0ƖᄅƐㄣϛ9ㄥ86"
    },
    13: {
        "name": "🅑🅤🅑🅑🅛🅔",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "fancy": "ⒷⓊⒷⒷⓁⒺⒷⓊⒷⒷⓁⒺⒷⓊⒷⒷⓁⒺⒷⓊⒷⒷⓁⒺⒷⓊⒷⒷⓁⒺⒷⓊⒷⒷⓁⒺⒷⓊⒷⒷⓁⒺⒷⓊⒷⒷⓁⒺ"
    },
    14: {
        "name": "𝔐𝔢𝔡𝔦𝔢𝔳𝔞𝔩",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷0123456789"
    },
    15: {
        "name": "Fαɳƈყ",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "ค๒ς๔єŦﻮђเןкɭ๓ภ๏קợгรՇยשฬאץչค๒ς๔єŦﻮђเןкɭ๓ภ๏קợгรՇยשฬאץչ0123456789"
    },
    16: {
        "name": "𝒮𝒸𝓇𝒾𝓅𝓉",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "fancy": "𝒜𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏"
    },
    17: {
        "name": "𝕲𝖔𝖙𝖍𝖎𝖈",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷0123456789"
    },
    18: {
        "name": "𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"
    },
    19: {
        "name": "G̷l̷i̷t̷c̷h̷",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "A̷B̷C̷D̷E̷F̷G̷H̷I̷J̷K̷L̷M̷N̷O̷P̷Q̷R̷S̷T̷U̷V̷W̷X̷Y̷Z̷a̷b̷c̷d̷e̷f̷g̷h̷i̷j̷k̷l̷m̷n̷o̷p̷q̷r̷s̷t̷u̷v̷w̷x̷y̷z̷0̷1̷2̷3̷4̷5̷6̷7̷8̷9̷"
    },
    20: {
        "name": "M҉a҉g҉i҉c҉",
        "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "A҉B҉C҉D҉E҉F҉G҉H҉I҉J҉K҉L҉M҉N҉O҉P҉Q҉R҉S҉T҉U҉V҉W҉X҉Y҉Z҉a҉b҉c҉d҉e҉f҉g҉h҉i҉j҉k҉l҉m҉n҉o҉p҉q҉r҉s҉t҉u҉v҉w҉x҉y҉z҉0҉1҉2҉3҉4҉5҉6҉7҉8҉9҉"
    }
}

def apply_font(text: str, font_id: int) -> str:
    if font_id not in FONTS:
        return text
    font = FONTS[font_id]
    result = ""
    for char in text:
        if char in font["normal"]:
            idx = font["normal"].index(char)
            result += font["fancy"][idx]
        else:
            result += char
    return result

def get_font_list_text():
    text = "🎨 **لیست فونت‌های موجود:**\n\n"
    for num, font in FONTS.items():
        text += f"{num}. {font['name']}\n"
    text += "\n📝 **لطفاً شماره فونت مورد نظر رو بفرست:**"
    return text

# بارگذاری داده‌ها
friends = load_list(FRIENDS_FILE)
enemies = load_list(ENEMIES_FILE)
replies = load_replies()
mahvi_replies = load_mahvi()
settings = load_json(SETTINGS_FILE, {
    "press_mode": False,
    "dragon_mode": False,
    "aggressive_mode": False,
    "anti_link": False,
    "kal_mode": False,
    "tiz_mode": False,
    "tiz_text": "",
    "self_active": True,
    "destroyer_mode": False,
    "mahvi_mode": False,
    "fire_mode": False,
    "font_mode": False,
    "active_font": 1
})
chatted_users = load_list(CHATTED_USERS_FILE)
subscribers = load_list(SUBSCRIBERS_FILE)
user_sessions = load_json(USER_SESSIONS_FILE, {})

# حافظه موقت
enemy_messages = {}
last_enemy_message = {}
last_active_group = None
temp_login_data = {}
user_clients = {}
font_selecting = {}

# راه‌اندازی پشتیبان‌گیر
backup_thread = threading.Thread(target=auto_backup_loop, daemon=True)
backup_thread.start()
print("🛟 سیستم پشتیبان‌گیر فعال شد (هر ۳۰ دقیقه)")

# ═══════════════════════════════════════
# 🛠️ توابع کمکی
# ═══════════════════════════════════════

def is_owner(user):
    if not user:
        return False
    return user.username and user.username.lower() == OWNER_USERNAME.lower()

def has_access(user):
    if not user:
        return False
    if is_owner(user):
        return True
    if user.username and user.username.lower() in [s.lower() for s in subscribers]:
        return True
    return False

async def mega_reply(message: Message, text: str, count: int = 8, delay: float = 0.05):
    if settings.get("font_mode") and settings.get("active_font"):
        text = apply_font(text, settings["active_font"])
    for i in range(count):
        try:
            await message.reply_text(text)
            await asyncio.sleep(delay)
        except FloodWait as e:
            print(f"⚠️ FloodWait: {e.x}s")
            await asyncio.sleep(e.x)

async def fire_reply(message: Message, text: str, count: int = 8):
    if settings.get("font_mode") and settings.get("active_font"):
        text = apply_font(text, settings["active_font"])
    tasks = [message.reply_text(text) for _ in range(count)]
    await asyncio.gather(*tasks, return_exceptions=True)

async def fire_message(chat_id: int, text: str, count: int = 10):
    if settings.get("font_mode") and settings.get("active_font"):
        text = apply_font(text, settings["active_font"])
    tasks = [main_self.send_message(chat_id, text) for _ in range(count)]
    await asyncio.gather(*tasks, return_exceptions=True)

async def destroyer_reply(message: Message, text: str):
    if settings.get("font_mode") and settings.get("active_font"):
        text = apply_font(text, settings["active_font"])
    await mega_reply(message, f"💥 {text}", count=50, delay=0.03)

async def mahvi_reply(message: Message):
    text = random.choice(mahvi_replies)
    if settings.get("font_mode") and settings.get("active_font"):
        text = apply_font(text, settings["active_font"])
    for _ in range(2):
        try:
            await message.reply_text(f"🌫️ {text}")
            await asyncio.sleep(0.5)
        except FloodWait as e:
            await asyncio.sleep(e.x)

async def is_admin(chat_id, user_id):
    try:
        member = await main_self.get_chat_member(chat_id, user_id)
        return member.status in ["creator", "administrator"]
    except:
        return False

def has_link(text):
    if not text:
        return False
    url_pattern = r'https?://\S+|www\.\S+|t\.me/\S+'
    return bool(re.search(url_pattern, text))

async def notify_in_group(user_first_name):
    global last_active_group
    if last_active_group:
        try:
            msg = f"📢 با سلام، بنده سلف مصی مگاترون هستم.\n👤 **{user_first_name}** شما یک پیام در پیوی خود دارید!"
            if settings.get("font_mode") and settings.get("active_font"):
                msg = apply_font(msg, settings["active_font"])
            await main_self.send_message(last_active_group, msg)
        except:
            pass

async def send_command_menu(client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 مشخصات", callback_data="cmd_profile"),
         InlineKeyboardButton("📊 وضعیت", callback_data="cmd_status")],
        [InlineKeyboardButton("📅 تاریخ", callback_data="cmd_date"),
         InlineKeyboardButton("🔍 جستجوی آهنگ", callback_data="cmd_search_info")],
        [InlineKeyboardButton("🤝 تنظیم دوست", callback_data="cmd_friend_info"),
         InlineKeyboardButton("💀 تنظیم دشمن", callback_data="cmd_enemy_info")],
        [InlineKeyboardButton("🔥 تهاجمی", callback_data="cmd_aggressive"),
         InlineKeyboardButton("💥 نابودگر", callback_data="cmd_destroyer")],
        [InlineKeyboardButton("🔄 فشاری", callback_data="cmd_press"),
         InlineKeyboardButton("🐉 اژدها", callback_data="cmd_dragon")],
        [InlineKeyboardButton("🌫️ محوی", callback_data="cmd_mahvi"),
         InlineKeyboardButton("🔗 ضد لینک", callback_data="cmd_antilink")],
        [InlineKeyboardButton("⚡ فایر", callback_data="cmd_fire"),
         InlineKeyboardButton("🎨 فونت", callback_data="cmd_font_menu")],
        [InlineKeyboardButton("🛟 پشتیبان", callback_data="cmd_backup"),
         InlineKeyboardButton("🕐 کل", callback_data="cmd_kal_info")],
        [InlineKeyboardButton("✈️ تیز", callback_data="cmd_tiz_info"),
         InlineKeyboardButton("🟢 فعال سلف", callback_data="cmd_active")],
        [InlineKeyboardButton("😴 خاموش سلف", callback_data="cmd_deactive"),
         InlineKeyboardButton("🚪 خروج", callback_data="cmd_logout")]
    ])
    
    await message.reply_text(
        "🎉 **ورود موفقیت‌آمیز!**\n\n"
        "🔥 **سلف مصی مگاترون** 🔥\n\n"
        "📋 **منوی دستورات:**\n"
        "از دکمه‌ها یا متن استفاده کن 👇",
        reply_markup=keyboard
    )
    
# ═══════════════════════════════════════
# 🚫 استارت ربات
# ═══════════════════════════════════════

@bot_client.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user = message.from_user
    
    if not has_access(user):
        await message.reply_text(
            "🚫 **زهی خیال باطل مردک!**\n\n"
            "⛔ شما حق استفاده از این ربات را ندارید!\n\n"
            "👑 این ربات فقط برای افراد مجاز قابل استفاده است.\n"
            "📌 مالک: @Mo3y_MEGATRON"
        )
        return
    
    if is_owner(user):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔐 ورود به اکانت", callback_data="login_account")],
            [InlineKeyboardButton("👥 مدیریت مشترک‌ها", callback_data="subs_menu")],
            [InlineKeyboardButton("📊 وضعیت", callback_data="show_status")],
            [InlineKeyboardButton("❌ بستن", callback_data="close_menu")]
        ])
        await message.reply_text(
            "🔥 **سلف مصی مگاترون** 🔥\n\n"
            "👑 شما مالک هستید!\n\n"
            "از دکمه‌های زیر استفاده کنید:",
            reply_markup=keyboard
        )
        return
    
    if has_access(user):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔐 ورود به اکانت", callback_data="login_account")],
            [InlineKeyboardButton("📊 وضعیت", callback_data="show_status")],
            [InlineKeyboardButton("❌ بستن", callback_data="close_menu")]
        ])
        await message.reply_text(
            "🔥 **سلف مصی مگاترون** 🔥\n\n"
            "✅ شما مشترک هستید!\n\n"
            "از دکمه‌های زیر استفاده کنید:",
            reply_markup=keyboard
        )

# ═══════════════════════════════════════
# 📋 راهنما
# ═══════════════════════════════════════

@bot_client.on_message(filters.command("help"))
async def help_command(client, message: Message):
    if not has_access(message.from_user):
        await message.reply_text("🚫 زهی خیال باطل مردک! حق استفاده نداری.")
        return
    
    await message.reply_text(
        "🔥 **سلف مصی مگاترون** 🔥\n\n"
        "**دستورات عمومی:**\n"
        "`مشخصات` `تاریخ` `وضعیت` `جستجوی آهنگ X` `سیک`\n\n"
        "**دوستان و دشمنان:**\n"
        "`تنظیم دوست` `حذف دوست` `تنظیم دشمن` `حذف دشمن`\n\n"
        "**حالت‌های تهاجمی:**\n"
        "`حالت تهاجمی` / `حالت تهاجمی خاموش`\n"
        "`نابودگر روشن` / `نابودگر خاموش`\n"
        "`حالت فشاری` / `فشاری خاموش`\n"
        "`اژدهای مصی روشن` / `اژدها بخواب`\n"
        "`محوی روشن` / `محوی خاموش`\n\n"
        "**ابزارها:**\n"
        "`ضد لینک روشن` / `ضد لینک خاموش`\n"
        "`کل` / `نکل`\n"
        "`تیز متن` / `نفرسس`\n"
        "`فعال سلف` / `خاموش سلف`\n\n"
        "**🎨 فونت:**\n"
        "`فونت فعال` — انتخاب فونت\n"
        "`فونت خاموش` — غیرفعال کردن\n\n"
        "**سیستم:**\n"
        "`/start` — منوی اصلی\n"
        "`/logout` — خروج از اکانت\n"
        "`/subscribers` — مدیریت مشترک‌ها (مالک)\n"
        "`/edit_replies` — مدیریت جواب‌ها (مالک)"
    )

# ═══════════════════════════════════════
# 🎛️ مدیریت همه دکمه‌ها
# ═══════════════════════════════════════

@bot_client.on_callback_query()
async def handle_all_callbacks(client, callback_query: CallbackQuery):
    user = callback_query.from_user
    data = callback_query.data
    
    if data == "close_menu":
        await callback_query.message.delete()
        await callback_query.answer("✅ بسته شد")
        return
    
    if not has_access(user):
        await callback_query.answer("🚫 حق استفاده نداری!", show_alert=True)
        return
    
    if data == "show_status":
        me = await main_self.get_me()
        s = settings
        current_font = FONTS.get(s.get("active_font", 1), {}).get("name", "Bold")
        text = f"""
**⚡ وضعیت سلف مصی مگاترون ⚡**

👑 مالک: @{OWNER_USERNAME}
👤 اکانت: {me.first_name}
🆔 آیدی: `{me.id}`

👥 دوستان: {len(friends)} | 💀 دشمنان: {len(enemies)}
👤 مشترک‌ها: {len(subscribers)} | 🔐 آنلاین: {len(user_clients)}
💬 جواب‌ها: {len(replies)} | 🌫️ محوی: {len(mahvi_replies)}

🟢 سلف: {'✅' if s.get('self_active') else '😴 خاموش'}
🔥 تهاجمی: {'✅' if s.get('aggressive_mode') else '❌'}
💥 نابودگر: {'✅' if s.get('destroyer_mode') else '❌'}
🔄 فشاری: {'✅' if s.get('press_mode') else '❌'}
🐉 اژدها: {'✅' if s.get('dragon_mode') else '❌'}
🌫️ محوی: {'✅' if s.get('mahvi_mode') else '❌'}
🔗 ضدلینک: {'✅' if s.get('anti_link') else '❌'}
⚡ فایر: {'✅' if s.get('fire_mode') else '❌'}
🎨 فونت: {'✅ ' + current_font if s.get('font_mode') else '❌'}
🕐 کَل: {'✅' if s.get('kal_mode') else '❌'}
✈️ تیز: {'✅' if s.get('tiz_mode') else '❌'}
"""
        await callback_query.message.reply_text(text)
        await callback_query.answer("✅")
        return
    
    if data == "login_account":
        if user.username and user.username in user_sessions:
            await callback_query.message.reply_text(
                "ℹ️ شما قبلاً وارد اکانت شدید!\n"
                "برای خروج: `/logout`"
            )
            await callback_query.answer("ℹ️ قبلاً وارد شدید")
            return
        
        temp_login_data[user.id] = {
            "action": "login",
            "step": "phone",
            "username": user.username
        }
        
        await callback_query.message.reply_text(
            "📱 **ورود به اکانت تلگرام**\n\n"
            "📞 لطفاً شماره تلفن خود را با کد کشور وارد کنید:\n"
            "مثال: `989124416473`\n\n"
            "🚫 برای لغو: `/cancel`"
        )
        await callback_query.answer("✅")
        return
    
    if data == "subs_menu":
        if not is_owner(user):
            await callback_query.answer("❌ فقط مالک!", show_alert=True)
            return
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ اضافه کردن مشترک", callback_data="add_sub")],
            [InlineKeyboardButton("➖ حذف مشترک", callback_data="del_sub")],
            [InlineKeyboardButton("📋 لیست مشترک‌ها", callback_data="list_subs")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ])
        
        await callback_query.message.reply_text(
            "👥 **مدیریت مشترک‌ها**\n\n"
            f"👑 مالک: @{OWNER_USERNAME}\n"
            f"👥 تعداد مشترک‌ها: {len(subscribers)}",
            reply_markup=keyboard
        )
        await callback_query.answer("✅")
        return
    
    if data == "back_main":
        await start_command(client, callback_query.message)
        await callback_query.answer("✅")
        return
    
    if data == "add_sub":
        if not is_owner(user):
            await callback_query.answer("❌ فقط مالک!", show_alert=True)
            return
        
        temp_login_data[user.id] = {"action": "add_sub"}
        await callback_query.message.reply_text(
            "📝 **لطفاً یوزرنیم مشترک جدید رو بفرست:**\n"
            "مثال: `@username` یا `username`\n\n"
            "🚫 لغو: `/cancel`"
        )
        await callback_query.answer("✅")
        return
    
    if data == "del_sub":
        if not is_owner(user):
            await callback_query.answer("❌ فقط مالک!", show_alert=True)
            return
        
        if not subscribers:
            await callback_query.answer("📋 هیچ مشترکی نیست!", show_alert=True)
            return
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🗑️ @{s}", callback_data=f"delsub_{s}")]
            for s in subscribers
        ] + [[InlineKeyboardButton("🔙 بازگشت", callback_data="subs_menu")]])
        
        await callback_query.message.reply_text(
            "🗑️ **مشترک مورد نظر رو انتخاب کن:**",
            reply_markup=keyboard
        )
        await callback_query.answer("✅")
        return
    
    if data == "list_subs":
        if not is_owner(user):
            await callback_query.answer("❌ فقط مالک!", show_alert=True)
            return
        
        if not subscribers:
            await callback_query.answer("📋 هیچ مشترکی نیست!", show_alert=True)
        else:
            text = "📋 **لیست مشترک‌ها:**\n\n"
            for i, s in enumerate(subscribers, 1):
                text += f"{i}. @{s}\n"
            await callback_query.message.reply_text(text)
            await callback_query.answer("✅")
        return
    
    if data.startswith("delsub_"):
        username = data.replace("delsub_", "")
        if username in subscribers:
            subscribers.remove(username)
            save_list(SUBSCRIBERS_FILE, subscribers)
            await callback_query.message.reply_text(f"🗑️ @{username} از مشترک‌ها حذف شد!")
        await callback_query.answer("✅ حذف شد")
        return
    
    if data == "cmd_profile":
        me = await main_self.get_me()
        photos = await main_self.get_profile_photos("me", limit=1)
        text = f"👤 **{me.first_name}**\n🆔 `{me.id}`\n🏷️ @{me.username or 'ندارد'}\n📝 {me.bio or 'ندارد'}"
        if photos:
            await callback_query.message.reply_photo(photos[0].file_id, caption=text)
        else:
            await callback_query.message.reply_text(text)
        await callback_query.answer("✅")
        return
    
    if data == "cmd_status":
        me = await main_self.get_me()
        s = settings
        current_font = FONTS.get(s.get("active_font", 1), {}).get("name", "Bold")
        text = f"""
**⚡ وضعیت ⚡**

👤 {me.first_name} | 🆔 `{me.id}`
👥 دوستان: {len(friends)} | 💀 دشمنان: {len(enemies)}
🟢 سلف: {'✅' if s.get('self_active') else '😴'}
🔥 تهاجمی: {'✅' if s.get('aggressive_mode') else '❌'}
💥 نابودگر: {'✅' if s.get('destroyer_mode') else '❌'}
🔄 فشاری: {'✅' if s.get('press_mode') else '❌'}
🐉 اژدها: {'✅' if s.get('dragon_mode') else '❌'}
🌫️ محوی: {'✅' if s.get('mahvi_mode') else '❌'}
🔗 ضدلینک: {'✅' if s.get('anti_link') else '❌'}
⚡ فایر: {'✅' if s.get('fire_mode') else '❌'}
🎨 فونت: {'✅ ' + current_font if s.get('font_mode') else '❌'}
"""
        await callback_query.message.reply_text(text)
        await callback_query.answer("✅")
        return
    
    if data == "cmd_date":
        now = jdatetime.datetime.now()
        await callback_query.message.reply_text(f"☀️ {now.strftime('%Y/%m/%d')}\n📆 {now.strftime('%A')}\n🕐 {now.strftime('%H:%M:%S')}")
        await callback_query.answer("✅")
        return
    
    if data == "cmd_search_info":
        await callback_query.message.reply_text("🔍 **جستجوی آهنگ:**\n`جستجوی آهنگ اسم آهنگ`\nمثال: `جستجوی آهنگ Shadmehr`")
        await callback_query.answer("✅")
        return
    
    if data == "cmd_friend_info":
        await callback_query.message.reply_text("🤝 **تنظیم دوست:**\nروی پیام طرف ریپلای بزن و بنویس: `تنظیم دوست`")
        await callback_query.answer("✅")
        return
    
    if data == "cmd_enemy_info":
        await callback_query.message.reply_text("💀 **تنظیم دشمن:**\nروی پیام طرف ریپلای بزن و بنویس: `تنظیم دشمن`")
        await callback_query.answer("✅")
        return
    
    if data == "cmd_aggressive":
        settings["aggressive_mode"] = not settings.get("aggressive_mode", False)
        save_json(SETTINGS_FILE, settings)
        state = "✅ روشن" if settings["aggressive_mode"] else "❌ خاموش"
        await callback_query.message.reply_text(f"🔥 **تهاجمی:** {state}")
        await callback_query.answer(f"🔥 {state}")
        return
    
    if data == "cmd_destroyer":
        settings["destroyer_mode"] = not settings.get("destroyer_mode", False)
        save_json(SETTINGS_FILE, settings)
        state = "✅ روشن" if settings["destroyer_mode"] else "❌ خاموش"
        await callback_query.message.reply_text(f"💥 **نابودگر:** {state} (۵۰ بار)")
        await callback_query.answer(f"💥 {state}")
        return
    
    if data == "cmd_press":
        settings["press_mode"] = not settings.get("press_mode", False)
        save_json(SETTINGS_FILE, settings)
        state = "✅ روشن" if settings["press_mode"] else "❌ خاموش"
        await callback_query.message.reply_text(f"🔄 **فشاری:** {state}")
        await callback_query.answer(f"🔄 {state}")
        return
    
    if data == "cmd_dragon":
        settings["dragon_mode"] = not settings.get("dragon_mode", False)
        save_json(SETTINGS_FILE, settings)
        state = "✅ روشن" if settings["dragon_mode"] else "❌ خاموش"
        await callback_query.message.reply_text(f"🐉 **اژدها:** {state}")
        await callback_query.answer(f"🐉 {state}")
        return
    
    if data == "cmd_mahvi":
        settings["mahvi_mode"] = not settings.get("mahvi_mode", False)
        save_json(SETTINGS_FILE, settings)
        state = "✅ روشن" if settings["mahvi_mode"] else "❌ خاموش"
        await callback_query.message.reply_text(f"🌫️ **محوی:** {state}")
        await callback_query.answer(f"🌫️ {state}")
        return
    
    if data == "cmd_antilink":
        settings["anti_link"] = not settings.get("anti_link", False)
        save_json(SETTINGS_FILE, settings)
        state = "✅ روشن" if settings["anti_link"] else "❌ خاموش"
        await callback_query.message.reply_text(f"🔗 **ضد لینک:** {state}")
        await callback_query.answer(f"🔗 {state}")
        return
    
    if data == "cmd_fire":
        settings["fire_mode"] = not settings.get("fire_mode", False)
        save_json(SETTINGS_FILE, settings)
        state = "✅ روشن" if settings["fire_mode"] else "❌ خاموش"
        await callback_query.message.reply_text(f"⚡ **فایر:** {state}")
        await callback_query.answer(f"⚡ {state}")
        return
    
    if data == "cmd_font_menu":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎨 فعال کردن فونت", callback_data="font_activate")],
            [InlineKeyboardButton("❌ خاموش کردن فونت", callback_data="font_deactivate")],
            [InlineKeyboardButton("📋 لیست فونت‌ها", callback_data="font_list")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ])
        current_font = FONTS.get(settings.get("active_font", 1), {}).get("name", "Bold")
        await callback_query.message.reply_text(
            "🎨 **تنظیمات فونت**\n\n"
            f"📊 وضعیت: {'✅ فعال' if settings.get('font_mode') else '❌ غیرفعال'}\n"
            f"🔤 فونت فعال: {current_font}\n\n"
            "انتخاب کن:",
            reply_markup=keyboard
        )
        await callback_query.answer("✅")
        return
    
    if data == "font_activate":
        font_selecting[user.id] = True
        await callback_query.message.reply_text(get_font_list_text())
        await callback_query.answer("✅")
        return
    
    if data == "font_deactivate":
        settings["font_mode"] = False
        save_json(SETTINGS_FILE, settings)
        await callback_query.message.reply_text("❌ **فونت غیرفعال شد!**")
        await callback_query.answer("❌")
        return
    
    if data == "font_list":
        await callback_query.message.reply_text(get_font_list_text())
        await callback_query.answer("✅")
        return
    
    if data == "cmd_backup":
        if not is_owner(user):
            await callback_query.answer("❌ فقط مالک!", show_alert=True)
            return
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 بک‌آپ الآن", callback_data="backup_now")],
            [InlineKeyboardButton("📤 بازیابی", callback_data="restore_now")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ])
        await callback_query.message.reply_text(
            "🛟 **سیستم پشتیبان**\n\n✅ پشتیبان‌گیر خودکار هر ۳۰ دقیقه فعاله!\n\nانتخاب کن:",
            reply_markup=keyboard
        )
        await callback_query.answer("✅")
        return
    
    if data == "backup_now":
        if backup_data():
            await callback_query.message.reply_text("✅ **پشتیبان با موفقیت ذخیره شد!** 🛟")
        else:
            await callback_query.message.reply_text("❌ خطا در پشتیبان‌گیری!")
        await callback_query.answer("✅")
        return
    
    if data == "restore_now":
        if restore_backup():
            await callback_query.message.reply_text("✅ **بازیابی با موفقیت انجام شد!** 📤")
        else:
            await callback_query.message.reply_text("❌ فایل پشتیبان پیدا نشد!")
        await callback_query.answer("✅")
        return
    
    if data == "cmd_kal_info":
        await callback_query.message.reply_text("🕐 **حالت کَل:**\nروی پیام دشمن ریپلای بزن و بنویس: `کل`\n🛑 توقف: `نکل`")
        await callback_query.answer("✅")
        return
    
    if data == "cmd_tiz_info":
        await callback_query.message.reply_text("✈️ **حالت تیز:**\n`تیز متن`\n🛑 توقف: `نفرسس`")
        await callback_query.answer("✅")
        return
    
    if data == "cmd_active":
        settings["self_active"] = True
        save_json(SETTINGS_FILE, settings)
        await callback_query.message.reply_text("✅ **سلف مصی مگاترون فعال شد!** 🔥")
        await callback_query.answer("✅ فعال شد")
        return
    
    if data == "cmd_deactive":
        settings["self_active"] = False
        save_json(SETTINGS_FILE, settings)
        await callback_query.message.reply_text("😴 **سلف مصی مگاترون خاموش شد!** 💤")
        await callback_query.answer("😴 خاموش شد")
        return
    
    if data == "cmd_logout":
        if user.username and user.username in user_sessions:
            if user.username in user_clients:
                try: await user_clients[user.username].disconnect()
                except: pass
                del user_clients[user.username]
            del user_sessions[user.username]
            save_json(USER_SESSIONS_FILE, user_sessions)
            session_file = f"user_{user.username}.session"
            if os.path.exists(session_file): os.remove(session_file)
            await callback_query.message.reply_text("🚪 **با موفقیت خارج شدید!**")
        else:
            await callback_query.message.reply_text("ℹ️ شما وارد اکانت نشدید!")
        await callback_query.answer("🚪")
        return

# ═══════════════════════════════════════
# 📱 سیستم لاگین
# ═══════════════════════════════════════

@bot_client.on_message(filters.text)
async def handle_text_messages(client, message: Message):
    # رد کردن پیام‌هایی که با / شروع می‌شوند (دستورات)
    if message.text and message.text.startswith('/'):
        return
    
    user = message.from_user
    text = message.text.strip()
    
    # انتخاب فونت
    if user.id in font_selecting and font_selecting[user.id]:
        if text.isdigit() and int(text) in FONTS:
            font_id = int(text)
            settings["font_mode"] = True
            settings["active_font"] = font_id
            save_json(SETTINGS_FILE, settings)
            font_selecting[user.id] = False
            await message.reply_text(f"✅ **فونت {FONTS[font_id]['name']} فعال شد!** 🎨")
        else:
            await message.reply_text("❌ شماره نامعتبر! یه عدد بین ۱ تا ۲۰ بفرست.")
        return
    
    # سیستم لاگین
    if user.id not in temp_login_data:
        return
    
    action_data = temp_login_data[user.id]
    
    if action_data.get("action") == "add_sub":
        new_sub = text.replace("@", "")
        if new_sub.lower() == OWNER_USERNAME.lower():
            await message.reply_text("❌ مالک که خودتی! 😅")
            del temp_login_data[user.id]
            return
        
        if new_sub in subscribers:
            await message.reply_text(f"ℹ️ @{new_sub} قبلاً مشترک بوده!")
        else:
            subscribers.append(new_sub)
            save_list(SUBSCRIBERS_FILE, subscribers)
            await message.reply_text(f"✅ @{new_sub} به مشترک‌ها اضافه شد! 🎉")
        
        del temp_login_data[user.id]
        return
    
    if action_data.get("action") == "login":
        step = action_data.get("step")
        
        if step == "phone":
            phone = text.replace("+", "").replace(" ", "")
            
            if not phone.isdigit() or len(phone) < 10:
                await message.reply_text("❌ شماره نامعتبر! دوباره بفرست:\nمثال: `989124416473`")
                return
            
            action_data["phone"] = phone
            action_data["step"] = "code"
            
            session_name = f"user_{user.username or user.id}"
            temp_client = Client(
                session_name,
                api_id=API_ID,
                api_hash=API_HASH,
                phone_number=phone
            )
            
            try:
                await temp_client.connect()
                sent_code = await temp_client.send_code(phone)
                action_data["temp_client"] = temp_client
                action_data["phone_code_hash"] = sent_code.phone_code_hash
                
                await message.reply_text(
                    "📱 **کد تأیید ارسال شد!**\n\n"
                    "🔢 لطفاً کد ۵ رقمی دریافت شده را وارد کنید:\n"
                    "مثال: `12345`\n\n"
                    "🚫 لغو: `/cancel`"
                )
            except Exception as e:
                await message.reply_text(f"❌ خطا در ارسال کد: {e}")
                del temp_login_data[user.id]
            return
        
        if step == "code":
            code = text.replace(" ", "")
            
            if not code.isdigit() or len(code) < 5:
                await message.reply_text("❌ کد نامعتبر! باید ۵ رقم باشه. دوباره بفرست:")
                return
            
            temp_client = action_data.get("temp_client")
            phone = action_data.get("phone")
            phone_code_hash = action_data.get("phone_code_hash")
            
            try:
                await temp_client.sign_in(phone, phone_code_hash, code)
                
                session_name = f"user_{user.username or user.id}"
                user_sessions[user.username] = session_name
                save_json(USER_SESSIONS_FILE, user_sessions)
                user_clients[user.username] = temp_client
                
                await send_command_menu(client, message)
                del temp_login_data[user.id]
                
            except SessionPasswordNeeded:
                action_data["step"] = "password"
                await message.reply_text(
                    "🔐 **احراز هویت دو مرحله‌ای فعال است!**\n\n"
                    "🔑 لطفاً رمز عبور خود را وارد کنید:"
                )
                
            except PhoneCodeInvalid:
                await message.reply_text("❌ کد اشتباهه! دوباره تلاش کن:")
                
            except PhoneCodeExpired:
                await message.reply_text("❌ کد منقضی شده! دوباره با `/start` شروع کن.")
                del temp_login_data[user.id]
                
            except Exception as e:
                await message.reply_text(f"❌ خطا: {e}")
                del temp_login_data[user.id]
            return
        
        if step == "password":
            password = text
            temp_client = action_data.get("temp_client")
            
            try:
                await temp_client.check_password(password)
                
                session_name = f"user_{user.username or user.id}"
                user_sessions[user.username] = session_name
                save_json(USER_SESSIONS_FILE, user_sessions)
                user_clients[user.username] = temp_client
                
                await send_command_menu(client, message)
                del temp_login_data[user.id]
                
            except Exception as e:
                await message.reply_text(f"❌ رمز اشتباه! دوباره تلاش کن:\n{e}")
            return

# ═══════════════════════════════════════
# 🚪 خروج - لغو
# ═══════════════════════════════════════

@bot_client.on_message(filters.command("logout"))
async def logout_command(client, message: Message):
    user = message.from_user
    
    if user.username and user.username in user_sessions:
        if user.username in user_clients:
            try: await user_clients[user.username].disconnect()
            except: pass
            del user_clients[user.username]
        
        del user_sessions[user.username]
        save_json(USER_SESSIONS_FILE, user_sessions)
        
        session_file = f"user_{user.username}.session"
        if os.path.exists(session_file):
            os.remove(session_file)
        
        await message.reply_text("🚪 **با موفقیت خارج شدید!**")
    else:
        await message.reply_text("ℹ️ شما وارد اکانت نشدید!")

@bot_client.on_message(filters.command("cancel"))
async def cancel_action(client, message: Message):
    uid = message.from_user.id
    if uid in temp_login_data:
        del temp_login_data[uid]
    if uid in font_selecting:
        font_selecting[uid] = False
    await message.reply_text("🚫 عملیات لغو شد.")

# ═══════════════════════════════════════
# 📊 وضعیت
# ═══════════════════════════════════════

@bot_client.on_message(filters.regex(r"^وضعیت$"))
async def status_command(client, message: Message):
    if not has_access(message.from_user): return
    start_time = time.time()
    msg = await message.reply_text("📡 ...")
    ping = round((time.time() - start_time) * 1000)
    me = await main_self.get_me()
    
    s = settings
    current_font = FONTS.get(s.get("active_font", 1), {}).get("name", "Bold")
    text = f"""
**⚡ وضعیت سلف مصی مگاترون ⚡**

👑 مالک: @{OWNER_USERNAME}
👤 اکانت: {me.first_name}
📊 پینگ: {ping}ms

👥 دوستان: {len(friends)} | 💀 دشمنان: {len(enemies)}
👤 مشترک‌ها: {len(subscribers)} | 🔐 آنلاین: {len(user_clients)}
💬 جواب‌ها: {len(replies)} | 🌫️ محوی: {len(mahvi_replies)}

🟢 سلف: {'✅' if s.get('self_active') else '😴'}
🔥 تهاجمی: {'✅' if s.get('aggressive_mode') else '❌'}
💥 نابودگر: {'✅' if s.get('destroyer_mode') else '❌'}
🔄 فشاری: {'✅' if s.get('press_mode') else '❌'}
🐉 اژدها: {'✅' if s.get('dragon_mode') else '❌'}
🌫️ محوی: {'✅' if s.get('mahvi_mode') else '❌'}
🔗 ضدلینک: {'✅' if s.get('anti_link') else '❌'}
⚡ فایر: {'✅' if s.get('fire_mode') else '❌'}
🎨 فونت: {'✅ ' + current_font if s.get('font_mode') else '❌'}
"""
    await msg.edit_text(text)

# ═══════════════════════════════════════
# 👤 مشخصات
# ═══════════════════════════════════════

@bot_client.on_message(filters.regex(r"^مشخصات$"))
async def profile_command(client, message: Message):
    if not has_access(message.from_user): return
    me = await main_self.get_me()
    photos = await main_self.get_profile_photos("me", limit=1)
    text = f"👤 **{me.first_name}**\n🆔 `{me.id}`\n🏷️ @{me.username or 'ندارد'}\n📝 {me.bio or 'ندارد'}"
    if photos:
        await message.reply_photo(photos[0].file_id, caption=text)
    else:
        await message.reply_text(text)

# ═══════════════════════════════════════
# 📅 تاریخ
# ═══════════════════════════════════════

@bot_client.on_message(filters.regex(r"^تاریخ$"))
async def date_command(client, message: Message):
    if not has_access(message.from_user): return
    now = jdatetime.datetime.now()
    await message.reply_text(f"☀️ {now.strftime('%Y/%m/%d')}\n📆 {now.strftime('%A')}\n🕐 {now.strftime('%H:%M:%S')}")

# ═══════════════════════════════════════
# 🔍 جستجو
# ═══════════════════════════════════════

@bot_client.on_message(filters.regex(r"^جستجوی آهنگ (.+)"))
async def search_music(client, message: Message):
    if not has_access(message.from_user): return
    query = message.matches[0].group(1)
    await message.reply_text(f"🔍 {query}...")
    results = []
    async for dialog in main_self.get_dialogs(limit=50):
        if dialog.chat.type in ["channel", "supergroup"]:
            try:
                async for msg in main_self.search_messages(dialog.chat.id, query=query, limit=2):
                    if msg.audio or msg.voice:
                        link = f"https://t.me/{dialog.chat.username}/{msg.id}" if dialog.chat.username else "لینک خصوصی"
                        results.append(f"🎵 {dialog.chat.title}\n{link}")
                        break
            except: continue
    await message.reply_text("\n\n".join(results[:5]) if results else "❌ پیدا نشد!")

# ═══════════════════════════════════════
# 🤝💀 دوستان و دشمنان
# ═══════════════════════════════════════

@bot_client.on_message(filters.reply & filters.regex(r"^تنظیم دوست$"))
async def set_friend(client, message: Message):
    if not has_access(message.from_user): return
    target = message.reply_to_message.from_user
    if target.id not in friends:
        friends.append(target.id); save_list(FRIENDS_FILE, friends)
        await message.reply_text(f"🤝 {target.first_name} → دوست! 🛡️")
    else: await message.reply_text("ℹ️ قبلاً دوست.")

@bot_client.on_message(filters.reply & filters.regex(r"^حذف دوست$"))
async def remove_friend(client, message: Message):
    if not has_access(message.from_user): return
    target = message.reply_to_message.from_user
    if target.id in friends:
        friends.remove(target.id); save_list(FRIENDS_FILE, friends)
        await message.reply_text(f"🗑️ {target.first_name} حذف شد!")
    else: await message.reply_text("ℹ️ نبود.")

@bot_client.on_message(filters.reply & filters.regex(r"^تنظیم دشمن$"))
async def set_enemy(client, message: Message):
    if not has_access(message.from_user): return
    target = message.reply_to_message.from_user
    if target.id not in enemies:
        enemies.append(target.id); save_list(ENEMIES_FILE, enemies)
        await message.reply_text(f"💀 {target.first_name} → دشمن! 🔫")
    else: await message.reply_text("ℹ️ قبلاً دشمن.")

@bot_client.on_message(filters.reply & filters.regex(r"^حذف دشمن$"))
async def remove_enemy(client, message: Message):
    if not has_access(message.from_user): return
    target = message.reply_to_message.from_user
    if target.id in enemies:
        enemies.remove(target.id); save_list(ENEMIES_FILE, enemies)
        await message.reply_text(f"🗑️ {target.first_name} حذف شد!")
    else: await message.reply_text("ℹ️ نبود.")

# ═══════════════════════════════════════
# 🔥 تهاجمی - 💥 نابودگر - 🔄 فشاری
# ═══════════════════════════════════════

@bot_client.on_message(filters.regex(r"^حالت تهاجمی خاموش$"))
async def aggressive_off(client, message: Message):
    settings["aggressive_mode"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🔥 **تهاجمی خاموش شد!**")

@bot_client.on_message(filters.regex(r"^حالت تهاجمی$"))
async def aggressive_on(client, message: Message):
    settings["aggressive_mode"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🔥 **تهاجمی روشن!** (۲۰ بار)")

@bot_client.on_message(filters.regex(r"^نابودگر روشن$"))
async def destroyer_on_cmd(client, message: Message):
    settings["destroyer_mode"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("💥 **نابودگر روشن!** (۵۰ بار)")

@bot_client.on_message(filters.regex(r"^نابودگر خاموش$"))
async def destroyer_off_cmd(client, message: Message):
    settings["destroyer_mode"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("💥 **نابودگر خاموش شد!**")

@bot_client.on_message(filters.regex(r"^حالت فشاری$"))
async def press_on_cmd(client, message: Message):
    settings["press_mode"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🔄 **فشاری روشن!**")

@bot_client.on_message(filters.regex(r"^فشاری خاموش$"))
async def press_off_cmd(client, message: Message):
    settings["press_mode"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🛑 **فشاری خاموش!**")

# ═══════════════════════════════════════
# 🐉 اژدها - 🌫️ محوی - 🔗 ضد لینک - 🎨 فونت
# ═══════════════════════════════════════

@bot_client.on_message(filters.regex(r"^اژدهای مصی روشن$"))
async def dragon_on_cmd(client, message: Message):
    settings["dragon_mode"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🐉 **اژدهای مصی بیدار شد!** 🔥")

@bot_client.on_message(filters.regex(r"^اژدها بخواب$"))
async def dragon_off_cmd(client, message: Message):
    settings["dragon_mode"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("😴 **اژدها به خواب رفت...** 💤")

@bot_client.on_message(filters.regex(r"^محوی روشن$"))
async def mahvi_on_cmd(client, message: Message):
    settings["mahvi_mode"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🌫️ **محوی روشن!** (۲ بار - ۱۰۰ جواب)")

@bot_client.on_message(filters.regex(r"^محوی خاموش$"))
async def mahvi_off_cmd(client, message: Message):
    settings["mahvi_mode"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🌫️ **محوی خاموش شد!**")

@bot_client.on_message(filters.regex(r"^ضد لینک روشن$"))
async def anti_link_on_cmd(client, message: Message):
    settings["anti_link"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🔗 **ضد لینک روشن!**")

@bot_client.on_message(filters.regex(r"^ضد لینک خاموش$"))
async def anti_link_off_cmd(client, message: Message):
    settings["anti_link"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🔗 **ضد لینک خاموش!**")

@bot_client.on_message(filters.regex(r"^فونت فعال$"))
async def font_activate_cmd(client, message: Message):
    if not has_access(message.from_user): return
    font_selecting[message.from_user.id] = True
    await message.reply_text(get_font_list_text())

@bot_client.on_message(filters.regex(r"^فونت خاموش$"))
async def font_deactivate_cmd(client, message: Message):
    if not has_access(message.from_user): return
    settings["font_mode"] = False
    save_json(SETTINGS_FILE, settings)
    font_selecting[message.from_user.id] = False
    await message.reply_text("❌ **فونت غیرفعال شد!**")

# ═══════════════════════════════════════
# 🕐 کَل
# ═══════════════════════════════════════

@bot_client.on_message(filters.reply & filters.regex(r"^کل$"))
async def kal_mode_start(client, message: Message):
    if not has_access(message.from_user):
        await message.reply_text("❌ دسترسی نداری!")
        return
    
    target_msg = message.reply_to_message
    chat_id = message.chat.id
    target_user = target_msg.from_user
    
    settings["kal_mode"] = True
    save_json(SETTINGS_FILE, settings)
    await message.reply_text(f"🕐 **کَل علیه {target_user.first_name} شروع شد!**")
    
    for cycle in range(10):
        if not settings.get("kal_mode"):
            await message.reply_text("🛑 متوقف شد!")
            return
        
        last_msg = last_enemy_message.get(target_user.id, target_msg)
        if replies:
            try: await last_msg.reply_text(random.choice(replies))
            except: pass
        await asyncio.sleep(2)
        
        for num in range(1, 10):
            if not settings.get("kal_mode"): return
            try:
                await main_self.send_message(chat_id, str(num))
                await asyncio.sleep(1)
            except FloodWait as e: await asyncio.sleep(e.x)
        
        try:
            await main_self.send_message(chat_id, "0")
            await asyncio.sleep(1)
        except FloodWait as e: await asyncio.sleep(e.x)
        
        try:
            madrak = await main_self.send_message(chat_id, "📎 **مدرک**")
            await madrak.pin()
            await asyncio.sleep(1)
        except FloodWait as e: await asyncio.sleep(e.x)
        
        for r in random.sample(replies, min(3, len(replies))):
            if not settings.get("kal_mode"): return
            try:
                await last_msg.reply_text(r)
                await asyncio.sleep(1.5)
            except FloodWait as e: await asyncio.sleep(e.x)
    
    if settings.get("kal_mode"):
        try: await main_self.send_message(chat_id, "🟥🟥NO OFF PLEASE🟥🟥")
        except: pass
        settings["kal_mode"] = False
        save_json(SETTINGS_FILE, settings)

@bot_client.on_message(filters.regex(r"^نکل$"))
async def kal_off_cmd(client, message: Message):
    if not has_access(message.from_user): return
    settings["kal_mode"] = False
    save_json(SETTINGS_FILE, settings)
    await message.reply_text("🛑 **کَل خاموش!**")

# ═══════════════════════════════════════
# ✈️ تیز
# ═══════════════════════════════════════

@bot_client.on_message(filters.regex(r"^تیز (.+)"))
async def tiz_start(client, message: Message):
    if not has_access(message.from_user):
        await message.reply_text("❌ دسترسی نداری!")
        return
    
    text_to_spam = message.matches[0].group(1)
    settings["tiz_mode"] = True
    settings["tiz_text"] = text_to_spam
    save_json(SETTINGS_FILE, settings)
    
    await message.reply_text(f"✈️ **تیز فعال!**\n📝 متن: `{text_to_spam}`\n🛑 توقف: `نفرسس`")
    
    chat_id = message.chat.id
    while settings.get("tiz_mode"):
        try:
            await main_self.send_message(chat_id, text_to_spam)
            await asyncio.sleep(0.3)
        except FloodWait as e: await asyncio.sleep(e.x)
        except: break

@bot_client.on_message(filters.regex(r"^نفرسس$"))
async def tiz_stop_cmd(client, message: Message):
    if not has_access(message.from_user): return
    settings["tiz_mode"] = False
    settings["tiz_text"] = ""
    save_json(SETTINGS_FILE, settings)
    await message.reply_text("🛑 **تیز خاموش!**")

# ═══════════════════════════════════════
# 🟢 فعال/خاموش سلف - 🛟 پشتیبان
# ═══════════════════════════════════════

@bot_client.on_message(filters.regex(r"^فعال سلف$"))
async def activate_self_cmd(client, message: Message):
    if not has_access(message.from_user): return
    settings["self_active"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("✅ **سلف مصی مگاترون فعال شد!** 🔥")

@bot_client.on_message(filters.regex(r"^خاموش سلف$"))
async def deactivate_self_cmd(client, message: Message):
    if not has_access(message.from_user): return
    settings["self_active"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("😴 **سلف مصی مگاترون خاموش شد!** 💤")

@bot_client.on_message(filters.regex(r"^پشتیبان$"))
async def backup_now_cmd(client, message: Message):
    if not is_owner(message.from_user): return
    if backup_data():
        await message.reply_text("✅ **پشتیبان ذخیره شد!** 🛟")
    else:
        await message.reply_text("❌ خطا!")

# ═══════════════════════════════════════
# 🚀 اجرا
# ═══════════════════════════════════════

async def main():
    print("🔥 سلف مصی مگاترون در حال راه‌اندازی...")
    print(f"👑 مالک: @{OWNER_USERNAME}")
    
    await main_self.start()
    await bot_client.start()
    
    for username, session_name in user_sessions.items():
        if os.path.exists(f"{session_name}.session"):
            try:
                client = Client(session_name, api_id=API_ID, api_hash=API_HASH)
                await client.start()
                user_clients[username] = client
                print(f"✅ کاربر @{username} وصل شد!")
            except Exception as e:
                print(f"❌ خطا برای @{username}: {e}")
    
    print("✅ همه کلاینت‌ها آماده‌ان!")
    print(f"👥 مشترک‌ها: {len(subscribers)} | 🔐 آنلاین: {len(user_clients)}")
    
    # نگه داشتن برنامه تا زمانی که دستی متوقف شود (Ctrl+C)
    try:
        await asyncio.Future()  # منتظر می‌ماند تا ابد
    except KeyboardInterrupt:
        print("\n🛑 ربات با دستور شما متوقف شد")

if __name__ == "__main__":
    asyncio.run(main())