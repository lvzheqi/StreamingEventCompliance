

from simulationStreamEvent import eventLog
# import uuid


class Client(object):
    def __init__(self, user_name, path):
        self.dictionary_threads = {}
        self.path = path
        self.uuid = user_name

    def run_compliance_checker(self):
        event_log = eventLog.read_log(self.path)
        eventLog.simulate_stream_event(self.uuid, event_log)
        return 0

    def run_show_deviation_pdf(self):
        print("PDF is on", "http://127.0.0.1:5000/show-deviation-pdf?uuid="+self.uuid)


client1 = Client("client1", "Example.xes")
client1.run_compliance_checker()
client1.run_show_deviation_pdf()


# TODO: 1.