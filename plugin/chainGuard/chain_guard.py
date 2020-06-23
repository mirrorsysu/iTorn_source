from bot.bot_interpreter import QQMessage
import bot.bot_interpreter as interpreter
from torn import APICenter
import threading

# --*-- 汇总 --*-- #
def query_chain_simple(msg):
    raw_message = APICenter.chain_simple_info_make()
    interpreter.send_msg(QQMessage(message=raw_message, group_number=msg.group_number, sender_number=msg.sender_number))


def query_chain_detail(msg):
    raw_message = APICenter.chain_detail_info_make()
    interpreter.send_msg(QQMessage(message=raw_message, group_number=msg.group_number, sender_number=msg.sender_number))


# --*-- 接口 --*-- #
chain_guard_commands = {
    '查询': query_chain_simple,
    '状态': query_chain_detail
}

chain_guard_commands_description = {
    '查询': '返回简单的chain状态',
    '状态': '返回详细的chain状态',
}
#
def solve_description():
    return chain_guard_commands_description


def solve_test(msg: QQMessage):
    command = msg.message
    return chain_guard_commands.get(command)


def solve(msg: QQMessage):
    if solve_test(msg):
        thread = threading.Thread(target=solve_test(msg), args=(msg,))
        thread.start()

if __name__ == '__main__':
    print(type(query_chain_simple))
