from simulate_stream_event import eventlog, config
from simulate_stream_event.client_logging import ClientLogging
from simulate_stream_event.exception import ReadFileException, ConnectionException, ServerRequestException, ThreadException
from multiprocessing import Process
import sys, traceback
import requests
import os
from console_logging.console import Console
console = Console()
console.setVerbosity(5)


class Client_cls(object):
    """
    Description:
        This class stores details regarding each client.
        The variables initialized are:
        path                :The path of the trace log file
        uuid                :It is the username of the user that has initiated the client
        cc_status           :compliance checked status for the client. It is true if the compliance check
                             is already done for uuid and false otherwise
    """
    def __init__(self, user_name, path=None):
        self.path = path
        self.uuid = user_name
        self.cc_status = False

    def login(self):
        """
        Description:
            This function sends a request to server and checks if the user with uuid is allowed to proceed further.
        :return: True/False :If the uuid is being used by other client this function returns false.
                             If uuid already exists in server database and compliance checking is done then returns true
                             If uuid doesn't exists in server database then returns true
        """
        func_name = sys._getframe().f_code.co_name
        try:
            ClientLogging().log_info(func_name, self.uuid,
                                         'Post request to server:http://127.0.0.1:5000/login?uuid=' + self.uuid)
            r = requests.post('http://127.0.0.1:5000/login?uuid=' + self.uuid)
            if r.status_code != 200:
                raise ServerRequestException('The user can not be created.')
            else:
                if r.text == 'True':
                    self.cc_status = True
                    return True
                elif r.text == 'False':
                    return True
                elif r.text == 'Refuse':
                    return False
        except Exception as e:
            print(e)
            raise ConnectionException

    def run_compliance_checker(self):
        """
        Description:
            This function initiates the reading of trace log and simulates the streaming event.
        """
        func_name = sys._getframe().f_code.co_name
        try:
            ClientLogging().log_info(func_name, self.uuid, 'Calling read_log()')
            event_log = eventlog.read_log(self.uuid, self.path)
            ClientLogging().log_info(func_name, self.uuid, 'Calling simulate_stream_event()')
            eventlog.simulate_stream_event(self.uuid, event_log)
        except ReadFileException:
            raise ReadFileException(self.path)
        except ConnectionException:
            raise ConnectionException
        except ThreadException:
            raise ThreadException(traceback.format_exc())

    def run_show_deviation_pdf(self):
        """
        Description:
           This function requests the server to render pdf with alerts
        """
        func_name = sys._getframe().f_code.co_name
        try:
            ClientLogging().log_info(func_name, self.uuid,
                                     'Post request to http://127.0.0.1:5000/show-deviation-pdf?uuid=' + self.uuid)
            r = requests.post('http://127.0.0.1:5000/show-deviation-pdf?uuid=' + self.uuid)
            if r.status_code != 200:
                raise ConnectionException
            else:
                if r.text != '':
                    ClientLogging().log_info(func_name, self.uuid, 'Compliance checking is done. '
                                                                   'Deviations PDF is available at '
                                                                   'http://127.0.0.1:5000/show-deviation-pdf?uuid=' +
                                             self.uuid)
                    console.info('The compliance checking is already done! You can get the pdf on the following link:')
                    console.info('http://127.0.0.1:5000/show-deviation-pdf?uuid=' + self.uuid)
                else:
                    ClientLogging().log_error(func_name, self.uuid, self.uuid +
                                              ' has not done compliance checking, '
                                              'hence warning generated to first do compliance checking')
                    console.secure("Warning", "You have not done the compliance checking, "
                                              "please do the compliance checking first!.")
        except Exception:
            raise ServerRequestException('PDF can not be created.')


def main(argv):
    """
    Description:
        This function is initially called when the client is run.
        Based on the number of command line arguments provided this function invokes other functions.
    :param argv: This depends on how many command line arguments were provided while initiating the client
                No of arguments sent = 1 then, it is the username
                No of arguments sent = 2 then, it is the username and trace log path
    """
    func_name = sys._getframe().f_code.co_name

    if len(argv) >= 3 or len(argv) < 1:
        console.secure("Warning", 'Please give one or two args, e.g. python client.py user_name (file_path)')
        ClientLogging().log_error(func_name,
                                  'Username or Event logger path arguments were not provided during the run time')
        return

    if len(argv) > 1 and not os.path.exists(argv[1]):
        ClientLogging().log_error(func_name, argv[0], 'The given path is not available!')
        ReadFileException(argv[1]).get_message()
        return

    if len(argv) == 1:
        client = Client_cls(argv[0])
    else:
        client = Client_cls(argv[0], argv[1])

    try:
        if not client.login():
            ClientLogging().log_error(func_name, argv[0], 'The user with the same name is just doing the '
                                                          'compliance checking, please try it later!')
            console.secure("Refuse", 'The user with the same name is just doing the compliance checking, '
                                     'please try it with other name!')
            return
    except ConnectionException as e:
        e.get_message()
        ClientLogging().log_error(func_name, argv[0], 'The server is not available, please try it later!')
        return
    except ServerRequestException as e:
        e.get_message()
        ClientLogging().log_error(func_name, argv[0], 'The user can not be created!')
        return

    while True:
        ClientLogging().log_info(func_name, argv[0], 'The options are displayed')
        print('There are two services:')
        if len(argv) == 2:
            print('\tPress 1, if you want to do the compliance checking')
        print('\tPress 2, if you want to show the deviation pdf')
        print('\tPress 3, if you want to exit')
        if len(argv) == 2:
            console.secure('Note:', 'you can interrupt with CTR_C, once you start to do the compliance checking')
        try:
            services = input()
        except Exception:
            pass

        if services == '1' and len(argv) == 2:
            redo = '1'
            ClientLogging().log_info(func_name, argv[0], 'The user selected option 1')

            if client.cc_status:
                console.secure('Warning', 'You have already done the compliance check! Do you really want to'
                                          ' restart? Or do you want to render the deviation pdf?')
                print('\tIf you want to restart, please press 1 again!')
                print('\tIf you want to skip, please press 2!')
                try:
                    redo = input()
                except Exception:
                    pass

            if redo == '1':
                ClientLogging().log_info(func_name, argv[0], 'The user selected option 1')
                ClientLogging().log_info(func_name, argv[0], 'Calling run_compliance_checker()')
                console.info('---------------start to do compliance checking, please wait-------------------')
                try:
                    p_main = Process(target=client.run_compliance_checker())
                    p_main.start()
                    p_main.join()
                    ClientLogging().log_info(func_name, argv[0], 'compliance checking is completed')
                    console.info('------------------the compliance checking is finishing------------------------')
                    client.cc_status = True
                except ReadFileException as e:
                    e.get_message()
                    ClientLogging().log_error(func_name, argv[0], 'Input file is not readable!')
                    console.secure('Warning',
                                   '------------------the compliance checking is interrupt------------------------')
                except KeyboardInterrupt:
                    client.cc_status = False
                    ClientLogging().log_error(func_name, argv[0], 'Compliance checking is interrupted by user')
                    console.secure('Warning',
                                   '------------------the compliance checking is interrupt------------------------')
                except ThreadException as e:
                    client.cc_status = False
                    e.get_message()
                    ClientLogging().log_error(func_name, argv[0], 'Server is not available')
                    console.error('------------------the compliance checking is interrupt------------------------')

                except ConnectionException as e:
                    client.cc_status = False
                    e.get_message()
                    ClientLogging().log_error(func_name, argv[0], 'Server is not available')
                    console.secure('Warning',
                                   '------------------the compliance checking is interrupt------------------------')
            elif redo == '2':
                ClientLogging().log_info(func_name, argv[0], 'The user selected option 2')
                pass
            else:
                ClientLogging().log_error(func_name, argv[0], 'The users input is invalid')
                console.secure('Warning', 'Your input is invalid, please try again!')
                print('------------------------------------------------------------------------------')

        elif services == '2':
            if not client.cc_status:
                console.secure('Warning',
                               'You have not done the compliance checking. Please do the compliance checking ahead!')
                print('------------------------------------------------------------------------------')
            else:
                ClientLogging().log_info(func_name, argv[0], 'The user selected option 2')
                ClientLogging().log_info(func_name, argv[0], 'Calling run_show_deviation_pdf() ')
                console.info('-----------------start to render deviation pdf, please wait-------------------')
                try:
                    client.run_show_deviation_pdf()
                except ConnectionException as e:
                    e.get_message()
                    ClientLogging().log_error(func_name, argv[0],
                                              'Error: The server is not available, please try it later!')
                except ServerRequestException as e:
                    e.get_message()
                    ClientLogging().log_error(func_name, argv[0], 'pdf can not be created')
                print('------------------------------------------------------------------------------')

        elif services == '3':
            ClientLogging().log_info(func_name, argv[0], 'The user selected option 3')
            ClientLogging().log_info(func_name, argv[0], 'Exiting...')
            console.info('Bye!')
            return
        else:
            ClientLogging().log_error(func_name, argv[0], 'The users input is invalid')
            console.secure('Warning', 'Your input is invalid, please try again!')
            print('------------------------------------------------------------------------------')


if __name__ == '__main__':
    main(sys.argv[1:])

