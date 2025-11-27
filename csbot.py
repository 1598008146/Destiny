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

# import os
# import telebot
# import requests
# import certifi

# TOKEN = os.getenv("TOKEN")  # Telegram Bot Token
# SERVERCHAN_SENDKEY = os.getenv("SERVERCHAN_SENDKEY")  # Server酱 key
# TARGET_USERNAMES = ["AndreaDepierre2020","KB_Kyle","KB-TOM","JIETION"]


# bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# # -------------------------------
# # 2️⃣ Server酱推送函数
# # -------------------------------
# def send_serverchan(msg: str):
#     print(f"str:"+msg)
#     url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
#     data = {
#         "title": "Telegram提醒",
#         "desp": msg
#     }
#     try:
#         res = requests.post(url, data=data, verify=certifi.where())
#         print(res.status_code, res.text)
#         if res.status_code == 200:
#             print("Server酱推送成功")
#         else:
#             print("Server酱推送失败")
#     except Exception as e:
#         print("Server酱推送异常:", e)

# # -------------------------------
# # 3️⃣ 监听 @ 的 Telegram 消息
# # -------------------------------
# @bot.message_handler(content_types=['text'])
# def detect_mention_and_notify(message):
#     print(f"收到消息: {message.text}")
#     if not message.entities:
#         print("消息没有 entities")
#         return

#     for entity in message.entities:
#         # 点击 @ 的真实用户
#         if entity.type == "text_mention":
#             uid = entity.user.id
#             print(f"检测到 text_mention: user_id={uid}")
#             # 这里只根据 username 列表固定回复，不用 ID
#             if entity.user.username in TARGET_USERNAMES:
#                 reply_text = "您好，劳请贵司稍等，我方立即确认。"
#                 bot.reply_to(message, reply_text)
#                 send_serverchan(f"{message.from_user.first_name} 在群里 @ 了 {entity.user.first_name}:\n{message.text}")
#                 return

#         # 纯文本 @username
#         elif entity.type == "mention":
#             mention_text = message.text[entity.offset: entity.offset + entity.length]  # "@username"
#             username = mention_text.lstrip("@")
#             print(f"检测到 mention: username={username}")

#             if username in TARGET_USERNAMES:
#                 reply_text = "您好，劳请贵司稍等，我方立即确认。"
#                 bot.reply_to(message, reply_text)
#                 send_serverchan(f"{message.from_user.first_name} 在群里 @ 了 @{username}:\n{message.text}")
#                 return

# # -------------------------------
# # 4️⃣ 启动长轮询
# # -------------------------------
# bot.infinity_polling(timeout=10, long_polling_timeout=5)

import os
from flask import Flask, request
import telebot
import requests
import certifi
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# 固定配置
# -------------------------------
TOKEN = os.getenv("TOKEN")  # Telegram Bot Token
SERVERCHAN_SENDKEY = os.getenv("SERVERCHAN_SENDKEY")  # Server酱 key
TARGET_USERNAMES = ["AndreaDepierre2020","KB_Kyle","KB_TOM","JIETION"]

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

@bot.message_handler(content_types=['text'])
def detect_mention_and_notify2(msg):
    if msg.entities:
        for i, entity in enumerate(msg.entities):
            logger.info(f"Entity #{i+1}:")
            # 获取所有属性及值
            for attr, value in vars(entity).items():
               logger.info(f"  {attr}: {value}")
    else:
        logger.info("没有 entities")

# -------------------------------
# Server酱推送函数
# -------------------------------
def send_serverchan(msg: str):
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    data = {"title": "Telegram提醒", "desp": msg}
    try:
        res = requests.post(url, data=data, verify=certifi.where())
        print(res.status_code, res.text)
    except Exception as e:
        print("Server酱推送异常:", e)

# -------------------------------
# 监听 @ 的消息
# -------------------------------
@bot.message_handler(content_types=['text'])
@bot.message_handler(content_types=['text'])
def detect_mention_and_notify(message):
    
    if not message.entities:
        print("没有 @ ，直接忽略")
        return

    for entity in message.entities:
        print("---- entity ----")
        print("类型：", entity.type)
        print("用户：", getattr(entity, 'user', None))

        # @具体用户（text_mention）
        if entity.type == "text_mention":
            username = entity.user.username
            print("检测到 text_mention @：", username)

            if username in TARGET_USERNAMES:
                print("命中目标用户，发送自动回复")
                bot.reply_to(message, "您好，劳请贵司稍等，我方立即确认。")

        # 普通 @ （@username）
        elif entity.type == "mention":
            detect_mention_and_notify2(entity)
            username = message.text[entity.offset: entity.offset + entity.length].lstrip("@")
            print("检测到普通 @：", username)

            if username in TARGET_USERNAMES:
                print("命中目标用户，发送自动回复")
                bot.reply_to(message, "您好，劳请贵司稍等，我方立即确认。")


# -------------------------------
# Flask 接收 Telegram Webhook
# -------------------------------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# -------------------------------
# 启动 Web 服务
# -------------------------------
if __name__ == "__main__":
    # 设置 Webhook
    WEBHOOK_URL = f"https://destiny-jhy5.onrender.com/{TOKEN}"  # 修改成你部署后的 HTTPS URL
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=5000, debug=True)
















