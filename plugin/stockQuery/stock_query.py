from bot.bot_interpreter import QQMessage
import bot.bot_interpreter as interpreter
import plugin.stockQuery.arson_warehouse_spider as spider
from plugin.stockQuery.foreign_item_map import *
import threading, random, re, time


# 激活spider
spider.commence_life_cycle()


# --*-- 接口 --*-- #
def get_country_by_nickname(nickname):
	for k,v in country_nickname_map.items():
		if nickname in v:
			return k


def search_flower_plushie_for(msg: QQMessage):
	message = msg.message
	nickname = message[message.find('#')+1:].lower()
	country = get_country_by_nickname(nickname)

	countries = []
	if country:
		countries = [country]
	else:
		countries = country_nickname_map.keys()

	target_ids = []
	for item_ids in [country_flower_plushie_map.get(country) for country in countries]:
		for item_id in item_ids:
			target_ids.append(item_id)

	target_dict = {}
	for item in spider.foreign_item_list:
		if item.item_id in target_ids:
			# FIXME: xanax的id有几个重复 要判断是不是南非的
			if item.item_id == 206 and item.country != 'South Africa':
				pass
			else:
				if target_dict.get(item.country):
					target_dict[item.country].append(item)
				else:
					target_dict[item.country] = [item]

	if not target_dict:
		interpreter.send_msg(QQMessage(group_number=msg.group_number, sender_number=msg.sender_number, message='查询出错'))
	else:
		ret_message = ''
		for country,items in target_dict.items():
			country_name = country_name_map[country]
			ret_message += "%s" % country_name
			if len(country_name) < 3:
				ret_message += '\t'
			ret_message += ':'
			for item in items:
				ret_message += "  %s%d" % (item_name_map[item.item_id], item.stock)
			ret_message += '\n'
		interpreter.send_msg(QQMessage(group_number=msg.group_number, sender_number=msg.sender_number, message=ret_message[:-1]))
	return


# --*-- 接口 --*-- #
stock_query_commands = {
	'ff#': search_flower_plushie_for
}

stock_query_commands_description = {
	'ff#': 'ff#[国家] 查询对应国家的飞花库存 留空则返回所有国家数据'
}

#
def solve_description():
	return stock_query_commands_description


def solve_test(msg:QQMessage):
	message = msg.message.lower()
	for command in stock_query_commands.keys():
		if message.startswith(command):
			return stock_query_commands.get(command)


def solve(msg:QQMessage):
	if solve_test(msg):
		thread = threading.Thread(target=solve_test(msg), args=(msg,))
		thread.start()


if __name__ == '__main__':
	content = '[TTT]Mirrorr[2564936]'
	result = re.search('.*?([a-zA-Z0-9]*?)\[.*?', content)
	print(result.group())
	pass