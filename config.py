import random


TOKEN = "1368859513:AAH5QLYrPtm4Td1nESdOfxmbiJinqqC4PPc"
DB_URL = "db.db"


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

CHARS = 'abcdefghijklnopqrstuvwxyz1234567890'
LETTERS = "abcdefghijklnopqrstuvwxyz"


def password_create(length=16):
	password = ''
	for i in range(length):
		password += random.choice(CHARS)
	return password