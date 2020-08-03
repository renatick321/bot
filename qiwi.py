import requests


TOKEN = "b2d4112b90cf66c965e5173d9d041f95"
MAIN_URL = "https://edge.qiwi.com"

NUMBER = '79051190153'

def get_comments(length=15):
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": "Bearer {TOKEN}".format(TOKEN)
			  }
	comments = {}
	r = requests.get("https://edge.qiwi.com/payment-history/v2/persons/{}/payments?rows={}".format(NUMBER, length), headers=headers).json()
	for i in r["data"]:
		a = "r" if i["comment"] is None else i["comment"]
		comments[a] = i["sum"]["amount"]
	print(comments)
	return comments