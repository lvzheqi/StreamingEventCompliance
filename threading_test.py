from threading import Thread
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
from threading import Thread
from time import sleep
import logging

class ThreadMemorizer(object):
    def __init__(self):
        self.dictionary_threads = {}

class EventThread(Thread):
    def __init__(self, event, threadMemorizer, index):
        self.event = event
        self.threadMemorizer = threadMemorizer
        self.index = index
        Thread.__init__(self)

    def run(self):
        while True:
            #print(event)
            #sleep(0.5)
            print("number of threads ",len(list(self.threadMemorizer.dictionary_threads.keys())))
            #sleep(0.01)
            #del self.threadMemorizer.dictionary_threads[self.index]
            break

T = ThreadMemorizer()
trace_log = xes_importer.import_log("C:\\running-example.xes")
event_log = transform.transform_trace_log_to_event_log(trace_log)
threads = []
for index, event in enumerate(event_log):
    #print(event)
    while len(threads) > 3:
        threads[0].join()
        del threads[0]
    event_thread = EventThread(event, T, index)
    T.dictionary_threads[index] = event_thread
    event_thread.start()
    threads.append(event_thread)
    #event_thread.join()

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(filename='example.log',level=logging.WARNING,format=FORMAT)
logging.error("hello")