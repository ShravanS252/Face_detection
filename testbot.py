import requests
TOKEN = "6023019811:AAGs4-feVKo6XRlH_PpdoHVXkOA-qVM5hkE"
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
# print(requests.get(url).json())
chat_id = "5893637739"
message = "hello from your telegram bot"
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
print(requests.get(url).json())