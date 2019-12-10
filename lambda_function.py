
import datetime
from datetime import timedelta

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from crawler import get_data, get_web_page, get_data_index
#from user_data import get_user_data, rewrite_user_data

from utils import send_text_message
from aqi import Aqi
from env import YOUR_CHANNEL_ACCESS_TOKEN,YOUR_CHANNEL_SECRET
import json
#=====initialize=====
user_data_filename="user_data.json"
#user_data=get_user_data(user_data_filename)
user_data={}
delta=timedelta(days=0,seconds=0,microseconds=0,milliseconds=0,minutes=0,hours=1,weeks=0)
air_data=get_data()
#air_data is a list with dictionaries
data_index=get_data_index(air_data)
#data_index is to indicade the order of site in air_data
data_time = datetime.datetime.now()
#====================

# Channel Access Token
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


def lambda_handler(event, context):
# 處理訊息
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        global data_time
        global data_index
        global air_data
        global user_data
        
        global user_data_filename

        if not(event.source.user_id in user_data):
            user_data[event.source.user_id]={"subscribe_site":[],"aqi_format":"simple"}
            #rewrite_user_data(user_data_filename,user_data) #write the data in storage

        if datetime.datetime.now()-delta>data_time or data_time.hour!=datetime.datetime.now().hour:
            air_data=get_data()
            data_index=get_data_index(air_data)
            data_time=datetime.datetime.now()
        
        input_text=event.message.text
        input_texts=input_text.split(' ')
        out_text=""
        try:
            if input_texts[0]=="add":
                if input_texts[1] in data_index:
                    if not(input_texts[1] in user_data[event.source.user_id]["subscribe_site"]):
                        user_data[event.source.user_id]["subscribe_site"].append(input_texts[1])
                        #rewrite_user_data(user_data_filename,user_data) #write the data in storage
                        out_text="add success"
                    else:
                        out_text="site already exist"
                else:
                    out_text="add fail, name error"
            elif input_texts[0]=="delete":
                if input_texts[1] in user_data[event.source.user_id]["subscribe_site"]:
                    user_data[event.source.user_id]["subscribe_site"].remove(input_texts[1])
                    #rewrite_user_data(user_data_filename,user_data) #write the data in storage
                    out_text="remove "+input_texts[1]+" from subscribe"
                else:
                    out_text="delete fail, site doesn't exist"
            elif input_texts[0]=="get":
                out_text=""
                if user_data[event.source.user_id]["aqi_format"]=="simple":
                    for i in user_data[event.source.user_id]["subscribe_site"]:
                        #result = json.dumps(air_data[data_index[i]], ensure_ascii=False)
                        out_text=out_text+Aqi.aqi_with_simple_format(air_data[data_index[i]])
                elif user_data[event.source.user_id]["aqi_format"]=="complex":
                    for i in user_data[event.source.user_id]["subscribe_site"]:
                        #result = json.dumps(air_data[data_index[i]], ensure_ascii=False)
                        out_text=out_text+Aqi.aqi_with_complex_format(air_data[data_index[i]])
                else:
                    out_text="format error"
                if out_text=="":
                    out_text="subscribe is empty"
            elif input_texts[0]=="list":
                out_text="aqi format : "+str(user_data[event.source.user_id]["aqi_format"])+"\nsubscribed : "
                for i in user_data[event.source.user_id]["subscribe_site"]:
                    out_text=out_text+str(i)+","
                out_text=out_text+"\nall site:"
                for i in data_index.keys():
                    out_text=out_text+str(i)+","
            elif input_texts[0]=="help":
                out_text="Usage:\n    <command> [options]\nCommands:\n    add \n    delete\n    list\n    get\n    help\n    set format\n"
            elif input_texts[0]=="who":
                out_text=event.source.user_id
            elif input_texts[0]=="alluser":
                
                #u=get_user_data(user_data_filename)
                out_text=json.dumps(user_data,ensure_ascii=False)
            elif input_texts[0]=="set":
                if input_texts[1]=="format":
                    if input_texts[2]=="simple":
                        user_data[event.source.user_id]["aqi_format"]="simple"
                        out_text="set format to simple"
                        #rewrite_user_data(user_data_filename,user_data) #write the data in storage
                    elif input_texts[2]=="complex":
                        user_data[event.source.user_id]["aqi_format"]="complex"
                        out_text="set format to complex"
                        #rewrite_user_data(user_data_filename,user_data) #write the data in storage
                    else:
                        out_text="input error"
                else:
                    out_text="input error"
            elif input_texts[0]=="fsm":
                message = ImageSendMessage("https://i.imgur.com/3YGE57U.png","https://i.imgur.com/08uqJTl.png")
                line_bot_api.reply_message(event.reply_token, message)
                return
            else:
                out_text="command not found"
        except IndexError:
            out_text="input error"


        message = TextSendMessage(out_text)
        line_bot_api.reply_message(event.reply_token, message)

    try:
            # get X-Line-Signature header value
            signature = event['headers']['X-Line-Signature']
            # get event body
            body = event['body']
            # handle webhook body
            handler.handle(body, signature)
    except InvalidSignatureError:
        return {'statusCode': 400, 'body': 'InvalidSignature'}
    except Exception as e:
        return {'statusCode': 400, 'body': str(e)}
    return {'statusCode': 200, 'body': 'OK'}

# @handler.add(FollowEvent)
# def handle_follow(event):
#     global user_data
#     global subscribe_site
#     if event.source.user_id in user_data:
#         subscribe_site=user_data[event.source.user_id]["subscribe_site"]
#     else:
#         user_data[event.source.user_id]={subscribe_site:[]}




