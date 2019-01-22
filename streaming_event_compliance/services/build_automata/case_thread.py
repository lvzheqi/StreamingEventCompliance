# from streaming_event_compliance import app
# from streaming_event_compliance.objects.variable.globalvar import gVars, CL, T, C
# from streaming_event_compliance.objects.automata import automata
# from streaming_event_compliance.objects.exceptions.exception import ThreadException
# from streaming_event_compliance.objects.logging.server_logging import ServerLogging
# import threading
# import traceback
# import sys
#
# check_executing_order = {}
# WINDOW_SIZE = app.config['WINDOW_SIZE']
# MAXIMUN_WINDOW_SIZE = app.config['MAXIMUN_WINDOW_SIZE']
#
#
# def run_build(event, iterator):
#     func_name = sys._getframe().f_code.co_name
#     ServerLogging().log_info(func_name, str(threading.current_thread()))
#     try:
#         print("before while", C.lock_List.get(event['case_id']), iterator)
#         while C.lock_List.get(event['case_id']) != iterator:
#             print("while")
#             ServerLogging().log_info(func_name, "server", event['case_id'],
#                                      event['activity'], "waiting for iterator: ", iterator, " equal to ", C.lock_List.get(event['case_id']))
#             pass
#         windows_memory = list(C.dictionary_cases.get(event['case_id']).values())[0: MAXIMUN_WINDOW_SIZE + 1]
#         assert windows_memory[MAXIMUN_WINDOW_SIZE] == event['activity'], 'window_memory caculated wrongly!'
#         ServerLogging().log_info(func_name, "server", event['case_id'],
#                                  event['activity'],
#                                  "Calculating connections")
#         calculate_connection_for_different_prefix_automata(windows_memory)
#         C.dictionary_cases.get(event['case_id']).pop(iterator - MAXIMUN_WINDOW_SIZE + 1)
#         assert len(windows_memory) == MAXIMUN_WINDOW_SIZE - 1, 'pop wrongly!'
#
#         global check_executing_order
#         '''--------For Testing: Before releasing lock, which thread used it will be stored-------'''
#         if check_executing_order.get(event['case_id']):
#             check_executing_order.get(event['case_id']).append(event['activity'])
#         else:
#             check_executing_order[event['case_id']] = []
#             check_executing_order[event['case_id']].append(event['activity'])
#         '''--------For Testing: Before releasing lock, which thread used it will be stored-------'''
#         # C.lock_List.get(event['case_id']).release()
#         C.lock_List[event['case_id']] = iterator + 1
#         ServerLogging().log_info(func_name, "server", event['case_id'],
#                                  event['activity'], "has been processed, and for this case the ",
#                                  iterator + 1, " -th event can be processed next!")
#     except Exception:
#             ServerLogging().log_error(func_name, "server",  event['case_id'], event['activity'],
#                                      "Error with Caselock")
#             raise ThreadException(traceback.format_exc())
#
#
# def calculate_connection_for_different_prefix_automata(windowsMemory):
#     """
#     Description:
#         This function will calculate the connections with different size for the windowsMemory.
#
#     :param windowsMemory: :`list` a list of activities from the same case_id of current event(another event),
#                          size is maximum_window_size, and the current event is in the last position of the
#                          windowsMemory (i.e. event == windowsMemory[maximum_window_size]).
#     """
#     for ws in WINDOW_SIZE:
#         source_node = ','.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws: MAXIMUN_WINDOW_SIZE])
#         sink_node = ','.join(windowsMemory[MAXIMUN_WINDOW_SIZE - ws + 1: MAXIMUN_WINDOW_SIZE + 1])
#         if CL.lock_list.get((source_node, sink_node)):
#             if CL.lock_list.get((source_node, sink_node)).acquire():
#                 try:
#                     if windowsMemory[MAXIMUN_WINDOW_SIZE] == '~!@#$%' and source_node.find('*') == -1:
#                         gVars.autos.get(ws).update_automata(automata.Connection(source_node, '~!@#$%', 0))
#                     elif source_node.find('*') == -1:
#                         gVars.autos.get(ws).update_automata(automata.Connection(source_node, sink_node, 1))
#                     elif source_node.find('*') != -1 and sink_node.find('*') == -1:
#                         gVars.autos.get(ws).update_automata(automata.Connection('NONE', sink_node, 1))
#                     CL.lock_list.get((source_node, sink_node)).release()
#                 except Exception as ec:
#                     raise ec
#         else:
#             lock = threading.RLock()
#             CL.lock_list[source_node, sink_node] = lock
#             if CL.lock_list.get((source_node, sink_node)).acquire():
#                 try:
#                     if windowsMemory[MAXIMUN_WINDOW_SIZE] == '~!@#$%' and source_node.find('*') == -1:
#                         gVars.autos.get(ws).update_automata(automata.Connection(source_node, '~!@#$%', 0))
#                     elif source_node.find('*') == -1:
#                         gVars.autos.get(ws).update_automata(automata.Connection(source_node, sink_node, 1))
#                     CL.lock_list.get((source_node, sink_node)).release()
#                 except Exception as ec:
#                     raise ec
