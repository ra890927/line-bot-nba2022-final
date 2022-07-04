import time

from config import *

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import os
from bot import Bot
from userInfo import UserInfo

app = Flask(__name__)

LINE_BOT_URL = 'https://line-bot-nba2022-final.herokuapp.com/'

# Channel Access Token
line_bot_api = LineBotApi(line_channel_access_token)
# Channel Secret
handler = WebhookHandler(line_channel_secret)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # create database table
    UserInfo.createTable()
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=(ImageMessage, TextMessage, StickerMessage))
def handle_message(event):
    if isinstance(event.message, TextMessage):
        msg = event.message.text

        user_info = UserInfo.getInfo(event.source.user_id)
        if user_info:
            lineBot = Bot(user_info)
        else:
            lineBot = Bot(event.source.user_id)

        if msg == 'reset':
            lineBot.reset()
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = lineBot.process()))
        else:
            response = lineBot.process(msg)
            if os.path.isfile('./static/' + response):
                line_bot_api.reply_message(event.reply_token, ImageSendMessage(
                    original_content_url=LINE_BOT_URL + 'static/' + response,
                    preview_image_url=LINE_BOT_URL + 'static/' + response,
                ))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text = response))

        UserInfo.saveInfo(lineBot.info())

@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '這是 NBA 2021-22 Final 資料分析機器人'))

@handler.add(LeaveEvent)
def handle_leave(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text = 'Bye'))
        
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
