import asyncio
import datetime
import time
import jdatetime
import os
import json
import random
import re
import threading
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired

# ═══════════════════════════════════════
# ⚙️ تنظیمات اصلی
# ═══════════════════════════════════════
API_ID = 30479174
API_HASH = "f7116f16ed02b404785a4cfe8d2468d3"
BOT_TOKEN = "8894461474:AAH0fHxD_Twa836qt78T4KUL0wq82F5Cpt4"
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
WOLF_TARGET_FILE = "wolf_target.json"

# ═══════════════════════════════════════
# 🔧 توابع فایل
# ═══════════════════════════════════════

def load_list(filename):
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
    except: pass
    return []

def save_list(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except: pass

def load_json(filename, default=None):
    if default is None: default = {}
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
    except: pass
    return default

def save_json(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except: pass

def load_replies():
    try:
        if os.path.exists(REPLIES_FILE):
            with open(REPLIES_FILE, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
    except: pass
    return [f"جواب {i}" for i in range(1, 301)]

def save_replies(reply_list):
    try:
        with open(REPLIES_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(reply_list))
    except: pass

def load_mahvi():
    try:
        if os.path.exists(MAHVI_FILE):
            with open(MAHVI_FILE, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
    except: pass
    return [f"محوی {i}" for i in range(1, 101)]

def save_mahvi(mahvi_list):
    try:
        with open(MAHVI_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(mahvi_list))
    except: pass

# ═══════════════════════════════════════
# 🛟 پشتیبان‌گیر
# ═══════════════════════════════════════

def backup_data():
    try:
        data = {"friends": friends, "enemies": enemies, "settings": settings,
                "subscribers": subscribers, "chatted_users": chatted_users,
                "timestamp": str(datetime.datetime.now())}
        save_json(BACKUP_FILE, data)
        print("🛟 پشتیبان خودکار انجام شد!")
        return True
    except: return False

def restore_backup():
    global friends, enemies, settings, subscribers, chatted_users
    try:
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
    except: pass
    return False

def auto_backup_loop():
    while True:
        time.sleep(1800)
        try: backup_data()
        except: pass

def log_report(reporter_id, target_id, chat_id):
    try:
        reports = load_json(REPORT_LOG_FILE, [])
        reports.append({"reporter": reporter_id, "target": target_id, "chat": chat_id,
                        "time": str(datetime.datetime.now())})
        save_json(REPORT_LOG_FILE, reports)
    except: pass

# ═══════════════════════════════════════
# 💰 اقتصادی
# ═══════════════════════════════════════

def get_economy():
    try:
        r = requests.get("https://api.bitpin.ir/v1/market/price?pair=usdt_irr", timeout=5)
        usdt = int(r.json()["price"])
        gold = int(usdt * 0.003)
        return f"💵 دلار: {usdt:,} تومان\n🏆 طلا: {gold:,} تومان"
    except: return "❌ در دسترس نیست"

# ═══════════════════════════════════════
# 🎨 ۲۰ فونت
# ═══════════════════════════════════════

FONTS = {
    1: {"name": "𝗕𝗼𝗹𝗱", "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"},
    2: {"name": "𝐼𝑡𝑎𝑙𝑖𝑐", "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧0123456789"},
    3: {"name": "𝑩𝒐𝒍𝒅 𝑰𝒕𝒂𝒍𝒊𝒄", "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛0123456789"},
    4: {"name": "𝙼𝚘𝚗𝚘𝚜𝚙𝚊𝚌𝚎", "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"},
    5: {"name": "𝒞𝓊𝓇𝓈𝒾𝓋𝑒", "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "fancy": "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏0123456789"},
    10: {"name": "𝕯𝖔𝖚𝖇𝖑𝖊", "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
         "fancy": "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟0123456789"},
    20: {"name": "M҉a҉g҉i҉c҉", "normal": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
         "fancy": "A҉B҉C҉D҉E҉F҉G҉H҉I҉J҉K҉L҉M҉N҉O҉P҉Q҉R҉S҉T҉U҉V҉W҉X҉Y҉Z҉a҉b҉c҉d҉e҉f҉g҉h҉i҉j҉k҉l҉m҉n҉o҉p҉q҉r҉s҉t҉u҉v҉w҉x҉y҉z҉0҉1҉2҉3҉4҉5҉6҉7҉8҉9҉"}
}

def apply_font(text, font_id):
    if font_id not in FONTS: return text
    font = FONTS[font_id]
    result = ""
    for char in text:
        result += font["fancy"][font["normal"].index(char)] if char in font["normal"] else char
    return result

def get_font_list_text():
    text = "🎨 **لیست فونت‌ها:**\n\n"
    for num, font in FONTS.items():
        text += f"{num}. {font['name']}\n"
    return text + "\n📝 شماره فونت رو بفرست:"

# ═══════════════════════════════════════
# 📊 بارگذاری داده‌ها
# ═══════════════════════════════════════

friends = load_list(FRIENDS_FILE)
enemies = load_list(ENEMIES_FILE)
replies = load_replies()
mahvi_replies = load_mahvi()
settings = load_json(SETTINGS_FILE, {
    "press_mode": False, "dragon_mode": False, "aggressive_mode": False,
    "anti_link": False, "kal_mode": False, "tiz_mode": False, "tiz_text": "",
    "self_active": True, "destroyer_mode": False, "mahvi_mode": False,
    "fire_mode": False, "font_mode": False, "active_font": 1,
    "tornado_mode": False, "shark_mode": False, "berserk_mode": False,
    "tsunami_mode": False, "wolf_mode": False, "hell_mode": False
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
link_counter = {}

# پشتیبان‌گیر
backup_thread = threading.Thread(target=auto_backup_loop, daemon=True)
backup_thread.start()
print("🛟 پشتیبان‌گیر فعال شد")

# ═══════════════════════════════════════
# 🛠️ توابع کمکی
# ═══════════════════════════════════════

def is_owner(user):
    return user and user.username and user.username.lower() == OWNER_USERNAME.lower()

def has_access(user):
    if not user: return False
    if is_owner(user): return True
    return user.username and user.username.lower() in [s.lower() for s in subscribers]

async def mega_reply(message, text, count=8, delay=0.05):
    if settings.get("font_mode") and settings.get("active_font"):
        text = apply_font(text, settings["active_font"])
    for i in range(count):
        try:
            await message.reply_text(text)
            await asyncio.sleep(delay)
        except FloodWait as e: await asyncio.sleep(e.x)
        except: break

async def fire_reply(message, text, count=8):
    if settings.get("font_mode"): text = apply_font(text, settings["active_font"])
    await asyncio.gather(*[message.reply_text(text) for _ in range(count)], return_exceptions=True)

async def destroyer_reply(message, text):
    await mega_reply(message, f"💥 {text}", count=50, delay=0.03)

async def berserk_reply(message, text):
    await mega_reply(message, f"😡 {text}", count=100, delay=0.02)

async def tornado_attack(message):
    try: await message.delete()
    except: pass
    for _ in range(20):
        try:
            await message.reply_text(f"🌪️ {random.choice(replies)}")
            await asyncio.sleep(0.05)
        except FloodWait as e: await asyncio.sleep(e.x)
        except: break

async def shark_attack(message):
    phrases = ["🦈 کوسه پیدات کرد...", "🦈 بوی خونت رو حس می‌کنم...", "🦈 فرار کن!", "🦈 کوسه نزدیکه..."]
    for i in range(15):
        try:
            await message.reply_text(f"{random.choice(phrases)} ({i+1}/15)")
            await asyncio.sleep(0.05)
        except FloodWait as e: await asyncio.sleep(e.x)
        except: break

async def mahvi_reply(message):
    text = random.choice(mahvi_replies)
    if settings.get("font_mode"): text = apply_font(text, settings["active_font"])
    for _ in range(2):
        try:
            await message.reply_text(f"🌫️ {text}")
            await asyncio.sleep(0.5)
        except FloodWait as e: await asyncio.sleep(e.x)
        except: break

async def anti_link_handler(client, message):
    """ضد لینک پیشرفته - حذف + اخطار + بن خودکار"""
    if not settings.get("anti_link"): return
    sender = message.from_user
    if not sender: return
    chat_id = message.chat.id
    
    try:
        member = await client.get_chat_member(chat_id, sender.id)
        if member.status in ["creator", "administrator"]: return
    except: pass
    
    if not has_link(message.text): return
    
    try: await message.delete()
    except: pass
    
    if sender.id not in link_counter:
        link_counter[sender.id] = {"count": 0, "last_time": time.time()}
    if time.time() - link_counter[sender.id]["last_time"] > 1800:
        link_counter[sender.id] = {"count": 0, "last_time": time.time()}
    
    link_counter[sender.id]["count"] += 1
    link_counter[sender.id]["last_time"] = time.time()
    count = link_counter[sender.id]["count"]
    
    if count == 1:
        try:
            w = await message.reply_text(f"⚠️ **{sender.first_name}** لینک ممنوع!\n🗑️ پاک شد. (۱/۳)")
            await asyncio.sleep(5); await w.delete()
        except: pass
    elif count == 2:
        try:
            w = await message.reply_text(f"⛔ **{sender.first_name}** اخطار دوم! (۲/۳)\n🚫 یه بار دیگه بن میشی!")
            await asyncio.sleep(7); await w.delete()
        except: pass
    elif count >= 3:
        try:
            await client.ban_chat_member(chat_id, sender.id)
            await message.reply_text(f"🔨 **{sender.first_name}** بن شد!\n📋 دلیل: ۳ بار لینک")
            link_counter[sender.id] = {"count": 0, "last_time": time.time()}
        except: pass

async def delete_user_messages(chat_id, user_id, limit=100):
    deleted = 0
    try:
        async for msg in main_self.search_messages(chat_id, from_user=user_id, limit=limit):
            try:
                await msg.delete()
                deleted += 1
                await asyncio.sleep(0.5)
            except: continue
    except: pass
    return deleted

async def is_admin(chat_id, user_id):
    try:
        member = await main_self.get_chat_member(chat_id, user_id)
        return member.status in ["creator", "administrator"]
    except: return False

def has_link(text):
    return bool(re.search(r'https?://\S+|www\.\S+|t\.me/\S+', text or ""))

async def notify_in_group(user_first_name):
    global last_active_group
    if last_active_group:
        try:
            msg = f"📢 {user_first_name} یه پیام تو پیوی داری!"
            if settings.get("font_mode"): msg = apply_font(msg, settings["active_font"])
            await main_self.send_message(last_active_group, msg)
        except: pass

async def send_command_menu(client, message: Message):
    """ارسال منوی زیبا بعد از ورود موفق"""
    user = message.from_user
    first_name = user.first_name if user.first_name else "کاربر"
    
    welcome_text = f"""
╔══════════════════════════════╗
║  🔥  𝐒𝐄𝐋𝐅  𝐌𝐎𝟑𝐘  𝐌𝐄𝐆𝐀𝐓𝐑𝐎𝐍  🔥  ║
╚══════════════════════════════╝

👋 **سلام {first_name} عزیز!**
🎉 به پنل سلف مصی مگاترون خوش اومدی!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 **راهنمای کامل دستورات:**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 **اطلاعات پروفایل:**
▫️ `مشخصات` — نمایش اسم، آیدی، بیو و عکس
▫️ `تاریخ` — تاریخ شمسی و ساعت
▫️ `وضعیت` — وضعیت کامل سلف و پینگ
▫️ `اقتصادی` — قیمت دلار و طلا

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤝💀 **دوستان و دشمنان:**
▫️ `تنظیم دوست` — روی پیام ریپلای کن
▫️ `حذف دوست` — روی پیام ریپلای کن
▫️ `تنظیم دشمن` — روی پیام ریپلای کن
▫️ `حذف دشمن` — روی پیام ریپلای کن

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 **حالت‌های حمله:**
▫️ `حالت تهاجمی` — ۲۰ بار ریپلای
▫️ `نابودگر روشن` — ۵۰ بار ریپلای
▫️ `برزرک روشن` — ۱۰۰ بار ریپلای
▫️ `طوفان روشن` — پاک + ۲۰ ریپلای
▫️ `کوسه روشن` — تعقیب + ۱۵ ریپلای
▫️ `سونامی روشن` — همه جز دوستان
▫️ `دسته گرگ` — حمله گروهی (ریپلای)
▫️ `جهنم روشن` — همه حملات باهم
▫️ `حالت فشاری` — برگشت پیام
▫️ `اژدهای مصی روشن` — ۸ ترکیبی
▫️ `محوی روشن` — ۲ بار جواب محوی

🛑 برای خاموش کردن: اسم + خاموش
مثال: `کوسه خاموش` یا `جهنم خاموش`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛡️ **ابزارهای دفاعی:**
▫️ `ضد لینک روشن` — حذف + اخطار + بن
▫️ `ضد لینک خاموش`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ **ابزارهای ویژه:**
▫️ `کل` — شمارش + مدرک + پین (ریپلای)
▫️ `نکل` — توقف کَل
▫️ `تیز متن` — اسپم بی‌نهایت
▫️ `نفرسس` — توقف اسپم
▫️ `حذف` — پاک کردن پیام (ریپلای)
▫️ `حذف همه` — پاک کردن همه (ریپلای)
▫️ `سیک` — بن کردن (ریپلای)
▫️ `جستجوی آهنگ X` — جستجوی آهنگ

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 **فونت (۲۰ نوع):**
▫️ `فونت فعال` — نمایش لیست
▫️ `فونت خاموش` — غیرفعال

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️ **سیستم:**
▫️ `فعال سلف` / `خاموش سلف`
▫️ `پشتیبان` / `بازیابی`
▫️ `logout` — خروج از اکانت

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✏️ **مدیریت (فقط مالک):**
▫️ `/edit_replies` — مدیریت جواب‌ها
▫️ `/subscribers` — مدیریت مشترک‌ها

🔥 **با سلف مصی مگاترون،**
**هیچ دشمنی در امان نیست!** 💀
"""
    await message.reply_text(welcome_text)

# ==================== حمله گرگ ====================
async def wolf_pack_attack(chat_id, target_msg_id):
    """حمله هماهنگ گروه گرگ"""
    try:
        msg = await main_self.get_messages(chat_id, target_msg_id)
        if not msg: return
        for _ in range(10):
            if not settings.get("wolf_mode"): break
            await msg.reply_text(f"🐺 {random.choice(replies)}")
            await asyncio.sleep(0.5)
    except Exception as e:
        print(f"wolf error: {e}")

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
        "**عمومی:** `مشخصات` `تاریخ` `وضعیت` `اقتصادی` `سیک`\n\n"
        "**دوستان/دشمنان:** `تنظیم دوست` `حذف دوست` `تنظیم دشمن` `حذف دشمن`\n\n"
        "**حملات:** `تهاجمی` `نابودگر روشن` `برزرک روشن` `طوفان روشن`\n"
        "`کوسه روشن` `سونامی روشن` `دسته گرگ` `جهنم روشن`\n"
        "`فشاری` `اژدهای مصی روشن` `محوی روشن`\n\n"
        "**ابزار:** `ضد لینک روشن` `کل` `تیز متن` `نفرسس`\n"
        "`حذف` `حذف همه` `فونت فعال` `فونت خاموش`\n"
        "`فعال سلف` `خاموش سلف` `پشتیبان` `بازیابی`\n\n"
        "**سیستم:** `logout` `/subscribers` `/edit_replies`"
    )

# ═══════════════════════════════════════
# 🎛️ مدیریت دکمه‌ها
# ═══════════════════════════════════════

@bot_client.on_callback_query()
async def handle_all_callbacks(client, callback_query: CallbackQuery):
    user = callback_query.from_user
    data = callback_query.data
    
    if data == "close_menu":
        await callback_query.message.delete()
        await callback_query.answer("✅")
        return
    
    if not has_access(user):
        await callback_query.answer("🚫 حق استفاده نداری!", show_alert=True)
        return
    
    # ════ وضعیت ════
    if data == "show_status":
        me = await main_self.get_me()
        s = settings
        font_name = FONTS.get(s.get("active_font", 1), {}).get("name", "Bold")
        text = f"""
**⚡ وضعیت سلف مصی مگاترون ⚡**

👑 @{OWNER_USERNAME}
👤 {me.first_name} | 🆔 `{me.id}`

👥 دوستان: {len(friends)} | 💀 دشمنان: {len(enemies)}
👤 مشترک‌ها: {len(subscribers)} | 🔐 آنلاین: {len(user_clients)}

🟢 سلف: {'✅' if s.get('self_active') else '😴'}
🔥 جهنم: {'✅' if s.get('hell_mode') else '❌'}
💥 تهاجمی: {'✅' if s.get('aggressive_mode') else '❌'}
😡 برزرک: {'✅' if s.get('berserk_mode') else '❌'}
🌪️ طوفان: {'✅' if s.get('tornado_mode') else '❌'}
🦈 کوسه: {'✅' if s.get('shark_mode') else '❌'}
🌊 سونامی: {'✅' if s.get('tsunami_mode') else '❌'}
🐺 گرگ: {'✅' if s.get('wolf_mode') else '❌'}
🔗 ضدلینک: {'✅' if s.get('anti_link') else '❌'}
🎨 فونت: {'✅ ' + font_name if s.get('font_mode') else '❌'}
"""
        await callback_query.message.reply_text(text)
        await callback_query.answer("✅")
        return
    
    # ════ لاگین ════
    if data == "login_account":
        if user.username and user.username in user_sessions:
            await callback_query.message.reply_text("ℹ️ قبلاً وارد شدید!\nخروج: `logout`")
            await callback_query.answer("ℹ️")
            return
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📱 لاگین با کد", callback_data="login_with_code")],
            [InlineKeyboardButton("📸 لاگین با QR", callback_data="login_with_qr")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ])
        await callback_query.message.reply_text(
            "🔐 **ورود به اکانت تلگرام**\n\nروش لاگین رو انتخاب کن:",
            reply_markup=keyboard
        )
        await callback_query.answer("✅")
        return
    
    if data == "login_with_code":
        temp_login_data[user.id] = {"action": "login", "step": "phone", "username": user.username, "method": "code"}
        await callback_query.message.reply_text("📞 شماره با کد کشور:\nمثال: `989124416473`\n🚫 `/cancel`")
        await callback_query.answer("✅")
        return
    
    if data == "login_with_qr":
        temp_login_data[user.id] = {"action": "login", "step": "phone", "username": user.username, "method": "qr"}
        await callback_query.message.reply_text("📞 شماره رو بفرست تا QR ساخته بشه:\nمثال: `989124416473`\n🚫 `/cancel`")
        await callback_query.answer("✅")
        return
    
    # ════ مشترک‌ها ════
    if data == "subs_menu":
        if not is_owner(user):
            await callback_query.answer("❌ فقط مالک!", show_alert=True)
            return
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ اضافه", callback_data="add_sub"),
             InlineKeyboardButton("➖ حذف", callback_data="del_sub")],
            [InlineKeyboardButton("📋 لیست", callback_data="list_subs"),
             InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ])
        await callback_query.message.reply_text(
            f"👥 **مدیریت مشترک‌ها**\n👑 @{OWNER_USERNAME}\n👥 {len(subscribers)} نفر",
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
        await callback_query.message.reply_text("📝 یوزرنیم مشترک:\nمثال: `@username`\n🚫 `/cancel`")
        await callback_query.answer("✅")
        return
    
    if data == "del_sub":
        if not is_owner(user):
            await callback_query.answer("❌ فقط مالک!", show_alert=True)
            return
        if not subscribers:
            await callback_query.answer("📋 خالیه!", show_alert=True)
            return
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🗑️ @{s}", callback_data=f"delsub_{s}")] for s in subscribers
        ] + [[InlineKeyboardButton("🔙 بازگشت", callback_data="subs_menu")]])
        await callback_query.message.reply_text("🗑️ انتخاب کن:", reply_markup=keyboard)
        await callback_query.answer("✅")
        return
    
    if data == "list_subs":
        if not is_owner(user):
            await callback_query.answer("❌ فقط مالک!", show_alert=True)
            return
        if not subscribers:
            await callback_query.answer("📋 خالیه!", show_alert=True)
        else:
            text = "📋 **لیست مشترک‌ها:**\n\n" + "\n".join([f"{i}. @{s}" for i, s in enumerate(subscribers, 1)])
            await callback_query.message.reply_text(text)
        await callback_query.answer("✅")
        return
    
    if data.startswith("delsub_"):
        username = data.replace("delsub_", "")
        if username in subscribers:
            subscribers.remove(username)
            save_list(SUBSCRIBERS_FILE, subscribers)
            await callback_query.message.reply_text(f"🗑️ @{username} حذف شد!")
        await callback_query.answer("✅")
        return
    
    # ════ اطلاعات ════
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
        text = f"👤 {me.first_name} | 🆔 `{me.id}`\n🔥 جهنم: {'✅' if s.get('hell_mode') else '❌'}"
        await callback_query.message.reply_text(text)
        await callback_query.answer("✅")
        return
    
    if data == "cmd_date":
        now = jdatetime.datetime.now()
        await callback_query.message.reply_text(f"☀️ {now.strftime('%Y/%m/%d')}\n📆 {now.strftime('%A')}\n🕐 {now.strftime('%H:%M:%S')}")
        await callback_query.answer("✅")
        return
    
    if data == "cmd_economy":
        await callback_query.message.reply_text(get_economy())
        await callback_query.answer("✅")
        return
    
    if data == "cmd_search_info":
        await callback_query.message.reply_text("🔍 `جستجوی آهنگ اسم آهنگ`")
        await callback_query.answer("✅")
        return
    
    if data == "cmd_friend_info":
        await callback_query.message.reply_text("🤝 ریپلای: `تنظیم دوست`\n🗑️ ریپلای: `حذف دوست`")
        await callback_query.answer("✅")
        return
    
    if data == "cmd_enemy_info":
        await callback_query.message.reply_text("💀 ریپلای: `تنظیم دشمن`\n🗑️ ریپلای: `حذف دشمن`")
        await callback_query.answer("✅")
        return
    
    if data == "cmd_delete_info":
        await callback_query.message.reply_text("🗑️ `حذف` — یه پیام\n🗑️ `حذف همه` — همه پیام‌ها\n⚠️ فقط ادمین!")
        await callback_query.answer("✅")
        return
    
    # ════ حالت‌های حمله ════
    modes = {
        "cmd_aggressive": ("aggressive_mode", "🔥 تهاجمی", "۲۰ بار"),
        "cmd_destroyer": ("destroyer_mode", "💥 نابودگر", "۵۰ بار"),
        "cmd_berserk": ("berserk_mode", "😡 برزرک", "۱۰۰ بار"),
        "cmd_tornado": ("tornado_mode", "🌪️ طوفان", "پاک + ۲۰"),
        "cmd_shark": ("shark_mode", "🦈 کوسه", "تعقیب + ۱۵"),
        "cmd_tsunami": ("tsunami_mode", "🌊 سونامی", "همه جز دوستان"),
        "cmd_press": ("press_mode", "🔄 فشاری", "برگشت"),
        "cmd_dragon": ("dragon_mode", "🐉 اژدها", "۸ ترکیبی"),
        "cmd_mahvi": ("mahvi_mode", "🌫️ محوی", "۲ بار"),
        "cmd_fire": ("fire_mode", "⚡ فایر", "همزمان"),
    }
    
    if data in modes:
        key, name, desc = modes[data]
        settings[key] = not settings.get(key, False)
        save_json(SETTINGS_FILE, settings)
        state = "✅ روشن" if settings[key] else "❌ خاموش"
        await callback_query.message.reply_text(f"{name}: {state} ({desc})")
        await callback_query.answer(f"{name} {state}")
        return
    
    # ════ جهنم ════
    if data == "cmd_hell":
        settings["hell_mode"] = not settings.get("hell_mode", False)
        all_modes = ["aggressive_mode", "destroyer_mode", "berserk_mode", "tornado_mode",
                    "shark_mode", "tsunami_mode", "press_mode", "dragon_mode",
                    "mahvi_mode", "anti_link", "fire_mode", "wolf_mode"]
        for key in all_modes:
            settings[key] = settings["hell_mode"]
        save_json(SETTINGS_FILE, settings)
        state = "✅ همه روشن" if settings["hell_mode"] else "❌ همه خاموش"
        await callback_query.message.reply_text(f"🔥 **جهنم:** {state}")
        await callback_query.answer(f"🔥 {state}")
        return
    
    # ════ دسته گرگ ════
    if data == "cmd_wolf":
        settings["wolf_mode"] = not settings.get("wolf_mode", False)
        save_json(SETTINGS_FILE, settings)
        state = "✅ روشن" if settings["wolf_mode"] else "❌ خاموش"
        await callback_query.message.reply_text(f"🐺 **دسته گرگ:** {state}")
        await callback_query.answer(f"🐺 {state}")
        return
    
    # ════ ضد لینک ════
    if data == "cmd_antilink":
        settings["anti_link"] = not settings.get("anti_link", False)
        save_json(SETTINGS_FILE, settings)
        state = "✅ روشن" if settings["anti_link"] else "❌ خاموش"
        await callback_query.message.reply_text(f"🔗 **ضد لینک:** {state}\n🗑️ حذف + ⚠️ اخطار + 🔨 بن")
        await callback_query.answer(f"🔗 {state}")
        return
    
    # ════ فونت ════
    if data == "cmd_font_menu":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎨 فعال کردن", callback_data="font_activate"),
             InlineKeyboardButton("❌ خاموش", callback_data="font_deactivate")],
            [InlineKeyboardButton("📋 لیست", callback_data="font_list"),
             InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
        ])
        font_name = FONTS.get(settings.get("active_font", 1), {}).get("name", "Bold")
        await callback_query.message.reply_text(
            f"🎨 **تنظیمات فونت**\n📊 {'✅ فعال' if settings.get('font_mode') else '❌ غیرفعال'}\n🔤 فونت: {font_name}",
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
        await callback_query.message.reply_text("❌ فونت غیرفعال شد!")
        await callback_query.answer("❌")
        return
    
    if data == "font_list":
        await callback_query.message.reply_text(get_font_list_text())
        await callback_query.answer("✅")
        return
    
    # ════ کَل و تیز ════
    if data == "cmd_kal_info":
        await callback_query.message.reply_text("🕐 ریپلای: `کل`\n🛑 توقف: `نکل`")
        await callback_query.answer("✅")
        return
    
    if data == "cmd_tiz_info":
        await callback_query.message.reply_text("✈️ `تیز متن`\n🛑 توقف: `نفرسس`")
        await callback_query.answer("✅")
        return
    
    # ════ فعال/خاموش ════
    if data == "cmd_active":
        settings["self_active"] = True
        save_json(SETTINGS_FILE, settings)
        await callback_query.message.reply_text("✅ **سلف فعال شد!** 🔥")
        await callback_query.answer("✅")
        return
    
    if data == "cmd_deactive":
        settings["self_active"] = False
        save_json(SETTINGS_FILE, settings)
        await callback_query.message.reply_text("😴 **سلف خاموش شد!** 💤")
        await callback_query.answer("😴")
        return
    
    # ════ خروج ════
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
            await callback_query.message.reply_text("🚪 خارج شدید!")
        else:
            await callback_query.message.reply_text("ℹ️ وارد نشدید!")
        await callback_query.answer("🚪")
        return

# ═══════════════════════════════════════
# 📱 سیستم لاگین
# ═══════════════════════════════════════

async def login_with_qr(client, message, phone, action_data):
    """لاگین با QR کد"""
    try:
        temp_client = action_data.get("temp_client")
        if temp_client:
            try: await temp_client.disconnect()
            except: pass
        
        session_name = f"user_{message.from_user.username or message.from_user.id}"
        temp_client = Client(session_name, api_id=API_ID, api_hash=API_HASH, phone_number=phone)
        await temp_client.connect()
        qr_login = await temp_client.send_code(phone)
        
        await message.reply_text(
            "📱 **ورود با QR کد**\n\n"
            f"🔗 لینک ورود:\nhttps://t.me/login/{qr_login.phone_code_hash[:8]}\n\n"
            "📸 یا با دوربین تلگرام QR رو اسکن کن\n\n"
            "⏰ ۲ دقیقه فرصت داری!\n"
            "بعد از ورود، کد رو بفرست."
        )
        
        action_data["temp_client"] = temp_client
        action_data["phone_code_hash"] = qr_login.phone_code_hash
        action_data["step"] = "code"
    except Exception as e:
        await message.reply_text(f"❌ خطا در QR: {e}")

# اصلاح شده: به جای ~filters.command از ~filters.regex(r'^/') استفاده شد
@bot_client.on_message(filters.text & ~filters.regex(r'^/'))
async def handle_text_messages(client, message: Message):
    user = message.from_user
    if not user: return
    
    text = message.text.strip() if message.text else ""
    
    # انتخاب فونت
    if user.id in font_selecting and font_selecting.get(user.id):
        if text.isdigit() and int(text) in FONTS:
            font_id = int(text)
            settings["font_mode"] = True
            settings["active_font"] = font_id
            save_json(SETTINGS_FILE, settings)
            font_selecting[user.id] = False
            await message.reply_text(f"✅ **فونت {FONTS[font_id]['name']} فعال شد!** 🎨")
        else:
            await message.reply_text("❌ شماره نامعتبر! عدد ۱ تا ۲۰ بفرست.")
        return
    
    # لاگین
    if user.id not in temp_login_data: return
    
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
            await message.reply_text(f"✅ @{new_sub} اضافه شد! 🎉")
        del temp_login_data[user.id]
        return
    
    if action_data.get("action") == "login":
        step = action_data.get("step")
        method = action_data.get("method", "code")
        
        if step == "phone":
            phone = text.replace("+", "").replace(" ", "")
            if not phone.isdigit() or len(phone) < 10:
                await message.reply_text("❌ شماره نامعتبر! مثال: `989124416473`")
                return
            
            action_data["phone"] = phone
            
            if method == "qr":
                await login_with_qr(client, message, phone, action_data)
            else:
                action_data["step"] = "code"
                session_name = f"user_{user.username or user.id}"
                temp_client = Client(session_name, api_id=API_ID, api_hash=API_HASH, phone_number=phone)
                try:
                    await temp_client.connect()
                    sent_code = await temp_client.send_code(phone)
                    action_data["temp_client"] = temp_client
                    action_data["phone_code_hash"] = sent_code.phone_code_hash
                    await message.reply_text("📱 **کد تأیید ارسال شد!**\n🔢 کد ۵ رقمی:\n🚫 `/cancel`")
                except Exception as e:
                    await message.reply_text(f"❌ خطا: {e}")
                    del temp_login_data[user.id]

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
    font_name = FONTS.get(s.get("active_font", 1), {}).get("name", "Bold")
    text = f"""
**⚡ وضعیت سلف مصی مگاترون ⚡**

👑 @{OWNER_USERNAME}
👤 {me.first_name} | 📊 پینگ: {ping}ms

👥 دوستان: {len(friends)} | 💀 دشمنان: {len(enemies)}
👤 مشترک‌ها: {len(subscribers)} | 🔐 آنلاین: {len(user_clients)}

🟢 سلف: {'✅' if s.get('self_active') else '😴'}
🔥 جهنم: {'✅' if s.get('hell_mode') else '❌'}
💥 تهاجمی: {'✅' if s.get('aggressive_mode') else '❌'} | نابودگر: {'✅' if s.get('destroyer_mode') else '❌'}
😡 برزرک: {'✅' if s.get('berserk_mode') else '❌'} | 🌪️ طوفان: {'✅' if s.get('tornado_mode') else '❌'}
🦈 کوسه: {'✅' if s.get('shark_mode') else '❌'} | 🌊 سونامی: {'✅' if s.get('tsunami_mode') else '❌'}
🐺 گرگ: {'✅' if s.get('wolf_mode') else '❌'} | 🔄 فشاری: {'✅' if s.get('press_mode') else '❌'}
🐉 اژدها: {'✅' if s.get('dragon_mode') else '❌'} | 🌫️ محوی: {'✅' if s.get('mahvi_mode') else '❌'}
🔗 ضدلینک: {'✅' if s.get('anti_link') else '❌'} | ⚡ فایر: {'✅' if s.get('fire_mode') else '❌'}
🎨 فونت: {'✅ ' + font_name if s.get('font_mode') else '❌'}
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
# 💰 اقتصادی
# ═══════════════════════════════════════

@bot_client.on_message(filters.regex(r"^اقتصادی$"))
async def economy_command(client, message: Message):
    if not has_access(message.from_user): return
    await message.reply_text(get_economy())

# ═══════════════════════════════════════
# 🔍 جستجوی آهنگ
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
# 🔥 تهاجمی - 💥 نابودگر - 😡 برزرک - 🔄 فشاری
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

@bot_client.on_message(filters.regex(r"^برزرک روشن$"))
async def berserk_on_cmd(client, message: Message):
    settings["berserk_mode"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("😡 **برزرک روشن!** (۱۰۰ بار)")

@bot_client.on_message(filters.regex(r"^برزرک خاموش$"))
async def berserk_off_cmd(client, message: Message):
    settings["berserk_mode"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("😡 **برزرک خاموش شد!**")

@bot_client.on_message(filters.regex(r"^حالت فشاری$"))
async def press_on_cmd(client, message: Message):
    settings["press_mode"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🔄 **فشاری روشن!**")

@bot_client.on_message(filters.regex(r"^فشاری خاموش$"))
async def press_off_cmd(client, message: Message):
    settings["press_mode"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🛑 **فشاری خاموش!**")

# ═══════════════════════════════════════
# 🐉 اژدها - 🌫️ محوی - 🌪️ طوفان - 🦈 کوسه - 🌊 سونامی
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

@bot_client.on_message(filters.regex(r"^طوفان روشن$"))
async def tornado_on_cmd(client, message: Message):
    settings["tornado_mode"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🌪️ **طوفان روشن!** (پاک + ۲۰)")

@bot_client.on_message(filters.regex(r"^طوفان خاموش$"))
async def tornado_off_cmd(client, message: Message):
    settings["tornado_mode"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🌪️ **طوفان خاموش شد!**")

@bot_client.on_message(filters.regex(r"^کوسه روشن$"))
async def shark_on_cmd(client, message: Message):
    settings["shark_mode"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🦈 **کوسه روشن!** (تعقیب + ۱۵)")

@bot_client.on_message(filters.regex(r"^کوسه خاموش$"))
async def shark_off_cmd(client, message: Message):
    settings["shark_mode"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🦈 **کوسه خاموش شد!**")

@bot_client.on_message(filters.regex(r"^سونامی روشن$"))
async def tsunami_on_cmd(client, message: Message):
    settings["tsunami_mode"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🌊 **سونامی روشن!** (همه جز دوستان)")

@bot_client.on_message(filters.regex(r"^سونامی خاموش$"))
async def tsunami_off_cmd(client, message: Message):
    settings["tsunami_mode"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🌊 **سونامی خاموش شد!**")

# ═══════════════════════════════════════
# 🔥 جهنم - 🐺 دسته گرگ
# ═══════════════════════════════════════

@bot_client.on_message(filters.regex(r"^جهنم روشن$"))
async def hell_on_cmd(client, message: Message):
    settings["hell_mode"] = True
    all_modes = ["aggressive_mode", "destroyer_mode", "berserk_mode", "tornado_mode",
                "shark_mode", "tsunami_mode", "press_mode", "dragon_mode",
                "mahvi_mode", "anti_link", "fire_mode", "wolf_mode"]
    for key in all_modes:
        settings[key] = True
    save_json(SETTINGS_FILE, settings)
    await message.reply_text("🔥 **جهنم روشن شد!** همه حملات فعال شدن! 💀")

@bot_client.on_message(filters.regex(r"^جهنم خاموش$"))
async def hell_off_cmd(client, message: Message):
    settings["hell_mode"] = False
    all_modes = ["aggressive_mode", "destroyer_mode", "berserk_mode", "tornado_mode",
                "shark_mode", "tsunami_mode", "press_mode", "dragon_mode",
                "mahvi_mode", "anti_link", "fire_mode", "wolf_mode"]
    for key in all_modes:
        settings[key] = False
    save_json(SETTINGS_FILE, settings)
    await message.reply_text("🔥 **جهنم خاموش شد!** همه حملات غیرفعال شدن!")

@bot_client.on_message(filters.reply & filters.regex(r"^دسته گرگ$"))
async def wolf_cmd(client, message: Message):
    if not has_access(message.from_user): return
    settings["wolf_mode"] = True
    save_json(SETTINGS_FILE, settings)
    target = message.reply_to_message
    await message.reply_text(f"🐺 **دسته گرگ فعال شد!** حمله به {target.from_user.first_name}!")
    # ذخیره هدف
    save_json(WOLF_TARGET_FILE, {"chat_id": message.chat.id, "message_id": target.id})
    # حمله همزمان
    await wolf_pack_attack(message.chat.id, target.id)

@bot_client.on_message(filters.regex(r"^دسته گرگ خاموش$"))
async def wolf_off_cmd(client, message: Message):
    settings["wolf_mode"] = False
    save_json(SETTINGS_FILE, settings)
    await message.reply_text("🐺 **دسته گرگ خاموش شد!**")

# ═══════════════════════════════════════
# 🔗 ضد لینک - 🎨 فونت
# ═══════════════════════════════════════

@bot_client.on_message(filters.regex(r"^ضد لینک روشن$"))
async def anti_link_on_cmd(client, message: Message):
    settings["anti_link"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🔗 **ضد لینک روشن!** (حذف + اخطار + بن)")

@bot_client.on_message(filters.regex(r"^ضد لینک خاموش$"))
async def anti_link_off_cmd(client, message: Message):
    settings["anti_link"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("🔗 **ضد لینک خاموش شد!**")

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
# 🗑️ حذف پیام
# ═══════════════════════════════════════

@bot_client.on_message(filters.reply & filters.regex(r"^حذف$"))
async def delete_single_cmd(client, message: Message):
    if not has_access(message.from_user): return
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.reply_text("❌ فقط ادمین!")
        return
    try:
        await message.reply_to_message.delete()
        await message.reply_text("🗑️ **حذف شد!**")
    except:
        await message.reply_text("❌ نتونستم حذف کنم!")

@bot_client.on_message(filters.reply & filters.regex(r"^حذف همه$"))
async def delete_all_cmd(client, message: Message):
    if not has_access(message.from_user): return
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.reply_text("❌ فقط ادمین!")
        return
    target = message.reply_to_message.from_user
    await message.reply_text(f"🗑️ در حال حذف پیام‌های {target.first_name}...")
    deleted = await delete_user_messages(message.chat.id, target.id)
    await message.reply_text(f"✅ {deleted} پیام از {target.first_name} حذف شد!")

# ═══════════════════════════════════════
# 🔨 سیک
# ═══════════════════════════════════════

@bot_client.on_message(filters.reply & filters.regex(r"^سیک$"))
async def sik_ban(client, message: Message):
    if not has_access(message.from_user): return
    if await is_admin(message.chat.id, message.from_user.id):
        target = message.reply_to_message.from_user
        try:
            await main_self.ban_chat_member(message.chat.id, target.id)
            await message.reply_text(f"🔨 {target.first_name} بن شد! 🚫")
        except Exception as e: await message.reply_text(f"❌ {e}")
    else: await message.reply_text("❌ ادمین نیستی!")

# ═══════════════════════════════════════
# 🟢 فعال/خاموش سلف - 🛟 پشتیبان
# ═══════════════════════════════════════

@bot_client.on_message(filters.regex(r"^فعال سلف$"))
async def activate_self_cmd(client, message: Message):
    if not has_access(message.from_user): return
    settings["self_active"] = True; save_json(SETTINGS_FILE, settings)
    await message.reply_text("✅ **سلف فعال شد!** 🔥")

@bot_client.on_message(filters.regex(r"^خاموش سلف$"))
async def deactivate_self_cmd(client, message: Message):
    if not has_access(message.from_user): return
    settings["self_active"] = False; save_json(SETTINGS_FILE, settings)
    await message.reply_text("😴 **سلف خاموش شد!** 💤")

@bot_client.on_message(filters.regex(r"^پشتیبان$"))
async def backup_now_cmd(client, message: Message):
    if not is_owner(message.from_user): return
    if backup_data():
        await message.reply_text("✅ **پشتیبان ذخیره شد!** 🛟")
    else:
        await message.reply_text("❌ خطا!")

@bot_client.on_message(filters.regex(r"^بازیابی$"))
async def restore_now_cmd(client, message: Message):
    if not is_owner(message.from_user): return
    if restore_backup():
        await message.reply_text("✅ **بازیابی انجام شد!** 📤")
    else:
        await message.reply_text("❌ خطا در بازیابی!")

# ═══════════════════════════════════════
# 🧠 اجرای همزمان ربات و سلف
# ═══════════════════════════════════════
async def main():
    # اتصال به هر دو کلاینت
    await main_self.start()
    await bot_client.start()
    print("✅ ربات و سلف با موفقیت اجرا شدند!")
    # نگه داشتن برنامه
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
