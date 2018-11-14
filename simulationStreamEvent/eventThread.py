from threading import Thread
import logging
import requests


class ThreadMemorizer(object):
    def __init__(self):
        self.dictionary_threads = {}


class EventThread(Thread):
    def __init__(self, event, threadMemorizer, index, client_uuid):
        self.event = event
        self.threadMemorizer = threadMemorizer
        self.index = index
        self.client_uuid = client_uuid
        Thread.__init__(self)

    def run(self):
        while True:
            print("number of threads ", len(list(self.threadMemorizer.dictionary_threads.keys())))
            r = requests.post("http://127.0.0.1:5000/compliance-checker?uuid=" + self.client_uuid, json=self.event)
            print(r.text)
            del self.threadMemorizer.dictionary_threads[self.index]
            break



# FORMAT = '%(asctime)-15s %(message)s'
# logging.basicConfig(filename='example.log',level=logging.WARNING,format=FORMAT)
# logging.error("hello")