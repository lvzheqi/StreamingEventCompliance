from threading import Thread
import requests


class EventThread(Thread):
    def __init__(self, event, client_uuid):
        self.event = event
        self.client_uuid = client_uuid
        Thread.__init__(self)

    def run(self):
        try:
            r = requests.post('http://127.0.0.1:5000/compliance-checker?uuid=' + self.client_uuid, json=self.event)
            if r.status_code != 200:
                print('Error: error by compliance checking')
            else:
                print("Info:", r.text)
        except Exception:
            print('The server is disconnect, please try again later')



