import http.client, urllib
from src.utils import truncate_string

class PushoverClient:
    def __init__(self, PUSHOVER_APP_TOKEN, PUSHOVER_USER_KEY, send_notification):
        self.PUSHOVER_APP_TOKEN = PUSHOVER_APP_TOKEN
        self.PUSHOVER_USER_KEY = PUSHOVER_USER_KEY
        self.send_notification = send_notification
        self.conn = http.client.HTTPSConnection("api.pushover.net:443")

    def send_message(self, message):                         
        try:
            # Documentation: https://support.pushover.net/i44-example-code-and-pushover-libraries#python
            self.conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
                "token": self.PUSHOVER_APP_TOKEN,    # "APP_TOKEN"
                "user": self.PUSHOVER_USER_KEY,      # "USER_KEY",
                "message": message,
            }), { "Content-type": "application/x-www-form-urlencoded" })
            
            response = self.conn.getresponse()
            response_data = response.read()
            print(response.status, response.reason, response_data)

        except Exception as e:
            print("Error:", e)

    def send_multiple_messages(self, messages):
        # Отправка нескольких сообщений
        for title in messages:
            if self.send_notification:
                self.send_message(title)
