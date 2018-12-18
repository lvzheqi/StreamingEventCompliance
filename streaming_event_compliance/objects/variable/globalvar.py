from typing import Any


class GlobalVars:
    def __init__(self):
        self.autos = {}
        self.auto_status = 0
        self.alert_logs = {}
        self.clients_status = {}
        self.clients_cc_status = {}

    def get_autos_status(self):
        return self.auto_status

    def get_client_alert_logs(self, uuid):
        return self.alert_logs[uuid]

    def get_client_status(self, uuid):
        return self.clients_status[uuid]

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class ThreadMemorizer(object):
    '''
    This object is for storing the threads that server creates for each case;
    '''

    def __init__(self):
        self.dictionary_threads = {}

    def clear_memorizer(self):
        self.dictionary_threads = {}

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class CaseMemorizer(object):
    '''
    This object is for storing the cases that server receives;

    key:'case_id'
    value:[a,b,c,d...] events sorting by timestamp, but we don't need to sort these events, and it also doesn't contain any timestamp
                    but the events are sent by Client in the order of time, even they are sent by multi-threads, the server will get
                    these events in the order of time. So when server get a event, it can only check its case_id and add it into the
                    corresponding list.
    '''

    def __init__(self):
        self.dictionary_cases = {}
        self.lock_List = {}

    def clear_memorizer(self):
        self.dictionary_cases = {}
        self.lock_List = {}

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class ConnectionsLocker(object):
    '''
    This object is for storing the threads that server creates for each case;
    '''

    def __init__(self):
        self.lock_List = {}

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class ClientThreadMemorizer(ThreadMemorizer):
    def __init__(self):
        super().__init__()
        self.client_number = 0

    def clear_client_memorizer(self, uuid):
        self.dictionary_threads[uuid] = {}


class ClientCaseMemorizer(CaseMemorizer):
    def __init__(self):
        super().__init__()
        self.client_number = 0

    def clear_client_memorizer(self, uuid):
        self.dictionary_cases[uuid] = {}
        self.lock_List[uuid] = {}


T = ThreadMemorizer()
C = CaseMemorizer()
CL = ConnectionsLocker()

CTM = ClientThreadMemorizer()
CCM = ClientCaseMemorizer()

gVars = GlobalVars()


