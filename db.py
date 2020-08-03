import sqlite3
from config import DB_URL, password_create
from datetime import datetime, timedelta

def user_create(id):
	conn = sqlite3.connect(DB_URL)
	cursor = conn.cursor()
	cursor.execute("INSERT INTO Users(cash, user_id, dt) SELECT 0, {}, '{}' WHERE NOT EXISTS(SELECT 1 FROM Users WHERE user_id = {})".format(id, datetime.now().strftime('%Y-%m-%d'), id))
	conn.commit()

def buy(name, num, user_id, price):
	conn = sqlite3.connect(DB_URL)
	cursor = conn.cursor()
	for i in cursor.execute("SELECT cash FROM Users WHERE user_id={}".format(user_id)):
		a = i[0]
	summa = a - price
	cursor.execute("UPDATE Users SET cash = {} WHERE user_id = {}".format(summa, user_id))	
	cursor.execute("INSERT INTO History(name, price, num, dt, user_id) VALUES ('{}', {}, {}, '{}', {})".format(name, price, num, datetime.now().strftime('%Y-%m-%d %I:%M:%S'), user_id))
	conn.commit()

def get_balance(user_id):
	conn = sqlite3.connect(DB_URL)
	cursor = conn.cursor()
	for i in cursor.execute("SELECT cash FROM Users WHERE user_id={}".format(user_id)):
		a = i[0]
		return float(a)
	

def get_info(user_id):
	conn = sqlite3.connect(DB_URL)
	cursor = conn.cursor()
	lst = []
	for i in cursor.execute("SELECT price FROM History WHERE user_id={}".format(user_id)):
		lst.append(i[0])
	return lst

def get_comment():
	conn = sqlite3.connect(DB_URL)
	cursor = conn.cursor()
	for i in cursor.execute("SELECT comment FROM Comment"):
		a = i[0] + 1
		break
	cursor.execute("UPDATE Comment SET comment = {}".format(a))
	conn.commit()
	return a

def replenishment(user_id, cash):
	conn = sqlite3.connect(DB_URL)
	cursor = conn.cursor()
	for i in cursor.execute("SELECT cash FROM Users WHERE user_id = {}".format(user_id)):
		a = float(i[0])
		break
	cursor.execute("UPDATE Users SET cash = {} WHERE user_id = {}".format(a + cash, user_id))
	conn.commit()

def get_cupon(cash):
	conn = sqlite3.connect(DB_URL)
	cursor = conn.cursor()
	cupon = password_create()
	cursor.execute("INSERT INTO Coupons(name, cash) VALUES ('{}', {})".format(cupon, cash))
	conn.commit()
	return cupon

def cupon_activate(user_id, name):
	conn = sqlite3.connect(DB_URL)
	cursor = conn.cursor()
	try: 
		for i in cursor.execute("SELECT cash FROM Coupons WHERE name = '{}'".format(name)):
			a = i[0]
			s = "Купон активирован"
			break
		print()
		print(a)
		print()
		replenishment(user_id, a)
		cursor.execute("DELETE FROM Coupons WHERE name = '{}'".format(name))
	except:
		s = "Купон не найден"
	conn.commit()
	return s

def get_last_payment(user_id):
	conn = sqlite3.connect(DB_URL)
	cursor = conn.cursor()
	lst = []
	for i in cursor.execute("SELECT price FROM History WHERE user_id = {}".format(user_id)):
		lst.append(i[0])
	return lst[::-1][0]

def info():
	s = ''
	conn = sqlite3.connect(DB_URL)
	cursor = conn.cursor()
	user_gain = 0
	for i in cursor.execute("SELECT * FROM Users WHERE dt = '{}';".format(datetime.now().strftime('%Y-%m-%d'))):
		user_gain += 1
	s += "Новых пользователей: {}\n".format(user_gain)
	users = 0
	for i in cursor.execute("SELECT * FROM Users"):
		users += 1
	s = "Всего пользователей: {}\n".format(users) + s
	month0 = str(datetime.now().month)
	month1 = str(datetime.now().month + 1) if datetime.now().month + 1 > 12 else "01"
	year = str(datetime.now().year)
	all_lst = []
	for i in cursor.execute("SELECT price FROM History"):
		all_lst.append(i[0])
	s += "Всего продаж: {}\n".format(len(all_lst))
	s += "Заработано за всё время: {}\n".format(sum(all_lst))
	month_lst = []
	date0 = year+"-"+month0+"-"+"01"
	date1 = year+"-"+month1+"-"+"01"
	for i in cursor.execute("SELECT price FROM History WHERE dt BETWEEN '{}' AND '{}'".format(date0, date1)):
		month_lst.append(i[0])
	s += "Продаж за 30 дней: {}\n".format(len(month_lst))
	s += "Заработано за 30 дней: {}\n".format(sum(month_lst))
	week_lst = []
	for i in cursor.execute("SELECT price FROM History WHERE dt BETWEEN '{}' AND '{}'".format((datetime.now()-timedelta(days = 7)).strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d'))):
		week_lst.append(i[0])
	s += "Продаж за 7 дней: {}\n".format(len(week_lst))
	s += "Заработано за 7 дней: {}\n".format(sum(week_lst))
	daily_lst = []
	for i in cursor.execute("SELECT price FROM History WHERE dt = '{}'".format(datetime.now().strftime('%Y-%m-%d'))):
		daily_lst.append(i[0])
	s += "Продаж за 7 дней: {}\n".format(len(daily_lst))
	s += "Заработано за 7 дней: {}\n".format(sum(daily_lst))
	return s

def get_users():
	conn = sqlite3.connect(DB_URL)
	cursor = conn.cursor()
	users = []
	for i in cursor.execute("SELECT user_id FROM Users"):
		users.append(i[0])
	return users