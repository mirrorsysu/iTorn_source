import requests
import threading, time, json
DATA_SOURCE_URL = 'https://arsonwarehouse.com/api/v1/foreign-stock'

class ForeignItem:
	def __init__(self, item_id, country, price, stock, reported_at):
		super(ForeignItem, self).__init__()
		self.item_id = int(item_id)
		self.country = str(country)
		self.price = int(price)
		self.stock = int(stock)
		self.reported_at = str(reported_at)


foreign_item_list = []


def update_foreign_items(items):
	global foreign_item_list
	new_list = []
	for item in items:
		item_id = item.get('item_id')
		country = item.get('country')
		price = item.get('price')
		stock = item.get('stock')
		reported_at = item.get('reported_at')
		new_list.append(ForeignItem(item_id, country, price, stock, reported_at))
	foreign_item_list = new_list[:]


def request_and_parse():
	r = requests.get(DATA_SOURCE_URL)
	if r.status_code != 200:
		return
	j = r.json()
	if j.get('items'):
		items = j.get('items')
		update_foreign_items(items)


def spider_life_cycle():
	while 1:
		try:
			request_and_parse()
		except Exception as e:
			print('库存爬虫似乎出错了')
		print('stock.query.heartbeat')
		time.sleep(30)


def commence_life_cycle():
	thread = threading.Thread(target=spider_life_cycle)
	thread.start()


if __name__ == '__main__':
	commence_life_cycle()