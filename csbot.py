# import telebot
# import requests
# import certifi
#
# # -------------------------------
# # 1️⃣ 固定配置
# # -------------------------------
# TOKEN = "7918333419:AAHe0gfhur6I-C8AuvI-9S6veJzLRqw80n4"
# SERVERCHAN_SENDKEY = "sctp13530t92aiwxtuadhanhsn26hw5z"
# TARGET_USERNAMES = ["AndreaDepierre2020","KB_Kyle","KB-TOM","JIETION"]

import os
import telebot
import requests
import certifi

TOKEN = os.getenv("TOKEN")  # Telegram Bot Token
SERVERCHAN_SENDKEY = os.getenv("SERVERCHAN_SENDKEY")  # Server酱 key
TARGET_USERNAMES = ["AndreaDepierre2020","KB_Kyle","KB-TOM","JIETION"]


bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# -------------------------------
# 2️⃣ Server酱推送函数
# -------------------------------
def send_serverchan(msg: str):
    print(f"str:"+msg)
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    data = {
        "title": "Telegram提醒",
        "desp": msg
    }
    try:
        res = requests.post(url, data=data, verify=certifi.where())
        print(res.status_code, res.text)
        if res.status_code == 200:
            print("Server酱推送成功")
        else:
            print("Server酱推送失败")
    except Exception as e:
        print("Server酱推送异常:", e)

# -------------------------------
# 3️⃣ 监听 @ 的 Telegram 消息
# -------------------------------
@bot.message_handler(content_types=['text'])
def detect_mention_and_notify(message):
    print(f"收到消息: {message.text}")
    if not message.entities:
        print("消息没有 entities")
        return

    for entity in message.entities:
        # 点击 @ 的真实用户
        if entity.type == "text_mention":
            uid = entity.user.id
            print(f"检测到 text_mention: user_id={uid}")
            # 这里只根据 username 列表固定回复，不用 ID
            if entity.user.username in TARGET_USERNAMES:
                reply_text = "您好，劳请贵司稍等，我方立即确认。"
                bot.reply_to(message, reply_text)
                send_serverchan(f"{message.from_user.first_name} 在群里 @ 了 {entity.user.first_name}:\n{message.text}")
                return

        # 纯文本 @username
        elif entity.type == "mention":
            mention_text = message.text[entity.offset: entity.offset + entity.length]  # "@username"
            username = mention_text.lstrip("@")
            print(f"检测到 mention: username={username}")

            if username in TARGET_USERNAMES:
                reply_text = "您好，劳请贵司稍等，我方立即确认。"
                bot.reply_to(message, reply_text)
                send_serverchan(f"{message.from_user.first_name} 在群里 @ 了 @{username}:\n{message.text}")
                return

# -------------------------------
# 4️⃣ 启动长轮询
# -------------------------------
bot.infinity_polling(timeout=10, long_polling_timeout=5)

