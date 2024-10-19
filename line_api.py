from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, 
                            TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, 
                            QuickReply, QuickReplyButton, CarouselTemplate, CarouselColumn)

app = Flask(__name__)


# ในการเทสบอท สามารถ add line id: @340kolkz

line_bot_api = LineBotApi('yj1VnWRAPbabFRDU05A4lBhfMWhQWZteMRz+OZyvk+C1V1dwj3RX+699IyizAIbx9CHckWgEjUl5tLWSvf4tUeld4JgpJgVN69PC26HjX8e3sd6CwDeQwyYewQU3RueV1pHy4Zh/rwl791814STEeAdB04t89/1O/w1cDnyilFU=') 
handler = WebhookHandler('fda46a82a408ce3ffdf8c411f1b4e6a0')  

@app.route("/callback", methods=['POST'])
def callback():
    # รับ Signature จาก Header เพื่อตรวจสอบความปลอดภัย
    signature = request.headers['X-Line-Signature']

    # รับ request body
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# ฟังก์ชันตอบกลับเมื่อผู้ใช้ส่งข้อความ
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.lower()  # ข้อความที่ผู้ใช้ส่งมา (แปลงเป็นตัวพิมพ์เล็ก)
    
    if user_text == "button":
        # ตอบกลับด้วย Button Template
        buttons_template = ButtonsTemplate(
            title='Menu', text='Please select an option:', actions=[
                MessageTemplateAction(label='Say Hello', text='Hello!'),
                MessageTemplateAction(label='Say Goodbye', text='Goodbye!')
            ]
        )
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='Buttons template', template=buttons_template)
        )

    elif user_text == "quickreply":
        # ตอบกลับด้วย Quick Reply
        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageTemplateAction(label="Option 1", text="Option 1")),
            QuickReplyButton(action=MessageTemplateAction(label="Option 2", text="Option 2")),
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Choose an option:", quick_reply=quick_reply)
        )

    elif user_text == "carousel":
        # ตอบกลับด้วย Carousel Template
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(title="Option 1", text="Description 1", actions=[
                MessageTemplateAction(label='Select 1', text='You selected option 1')
            ]),
            CarouselColumn(title="Option 2", text="Description 2", actions=[
                MessageTemplateAction(label='Select 2', text='You selected option 2')
            ])
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='Carousel template', template=carousel_template)
        )

    else:
        # ตอบกลับข้อความธรรมดาในกรณีที่ไม่ได้ส่งข้อความที่กำหนดไว้
        reply_chat = f"You said {user_text}"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"{reply_chat} (Please send 'button', 'quickreply' or 'carousel')")
        )

if __name__ == "__main__":
    app.run(debug=True)
