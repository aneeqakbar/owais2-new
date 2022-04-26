from email import message
from django.shortcuts import render, redirect
from httplib2 import Http
from home.models import User
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import os.path
from scrapper.cron import fetch_telegram_b_data, fetch_telegram_data, fetch_reddit_data
from telegramBot.models import Telegram_Accounts
from telegramBot.models import Telegram_Groups
from telegramBot.models import Telegram_Questions
from telegramBot.models import Telegram_Answers
from telegramBot.models import Schedule_Messages
from django.conf import settings
import time
import asyncio
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import *
from telethon import functions
import sys
from datetime import datetime
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler


PROFILE_PIC_FOLDER='static/images/profile-pics/' 
TELEGRAM_SESSIONS_FOLDER= settings.BASE_DIR
# Create your views here.

def some_task():
    print('Tick! The time is: %s' % datetime.now())

    data = Schedule_Messages(userid=1, message="xxx", account_id=1, group="xxx", delay = 1, date="xxxx", time="xxxx",status="xxxx")
    data.save()

    data = Schedule_Messages.objects.all().filter(status="pending")
    for i in data:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")
        tm_string = now.strftime("%H:%M")
        print("time-now = ",tm_string)
        if i.date == dt_string and i.time==tm_string:
            print("chal gaya xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print(i.message)

            group_name = i.group
            account_id = i.account_id
            chat = i.message
            sleep_time_first = i.delay

            print(group_name, chat, account_id, sleep_time_first, datetime)
            TelegramAccount = Telegram_Accounts.objects.all().filter(id=account_id)
            phone = TelegramAccount[0].number
            api_id = TelegramAccount[0].hash_id
            api_hash = TelegramAccount[0].hash_key
            sleep_time = 2
            sleep_time_first = int(sleep_time_first)
            print(phone,api_hash,api_id)
            try:
                client = telegram_client(phone, api_id, api_hash)
                print('Account login successfully')
            except PhoneCodeInvalidError:
                sys.exit('You enter the wrong code.')
            client(functions.channels.JoinChannelRequest(channel=group_name))
            print('Bot send message after '+str(sleep_time_first)+' seconds.')
            time.sleep(sleep_time_first)
            while True:
                try:
                    client.send_message(group_name, str(chat))
                    print('Question send successfully. Bot sleep for '+str(sleep_time)+ ' seconds.')
                    client.disconnect()
                    t = Schedule_Messages.objects.get(id=i.id)
                    t.status = "completed"
                    t.save()
                    return HttpResponse('Chat send successfully')         
                    account = Telegram_Accounts.objects.all().filter(id=id)
                    user_data = User.objects.all().filter(id=request.session.get('userid'))
                    groups = Telegram_Groups.objects.all().filter(userid=request.session.get('userid'),account_id=id)
                    questions = Telegram_Questions.objects.all().filter(userid=request.session.get('userid'),account_id=id)
                    context= {"username":request.session.get('username'),"user_data":user_data,"account":account, "category":"question","groups":groups,"questions":questions,"sent":"true","group_name":group_name}
                    return render(request,"telegramBot/telegram-bot-send.html",context)
                    column += 1
                    time.sleep(sleep_time)
                except IndexError:         
                    client.disconnect()
                    print("All questions completed in "+group_name+' group.\n')
                    print()
                    return HttpResponse("All questions completed in "+group_name+' group.\n')
                    url = "/telegramBot/telegram-dmBot-send/"+id
                    return HttpResponseRedirect(url)
                except FloodError:         
                    client.disconnect()
                    print('Due to many messages in group bot stops (Flood error).')
                    return HttpResponse('Due to many messages in group bot stops (Flood error).')
                    sys.exit()
                    url = "/telegramBot/telegram-dmBot-send/"+id
                    return HttpResponseRedirect(url)
                except FloodWaitError:         
                    client.disconnect()
                    print('Due to many messages in group bot stops (Flood error).')
                    sys.exit()
                    url = "/telegramBot/telegram-dmBot-send/"+id
                    return HttpResponseRedirect(url)
                except Exception as e:         
                    client.disconnect()
                    print(e)
                    return HttpResponse(e)
                    sys.exit()
                    url = "/telegramBot/telegram-dmBot-send/"+id
                    return HttpResponseRedirect(url)

                except Exception as e:         
                    client.disconnect()
                    print(e)
                    url = "/telegramBot/telegram-dmBot-send/"+id
                    return HttpResponseRedirect(url)

def telegram_client(phone, api_id, api_hash):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # client = TelegramClient(phone, api_id, api_hash)
    client = TelegramClient(phone, api_id, api_hash, loop=loop)
    time.sleep(3)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))
    return client


def start_jobs():
    scheduler = BackgroundScheduler()
    cron_interval = {'month': '*', 'day': '*', 'hour': '*', 'minute':'*/30'}
    # fetch_telegram_data()
    # fetch_telegram_b_data()
    # fetch_reddit_data()
    scheduler.add_job(fetch_telegram_data, 'cron', **cron_interval)
    scheduler.add_job(fetch_telegram_b_data, 'cron', **cron_interval)
    scheduler.add_job(fetch_reddit_data, 'cron', **cron_interval)

    #Set cron to runs every 20 min.
    # cron_job = {'month': '*', 'day': '*', 'hour': '*', 'minute':'*/20'}
    #Add our task to scheduler.
    # scheduler.add_job(some_task, 'cron', **cron_job)
    # scheduler.add_job(fetch_telegram_data_b, 'interval', seconds=180)
    scheduler.start()
