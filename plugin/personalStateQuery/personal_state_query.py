import json, threading
import requests
from threading import Timer
from bot.bot_interpreter import QQMessage
import bot.bot_interpreter as interpreter
import GLOBAL_CONFIG

def handle_msg(msg:QQMessage):
    try:
        test_url(msg.message.split("#")[1], msg.group_number, msg.sender_number)
    except Exception as e:
        print('发送失败')


def test_url(userid, group_number, sender_number):
    errorinfo = []
    url_base="https://api.torn.com/user/"
    url_last="?selections=profile&key=%s" % GLOBAL_CONFIG.API_KEY
    rereadtime=60
    global indexer
    if 1==1:
        resp = None
        print("Inveistigating user ["+userid+"]")
        try:
            resp = requests.get(url_base+userid+url_last, timeout=7)
            print (resp)
        except (
        requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout) as e:
            print("request exceptions:" + str(e))
            print("Inveistigate " + userid + " timeout")
            return
        else:
            if resp.status_code >= 400:
                print("response status code fail:" + str(resp.status_code))
                print("Inveistigate " + userid + " fail, status code:" + str(resp.status_code))
                return
        body = resp.text
        dct = json.loads(body)
        if ("error" in dct):
            print("API Error")
            t = Timer(rereadtime, test_url)
            t.start()
            return
        ret_message = "用户名："+str(dct.get("name"))+"\n活动："+str(dct.get("status").get("description"))+"\n状态："+str(dct.get("status").get("state"))+"\n血量："+str(dct.get("life").get("current"))+"/"+str(dct.get("life").get("maximum"))
        interpreter.send_msg(QQMessage(group_number=group_number, sender_number=sender_number, message=ret_message))


# --*-- 接口 --*-- #
personal_query_commands = {
    'id#': handle_msg
}


personal_query_commands_description = {
    'id#': 'id#[id] 查询个人状态'
}


def solve_description():
    return personal_query_commands_description


def solve_test(msg:QQMessage):
    message = msg.message.lower()
    for command in personal_query_commands.keys():
        if message.startswith(command):
            return personal_query_commands.get(command)


def solve(msg:QQMessage):
    if solve_test(msg):
        thread = threading.Thread(target=solve_test(msg), args=(msg,))
        thread.start()
