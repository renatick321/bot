import requests 
import random
from time import sleep


APIKEY = '7de84f495dee36bd83cd2Ac39d09Adb6'
SERVICE = 'qw'
OPERATOR = None
BAD = 8
GOOD = 6

smshub = {
    "Telegram": "tg",
    "Вконтакте": "vk",
    "Whatsapp": "wa",
    "Avito": "av",
    "Qiwi": "qw",
    "Пятерочка": "bd",
    "McDonalds": "ry",
    "PayPal": "ts",
    "Burger King": "ip",
    "Яндекс": "ya",
    "BlaBlaCar": "ua",
    "Instagram": "ig",
    "Google": "go",
    "Steam": "mt",
         }

COUNTRY = {
	"Россия": "0",
	"Украина": "1",
	"Казахстан": "2" 
		  }
#  Сразу после получения номера доступны следующие действия:
#  8 - Отменить активацию
#  1 - Сообщить, что SMS отправлена (необязательно)
#  Для активации со статусом 1:
#  8 - Отменить активацию
# ==========================================================
#  Сразу после получения кода:
#  3 - Запросить еще одну смс
#  6 - Подтвердить SMS-код и завершить активацию
#  Для активации со статусом 3:
#  6 - Подтвердить SMS-код и завершить активацию
def info():
	l = [
	' Сразу после получения номера доступны следующие действия:',
	' 8 - Отменить активацию',
	' 1 - Сообщить, что SMS отправлена (необязательно)',
	' Для активации со статусом 1:',
	' 8 - Отменить активацию',
	'==========================================================',
	' Сразу после получения кода:',
	' 3 - Запросить еще одну смс',
	' 6 - Подтвердить SMS-код и завершить активацию',
	' Для активации со статусом 3:',
	' 6 - Подтвердить SMS-код и завершить активацию'
		]
	print("\n".join(l))

def price_boost(price):
	price = float(price)
	if price < 1.5:
		price = 3
	elif price <= 5:
		price = 7
	elif price < 7:
		price = 8
	else:
		price *= 1.7
		price = float(int(price * 100)) / 100 + 0.9
	return price

def get_price(service, country, apikey=APIKEY):
	r = requests.get("https://sms-activate.ru/stubs/handler_api.php?api_key={}&action=getPrices&service={}&country={}".format(APIKEY, service, COUNTRY[country]))
	d = r.json()
	try:
		c = d[COUNTRY[country]]
		print(c)
		print(c[service])
		print(c[service]["count"])
		a = price_boost(c[service]["cost"])
		price = str(a) + ' ₽'
		if c[service]["count"] == 0:
		    price = 'Нет в наличии'
	except:
		price = 'Нет в наличии'
	return price

class Number:
	def __init__(self, service, country, apikey=APIKEY):
		self.country = COUNTRY[country]
		self.service = service
		self.apikey = apikey
		try:
			url = "https://sms-activate.ru/stubs/handler_api.php?api_key={}&action=getNumber&service={}&country={}".format(self.apikey, self.service, self.country)
			r = requests.get(url).text
			b = False if r == 'NO_NUMBERS' or r == 'NO_BALANCE' else True
			try:
			    s, self.id, self.number = map(str, r.split(":"))
			except:
			    s, self.id, self.number, token = map(str, r.split(":"))
		except:
			self.number = ""

	def __str__(self):
		return str(self.number)

	def get_sms(self):
		for i in range(240):
			sleep(1)
			r = requests.get("https://sms-activate.ru/stubs/handler_api.php?api_key={}&action=getStatus&id={}".format(self.apikey, self.id)).text
			print(r)
			if "STATUS_OK" in r:
				return r[len("STATUS_OK:"):]
			elif "STATUS_CANCEL" == r:
				return "Аренда номера была отменена"
		return "Аренда номера была отменена"

	def edit_status(self, status):
		r = requests.get("https://sms-activate.ru/stubs/handler_api.php?api_key={}&action=setStatus&status={}&id={}".format(self.apikey, status, self.id))
		return r.text

	def get_balance(self):
		r = requests.get("https://sms-activate.ru/stubs/handler_api.php?api_key={}&action=getBalance".format(self.apikey))
		return r.text