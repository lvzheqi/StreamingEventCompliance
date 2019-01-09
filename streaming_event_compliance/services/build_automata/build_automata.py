from streaming_event_compliance import app
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log import transform
from streaming_event_compliance.services.build_automata import case_thread
import threading
from streaming_event_compliance.database import dbtools
from streaming_event_compliance.objects.variable.globalvar import T, C, gVars
from streaming_event_compliance.services import setup
from streaming_event_compliance.objects.exceptions.exception import ReadFileException, ThreadException, EventException
from multiprocessing import Process
import traceback
from console_logging.console import Console
from streaming_event_compliance.objects.logging.server_logging import ServerLogging
import sys
console = Console()
console.setVerbosity(5)

threads = []
threads_index = 0
WINDOW_SIZE = app.config['WINDOW_SIZE']
MAXIMUN_WINDOW_SIZE = app.config['MAXIMUN_WINDOW_SIZE']
TRAINING_EVENT_LOG_PATH = app.config['TRAINING_EVENT_LOG_PATH']


def build_automata():
    func_name = sys._getframe().f_code.co_name
    console.info('---------------------Start: Traininging automata starts!--------------------------------------')
    ServerLogging().log_info(func_name, "Traininging automata starts!")
    try:
        process_ = Process(target=build_automata_pro())
        process_.start()
        process_.join()
    except ThreadException as ec:
        raise ec
    else:
        autos = gVars.autos
        ServerLogging().log_info(func_name, "Setting probabilities...")
        for ws in WINDOW_SIZE:
            autos[ws].set_probability()
        dbtools.insert_node_and_connection(autos)
        ServerLogging().log_info(func_name, "Inserting automata to database")
        console.info('---------------------End: Everything for training automata is Done!---------------------------')
        ServerLogging().log_info(func_name, "Training automata ends!")
    finally:
        gVars.auto_status = 1
        setup.clear_build_automata_memorizer()
        ServerLogging().log_info(func_name, "Cleared automata memorizer")


def build_automata_pro():
    '''
        Reads the training event logger from database.config.TRAINING_EVENT_LOG_PATH and build automata.
        It generates the probability between SourceNode and SinkNode with different prefix size
        and stores corresponding information into the database.
    :return:
    '''
    func_name = sys._getframe().f_code.co_name
    try:
        trace_log = xes_importer.import_log(TRAINING_EVENT_LOG_PATH)
        event_log = transform.transform_trace_log_to_event_log(trace_log)
        event_log.sort()
        ServerLogging().log_info(func_name, "server", "Training file processed and sorted")
    except Exception:
        ServerLogging().log_error(func_name, "server", "Training file cannot be processed")
        raise ReadFileException(TRAINING_EVENT_LOG_PATH)

    global threads_index, threads
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
                if event['case_id'] in C.dictionary_cases:
                    C.dictionary_cases.get(event['case_id']).append(event['activity'])
                    thread = case_thread.CaseThreadForTraining(event, threads_index, T, C)
                    thread.start()
                    T.dictionary_threads[threads_index] = thread
                    threads.append(thread)
                    threads_index = threads_index + 1
                else:
                    ServerLogging().log_info(func_name, "server", event['case_id'], event['activity'], "Creating dictionary_case memorizer")
                    C.dictionary_cases[event['case_id']] = ['*' for i in range(0, MAXIMUN_WINDOW_SIZE)]
                    C.dictionary_cases[event['case_id']].append(event['activity'])
                    lock = threading.RLock()
                    C.lock_List[event['case_id']] = lock
                    thread = case_thread.CaseThreadForTraining(event, threads_index, T, C)
                    thread.start()
                    T.dictionary_threads[threads_index] = thread
                    threads.append(thread)
                    threads_index = threads_index + 1
            except Exception:
                console.error('build_auto_pro:' + traceback.format_exc())
                ServerLogging().log_error(func_name, "server", "Exception raised while creating dictionary_case")
                raise ThreadException(traceback.format_exc())

    for item in C.dictionary_cases:
        end_event = {'activity': '~!@#$%', 'case_id': item}
        C.dictionary_cases.get(end_event['case_id']).append(end_event['activity'])
        thread = case_thread.CaseThreadForTraining(end_event, threads_index, T, C)
        thread.start()
        T.dictionary_threads[threads_index] = thread
        threads.append(thread)
        threads_index = threads_index + 1
    for th in threads:
        try:
            th.join_with_exception()
        except ThreadException:
            ServerLogging().log_error(func_name, "server", "Joining is not successful")
            raise ThreadException(traceback.format_exc())
