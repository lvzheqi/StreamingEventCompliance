from streaming_event_compliance.services.globalvar import ThreadMemorizer, CaseMemorizer
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
from streaming_event_compliance.services.build_automata import case_thread
import threading
from streaming_event_compliance.utils.config import MAXIMUN_WINDOW_SIZE, WINDOW_SIZE
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.utils import config
from streaming_event_compliance.services import set_globalvar
from multiprocessing import Process

T = ThreadMemorizer()
C = CaseMemorizer()
threads = []
threads_index = 0


def build_automata():
    print("---------------------Start: Traininging automata starts!--------------------------------------")
    process_ = Process(target=build_automata_pro())
    process_.start()
    process_.join()
    autos, status = set_globalvar.get_autos()
    for ws in WINDOW_SIZE:
        autos[ws].set_probability()
    dbtools.insert_node_and_connection(autos)
    print("---------------------End: Everything for training automata is Done!---------------------------")


def build_automata_pro():
    """
    Reads the training event logger from database.config.TRAINING_EVENT_LOG_PATH and build automata.
    It generates the probability between SourceNode and SinkNode with different prefix size
    and stores corresponding information into the database.
    :return:
    """

    # Read file
    try:
        trace_log = xes_importer.import_log(config.TRAINING_EVENT_LOG_PATH)
        event_log = transform.transform_trace_log_to_event_log(trace_log)
        event_log.sort()
    except Exception:
        print('Error: The file is in wrong Form.')
        return

    global threads_index
    for one_event in event_log:
        event = {}
        for item in one_event.keys():
            if item == 'concept:name':
                event['activity'] = one_event.get(item)
            elif item == 'case:concept:name':
                event['case_id'] = one_event.get(item)

        # Create thread for each event
        if C.dictionary_cases.get(event['case_id']):
            C.dictionary_cases.get(event['case_id']).append(event['activity'])
            thread = case_thread.CaseThreadForTraining(event, threads_index, T, C)
            T.dictionary_threads[threads_index] = case_thread
            try:
                thread.start()
            except KeyboardInterrupt:
                print('Error: Thread is interrupt!')
        else:
            C.dictionary_cases[event['case_id']] = ['*' for i in range(0, MAXIMUN_WINDOW_SIZE)]
            C.dictionary_cases[event['case_id']].append(event['activity'])
            lock = threading.Lock()
            # Create a lock for the new case
            C.lock_List[event['case_id']] = lock
            thread = case_thread.CaseThreadForTraining(event, threads_index, T, C)
            T.dictionary_threads[threads_index] = case_thread
            try:
                thread.start()
            except KeyboardInterrupt:
                print('Error: Thread is interrupt!')

        threads.append(thread)
        threads_index = threads_index + 1
    # TODO: Jinjing raise exception when not success
    # for th in threads:
    #     th.join()
    #     print(th, "is done")

