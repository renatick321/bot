import requests 
import random
from time import sleep


APIKEY = 'JFOlfs3vSFy7YcCFzBVVKoKI7kQxJ4'
SERVICE = 'qw'
OPERATOR = None
BAD = 8
GOOD = 6

BALANCE_URL = f"https://smshub.org/stubs/handler_api.php?api_key={APIKEY}&action=getBalance"
NUMBER_URL = f"https://smshub.org/stubs/handler_api.php?api_key={APIKEY}&action=getNumber&service={SERVICE}"

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
	"Россия": 0,
	"Украина": 1,
	"Казахстан": 2 
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
		price = float(int(price * 100)) / 100
	return price

def get_price(service, country, apikey=APIKEY):
	r = requests.get(f"http://simsms.org/priemnik.php?metod=get_service_price&country={country}&service={service}&apikey={apikey}")
	d = r.json()
	key = list(dict(d).keys())[0]
	try:
		a = d[key][service]
		price = str(price_boost(str(list(a.keys())[0]))) + ' ₽'
	except:
		price = 'Нет в наличии'
	return price

class Number:
	def __init__(self, service, country, apikey=APIKEY):
		self.country = COUNTRY[country]
		self.service = service
		self.apikey = apikey
		try:
			url = f"http://simsms.org/priemnik.php?metod=get_number&country={country}&service={service}&apikey={apikey}"
			r = requests.get(url).json()
			self.id, self.number = r["id"], r["number"]
		except:
			self.number = ""

	def __str__(self):
		return str(self.number)

	def get_sms(self):
		for i in range(240):
			sleep(1)
			r = requests.get(f"http://simsms.org/priemnik.php?metod=get_sms&country={self.country}&service={self.service}&id={self.id}&apikey={self.apikey}").json()
			print(r)
			if r["sms"]:
				return r["sms"]
		return "Аренда номера была отменена"

	def edit_status(self, status):
		r = requests.get(f"http://simsms.org/stubs/handler_api.php?api_key={self.apikey}&action=setStatus&status={status}&id={self.id}")
		return r.text

	def get_balance(self):
		r = requests.get(f"http://simsms.org/priemnik.php?metod=get_balance&service=opt4&apikey={self.apikey}")
		return r.text
