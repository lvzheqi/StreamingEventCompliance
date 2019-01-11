from typing import Any


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance


class GlobalVars(Singleton):
    def __init__(self):
        self.autos = {}
        self.auto_status = 0
        self.alert_logs = {}
        self.clients_status = {}
        self.clients_cc_status = {}

    def get_autos_status(self):
        return self.auto_status

    def get_client_alert_logs(self, uuid):
        return self.alert_logs.get(uuid)

    def get_client_status(self, uuid):
        return self.clients_status[uuid]

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class ThreadMemorizer(Singleton):
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


class CaseMemorizer(Singleton):
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


class ConnectionsLocker(Singleton):
    '''
    This object is for storing the threads that server creates for each case;
    '''

    def __init__(self):
        self.lock_list = {}

    def clear_memorizer(self):
        self.lock_list = {}

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class ClientThreadMemorizer(Singleton):
    def __init__(self):
        super().__init__()
        self.client_number = 0
        self.dictionary_threads = {}

    def init_client_memorizer(self, uuid):
        self.dictionary_threads[uuid] = []

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class ClientCaseMemorizer(Singleton):
    def __init__(self):
        super().__init__()
        self.client_number = 0
        self.dictionary_cases = {}
        self.lock_List = {}

    def init_client_memorizer(self, uuid):
        self.dictionary_cases[uuid] = {}
        self.lock_List[uuid] = {}

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class ClientAlertsLocker(Singleton):
    '''
    This object is for storing the threads that server creates for each case;
    '''

    def __init__(self):
        self.c_alerts_lock_list = {}

    def init_client_memorizer(self, uuid):
        self.c_alerts_lock_list[uuid] = {}

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


T = ThreadMemorizer()
C = CaseMemorizer()
CL = ConnectionsLocker()

CTM = ClientThreadMemorizer()
CCM = ClientCaseMemorizer()
CAL = ClientAlertsLocker()

gVars = GlobalVars()


