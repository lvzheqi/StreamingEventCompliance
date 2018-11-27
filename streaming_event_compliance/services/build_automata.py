from streaming_event_compliance.utils import config
from streaming_event_compliance.services.memory import ThreadMemorizer, CaseMemorizer
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
from streaming_event_compliance.services import case_thread
import threading
from streaming_event_compliance.services import set_automatos, globalvar

T = ThreadMemorizer()
C = CaseMemorizer()
threads = []
threads_index = 0
maximum_window_size = int(config.MAXIMUN_WINDOW_SIZE)
check_order_list = []


def build_automata():
    """
    Reads the training event log from utils.config.TRAINING_EVENT_LOG_PATH and build automata.
    It generates the probability between SourceNode and SinkNode with different prefix size
    and stores corresponding information into the database.
    :return: the status of the automata
    """
    # TODO: Instantiate an object Automata.
    # Read file
    event_log = None
    print('-------build_automata--------')
    print("进入build——automata之后globalvar.autos", globalvar.autos)
    print("进入build——automata之后set_automatos.get_autos()", set_automatos.get_autos())
    globalvar.autos = {}
    globalvar.autos['asd']  = 'asdfas'

    try:
        trace_log = xes_importer.import_log(config.TRAINING_EVENT_LOG_PATH)
        event_log = transform.transform_trace_log_to_event_log(trace_log)
        event_log.sort()
        print("the whole event_log:", event_log)
    except Exception:
        print("The file is in wrong Form.")
        return

    # primal_list = []
    global threads_index
    for one_event in event_log:
        event = {}
        for item in one_event.keys():
            if item == 'concept:name':
                event['activity'] = one_event.get(item)
            elif item == 'case:concept:name':
                event['case_id'] = one_event.get(item)
        # primal_list.append('case_id:' + event.get('case_id') + 'activity:' + event.get('activity'))

        # print("event:", event['activity'], "of case ", event['case_id'], "is ready.")
        if C.dictionary_cases.get(event['case_id']):
            # print('have already found the case in caseMemory', C.dictionary_cases.get(event['case_id']))
            '''if we have already found the case in caseMemory, just add this event to this case.'''
            C.dictionary_cases.get(event['case_id']).append(event['activity'])
            # print("This event is added in one case which already exists in caseMemory")
            thread = case_thread.CaseThreadForTraining(event, threads_index, T, C)
            T.dictionary_threads[threads_index] = case_thread
            # print("Now the number of T.dictionary_threads is:", len(T.dictionary_threads))
            try:
                thread.start()
            except KeyboardInterrupt:
                print('Thread is interrupt!')
            threads.append(case_thread)
            # TODO: huojingjing create thread for this event
        else:
            # print('have not found the case', event['case_id'], 'in caseMemory.')
            # 1. Add it to the caseMemory
            # 2. Create a new thread for this case
            C.dictionary_cases[event['case_id']] = ['*' for i in range(0, maximum_window_size - 1)]
            C.dictionary_cases[event['case_id']].append(event['activity'])
            # print("in caseMemory we add a new case with it's first activity:", event['case_id'], event['activity'])
            lock = threading.Lock()
            # print("we creat a lock for this new case;")
            C.lock_List[event['case_id']] = lock
            # print("Now the locklist:", C.lock_List)
            thread = case_thread.CaseThreadForTraining(event, threads_index, T, C)
            # 3. Add it into threadMemory
            T.dictionary_threads[threads_index] = case_thread
            # this is just for remember the threads information that we have created.
            # print("Now the number of T.dictionary_threads is:", len(T.dictionary_threads))
            # 4. Start it
            try:
                thread.start()
            except KeyboardInterrupt:
                print('Thread is interrupt!')
            threads.append(case_thread)
            # this is for limiting the number of the threads that are runing???
            # TODO: what does caseThread do? give another init with 4 parameters
        threads_index = threads_index + 1
        # while len(threads) > 10:
        #     threads[0].join()  # TODO: Jingjing: why we need to join these threads?
        #     del threads[0]  # why we delete?
    # TODO: raise exception when not success
    print("All events have threads running.")
    if not T.dictionary_threads:
        print("All threads are done.")
    # print('\n\n\n############################## primal list', primal_list, '#####################\n\n\n')

    # except KeyboardInterrupt:
    #     raise KeyboardInterrupt
    # except:
    #     print("Unexpected error:", sys.exc_info()[0])
    #     raise
    return True


