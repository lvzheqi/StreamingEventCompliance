# from streaming_event_compliance import app
# from pm4py.objects.log.importer.xes import factory as xes_importer
# from pm4py.objects.log import transform
# from streaming_event_compliance.services.build_automata import case_thread
# import threading
# from streaming_event_compliance.database import dbtools
# from streaming_event_compliance.objects.variable.globalvar import C, gVars
# from streaming_event_compliance.services import setup
# from streaming_event_compliance.objects.exceptions.exception import ReadFileException, ThreadException, EventException
# from streaming_event_compliance.objects.threadpool.threadpool import ThreadPoolManager
# from multiprocessing import Process
# import traceback
# from console_logging.console import Console
# from streaming_event_compliance.objects.logging.server_logging import ServerLogging
# import sys, time
# console = Console()
# console.setVerbosity(5)
#
# WINDOW_SIZE = app.config['WINDOW_SIZE']
# MAXIMUN_WINDOW_SIZE = app.config['MAXIMUN_WINDOW_SIZE']
# TRAINING_EVENT_LOG_PATH = app.config['TRAINING_EVENT_LOG_PATH']
#
#
# def build_automata():
#     func_name = sys._getframe().f_code.co_name
#     console.info('---------------------Start: Training automata starts!--------------------------------------')
#     ServerLogging().log_info(func_name, "Training automata starts!")
#     try:
#         process_ = Process(target=build_automata_pro())
#         process_.start()
#         process_.join()
#     except ThreadException as ec:
#         raise ec
#     else:
#         autos = gVars.autos
#         ServerLogging().log_info(func_name, "Setting probabilities...")
#         for ws in WINDOW_SIZE:
#             autos[ws].set_probability()
#         dbtools.insert_node_and_connection(autos)
#         ServerLogging().log_info(func_name, "Inserting automata to database")
#         console.info('---------------------End: Everything for training automata is Done!---------------------------')
#         ServerLogging().log_info(func_name, "Training automata ends!")
#     finally:
#         gVars.auto_status = 1
#         setup.clear_build_automata_memorizer()
#         ServerLogging().log_info(func_name, "Cleared automata memorizer")
#
#
# def build_automata_pro():
#     """
#     Description:
#         Reads the training event logger from database.config.TRAINING_EVENT_LOG_PATH and build automata.
#         It generates the probability between SourceNode and SinkNode with different prefix size
#         and stores corresponding information into the database.
#     """
#     thread_pool = ThreadPoolManager(1000)
#     func_name = sys._getframe().f_code.co_name
#     try:
#         trace_log = xes_importer.import_log(TRAINING_EVENT_LOG_PATH)
#         event_log = transform.transform_trace_log_to_event_log(trace_log)
#         event_log.sort()
#         ServerLogging().log_info(func_name, "server", "Training file processed and sorted")
#         ti = time.clock()
#         number_event_process = 0
#         console.secure("[ Preprocessing eventlog time ]", ti)
#         console.secure("[ Number of event  ]", len(event_log))
#     except Exception:
#         ServerLogging().log_error(func_name, "server", "Training file cannot be processed")
#         raise ReadFileException(TRAINING_EVENT_LOG_PATH, traceback.format_exc())
#
#     for one_event in event_log:
#         event = {}
#         number_event_process += 1
#         try:
#             for item in one_event.keys():
#                 if item == 'concept:name':
#                     event['activity'] = one_event.get(item)
#                 elif item == 'case:concept:name':
#                     event['case_id'] = one_event.get(item)
#         except AttributeError:
#             raise EventException(event)
#         else:
#             try:
#                 if event['case_id'] in C.dictionary_cases:
#                     dic = C.dictionary_cases.get(event['case_id'])
#                     iterator = C.event_iterator.get(event['case_id'])
#                     dic[iterator] = event['activity']
#                     thread_pool.add_job(case_thread.run_build, *(event, iterator,))
#                     C.event_iterator[event['case_id']] = iterator + 1
#                 else:
#                     ServerLogging().log_info(func_name, "server", event['case_id'], event['activity'],
#                                              "Creating dictionary_case memorizer")
#                     dic = {}
#                     for i in range(1, MAXIMUN_WINDOW_SIZE):
#                         dic[i] = '*'
#                     dic[MAXIMUN_WINDOW_SIZE] = event['activity']
#                     C.dictionary_cases[event['case_id']] = dic
#                     # lock = threading.RLock()
#                     C.lock_List[event['case_id']] = MAXIMUN_WINDOW_SIZE
#                     thread_pool.add_job(case_thread.run_build, *(event, MAXIMUN_WINDOW_SIZE,))
#                     C.event_iterator[event['case_id']] = MAXIMUN_WINDOW_SIZE + 1
#             except Exception:
#                 console.error('build_auto_pro:' + traceback.format_exc())
#                 ServerLogging().log_error(func_name, "server", "Exception raised while creating dictionary_case")
#                 raise ThreadException(traceback.format_exc())
#     for item in C.dictionary_cases:
#         end_event = {'activity': '~!@#$%', 'case_id': item}
#         iterator = C.event_iterator.get(end_event['case_id'])
#         C.dictionary_cases.get(end_event['case_id'])[iterator] = end_event['activity']
#         thread_pool.add_job(case_thread.run_build, *(end_event, iterator,))
#         C.event_iterator[end_event['case_id']] = iterator + 1
#
#     thread_pool.wait_completion()
