from typing import Any


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance


class GlobalVars(Singleton):
    """
    Description:
        This class contains variables that are used as global varibales.

    Instance Variables:
    autos: :`dict`={int, class `streaming_event_compliance.object.automata.automata.Automata`}
                   {windowsize: Automata object}.
    auto_status: :int after training automata, this will be set as 1.
    alert_logs: :`dict`={`string`: {int: class `streaming_event_compliance.object.automata.alertlog.AlertLog`}}
                        {clientid: {windowsize: AlertLog object}}
    clients_status: :`dict`={`string`: Boolean} {client_id: true/false} This will be set to true after the compliance
                    checker for this client is done.
    clients_cc_status: :`dict`={`string`: Boolean} {client_id: true/false} This will be set to true when the compliance
                    checker for this client begins.
    """
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
    """
    Description:
        This class is for storing the threads that server creates for each case.

    Instance Variables:
    dictionary_threads: :`dict`={int:
        class `streaming_event_compliance.services.build_automata.case_thread.CaseThreadForTraining`}
    """
    def __init__(self):
        self.dictionary_threads = {}

    def clear_memorizer(self):
        self.dictionary_threads = {}

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class CaseMemorizer(Singleton):
    """
    Description:
        This class is for storing the cases that server receives.

    Instance Variables:
    dictionary_cases: :`dict`={`string`: `list`} {case_id: [a,b,c,d...]} event list [a,b,c,d...] that is sorted by
        timestamp, we don't need to sort these events, and it also doesn't contain any timestamp, but the events
        are sent by Client in the order of time, even they are sent by multi-threads, the server will get these events
        in the order of time. So when server get a event, it can only check its case_id and add it into the
        corresponding list.
    lock_List: :`dict`={`string`: `threading.RLock`} {case_id: RLock object}
    """
    def __init__(self):
        self.dictionary_cases = {}
        self.event_iterator = {}
        self.lock_List = {} # here for each case we store the index of current event which will be processed

    def clear_memorizer(self):
        self.dictionary_cases = {}
        self.lock_List = {}

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class ConnectionsLocker(Singleton):
    """
    Description:
        This class is for storing the connection locks.

    Instance Variables:
    dictionary_threads: :`dict`={`tuple`: `threading.RLock`} {(source_node, sink_node): RLock object}
    """
    def __init__(self):
        self.lock_list = {}

    def clear_memorizer(self):
        self.lock_list = {}

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class ClientThreadMemorizer(Singleton):
    """
    Description:
        This class is for storing the threads that server creates for each client.

    Instance Variables:
    client_number: :int
    dictionary_threads: :`dict`={`string`: `list`} {client_id:
    [class `streaming_event_compliance.services.compliance_check.compliance_check_cc.CaseThreadForCC`...]}
    """
    def __init__(self):
        super().__init__()
        self.dictionary_threads = {}

    def init_client_memorizer(self, uuid):
        self.dictionary_threads[uuid] = []

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class ClientCaseMemorizer(Singleton):
    """
    Description:
        This class is for storing the cases that server creates for each client.

    Instance Variables:
    dictionary_cases: :`dict`={`string`: {`string`: `list`}} {client_id: {case_id: [a,b,c,d...]}}
    lock_List: :`dict`={`string`: {`string`: `threading.RLock`}} {client_id: {case_id: RLock object}}
    """
    def __init__(self):
        super().__init__()
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
    """
    Description:
        This class is for storing the locks for each alert.

    Instance Variables:
    c_alerts_lock_list: :`dict`={`string`: {`tuple`: `threading.RLock`}}
                                {client_id: {(source_node, sink_node): RLock object}}
    """
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


