from flask import Flask, request, abort
import yaml
import requests
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

NGROK_URL = ""

def get_ngrok_url():
    response = requests.get("http://localhost:4040/api/tunnels")
    global NGROK_URL
    NGROK_URL = json.loads(response.text)["tunnels"][0]["public_url"]


app = Flask(__name__)

with open("MySecretConfig.yaml") as f:
    secret_config = yaml.safe_load(f)

line_bot_api = LineBotApi(secret_config['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(secret_config['CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text + "やで"))
    image_message = ImageSendMessage(
        original_content_url=f"{NGROK_URL}/static/images/sample.jpg",
        preview_image_url=f"{NGROK_URL}/static/images/sample.jpg",
    )
    line_bot_api.reply_message(event.reply_token, image_message)



if __name__ == "__main__":
    get_ngrok_url()
    app.run()