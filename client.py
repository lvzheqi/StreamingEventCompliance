# if __package__ is None:
#     import sys
#     from os import path
#     sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
#     from StreamEventCompliance.simulationStreamEvent import simulationStreamEvent
# else:
#     from packages.files import fileChecker


from simulationStreamEvent import eventLog
import uuid


class Client(object):
    def __init__(self, path):
        self.dictionary_threads = {}
        self.path = path
        self.uuid = str(uuid.uuid1())

    def run_compliance_checker(self):
        event_log = eventLog.read_log(self.path)
        eventLog.simulate_stream_event(self.uuid, event_log)
        return 0

    def run_show_deviation_pdf(self):
        print("pdf is on", "http://127.0.0.1:5000/show-deviation-pdf?"+self.uuid)


client1 = Client("Example.xes")
client1.run_compliance_checker()
client1.run_show_deviation_pdf()


# TODO: 1.