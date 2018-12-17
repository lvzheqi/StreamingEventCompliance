from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
from streaming_event_compliance.services.build_automata import case_thread
import threading
from streaming_event_compliance.utils.config import MAXIMUN_WINDOW_SIZE, WINDOW_SIZE
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.utils import config
from streaming_event_compliance.services import globalvar
from streaming_event_compliance.objects.exceptions.exception import ReadFileException, ThreadException, EventException
from multiprocessing import Process
import traceback


threads = []
threads_index = 0


def build_automata():
    print("---------------------Start: Traininging automata starts!--------------------------------------")
    try:
        process_ = Process(target=build_automata_pro())
        process_.start()
        process_.join()
    except ThreadException as ec:
        raise ec
    else:
        autos = globalvar.get_autos()
        for ws in WINDOW_SIZE:
            autos[ws].set_probability()
        dbtools.insert_node_and_connection(autos)
        print("---------------------End: Everything for training automata is Done!---------------------------")
    finally:
        globalvar.set_auto_status()
        globalvar.clear_memorizer()


def build_automata_pro():
    """
        Reads the training event logger from database.config.TRAINING_EVENT_LOG_PATH and build automata.
        It generates the probability between SourceNode and SinkNode with different prefix size
        and stores corresponding information into the database.
    :return:
    """
    C = globalvar.get_case_memory()
    T = globalvar.get_thread_memory()
    try:
        trace_log = xes_importer.import_log(config.TRAINING_EVENT_LOG_PATH)
        event_log = transform.transform_trace_log_to_event_log(trace_log)
        event_log.sort()
    except Exception:
        raise ReadFileException(config.TRAINING_EVENT_LOG_PATH)

    global threads_index
    for one_event in event_log:
        event = {}
        try:
            for item in one_event.keys():
                if item == 'concept:name':
                    event['activity'] = one_event.get(item)
                elif item == 'case:concept:name':
                    event['case_id'] = one_event.get(item)
        except AttributeError:
            raise EventException(event)
        else:
            try:
                if C.dictionary_cases.get(event['case_id']):
                    C.dictionary_cases.get(event['case_id']).append(event['activity'])
                    thread = case_thread.CaseThreadForTraining(event, threads_index, T, C)
                    T.dictionary_threads[threads_index] = thread
                    thread.start()
                else:
                    C.dictionary_cases[event['case_id']] = ['*' for i in range(0, MAXIMUN_WINDOW_SIZE)]
                    C.dictionary_cases[event['case_id']].append(event['activity'])
                    lock = threading.RLock()
                    C.lock_List[event['case_id']] = lock
                    thread = case_thread.CaseThreadForTraining(event, threads_index, T, C)
                    T.dictionary_threads[threads_index] = thread
                    thread.start()
            except Exception:
                raise ThreadException(traceback.format_exc())
            else:
                threads.append(thread)
                threads_index = threads_index + 1

    #TODO:Jingjing-This join can be done after adding end event?
    try:
        for th in threads:
            th.join_with_exception()
    except Exception:
        raise ThreadException(traceback.format_exc())
    else:
        print('----------------------------------------------------------------------------------------------\n')
        for item in C.dictionary_cases:
            print(len(C.dictionary_cases.get(item)), C.dictionary_cases.get(item))
        print('----------------------------------------------------------------------------------------------\n')
        end_message = {}
        for item in C.dictionary_cases:
            end_message['case_id'] = item
            end_message['activity'] = '!@#$%^'
            C.dictionary_cases.get(item).append(end_message['activity'])
            thread = case_thread.CaseThreadForTraining(end_message, threads_index, T, C)
            thread.start()
            T.dictionary_threads[threads_index] = thread
            threads.append(thread)
            threads_index = threads_index + 1
        print('----------------------------------------------------------------------------------------------\n')
        for item in C.dictionary_cases:
            print(len(C.dictionary_cases.get(item)), C.dictionary_cases.get(item))
        print('----------------------------------------------------------------------------------------------\n')

    # try:
    #     for th in threads:
    #         th.join_with_exception()
    # except ThreadException:
    #     print('join error')
    #     raise ThreadException(traceback.format_exc())

    # for item in C.dictionary_cases:
    #     print(len(C.dictionary_cases.get(item)), 'after threading', item, C.dictionary_cases.get(item))
