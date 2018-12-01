from simulate_stream_event import eventlog, client_logging
from simulate_stream_event.exception import ReadFileException, ConnectionException
from multiprocessing import Process
import sys
import requests
import os


class Client_cls(object):

    def __init__(self, user_name, path=None):
        self.dictionary_threads = {}
        self.path = path
        self.uuid = user_name

    def run_compliance_checker(self):
        func_name = sys._getframe().f_code.co_name
        try:
            client_logging.log_info(func_name=func_name, username=self.uuid,
                                          message="Calling read_log()")
            event_log = eventlog.read_log(self.uuid, self.path)
        except ReadFileException:
            client_logging.log_error(func_name=func_name, username=self.uuid,
                                          message="Exception raised while reading file")
            raise ReadFileException(self.path)
        client_logging.log_info(func_name=func_name, username=self.uuid,
                                      message="Calling simulate_stream_event()")
        eventlog.simulate_stream_event(self.uuid, event_log)

    def run_show_deviation_pdf(self):
        func_name = sys._getframe().f_code.co_name
        try:
            client_logging.log_info(func_name=func_name, username=self.uuid,
                                          message="Post request to http://127.0.0.1:5000/show-deviation-pdf?uuid="
                                                  + self.uuid)
            r = requests.post('http://127.0.0.1:5000/show-deviation-pdf?uuid=' + self.uuid)
            if r.status_code != 200:
                client_logging.log_error(func_name=func_name,
                                              username=self.uuid,
                                              message="pdf can not be created")
                print('Error: pdf can not be created')
            else:
                if r.text: # TODO: according to the status of server
                    client_logging.log_info(func_name=func_name,
                                                  username=self.uuid,
                                                  message="Compliance checking is done. Deviations PDF is available at"
                                                          "http://127.0.0.1:5000/show-deviation-pdf?uuid=" + self.uuid)

                    print('The compliance checking is already done! You can get the pdf on the following link:')
                    print('http://127.0.0.1:5000/show-deviation-pdf?uuid=' + self.uuid)
                else:
                    client_logging.log_error(func_name=func_name,
                                                  username=self.uuid,
                                                  message=self.uuid + " hasn't done compliance checking, hence warning "
                                                                      "generated to first do compliance checking")
                    print('Warning: You have not do the compliance checking, '
                          'please do the compliance checking at first!')
        except Exception:
            client_logging.log_error(func_name=func_name,
                                          username=self.uuid,
                                          message="Error: The server is not available, please try it later!")
            print(ConnectionException.message)
            return


def main(argv):
    func_name = sys._getframe().f_code.co_name

    if len(argv) > 3 or len(argv) < 1:
        print('Please give one or two args, e.g. python client.py user_name (file_path)')
        client_logging.log_error(func_name=func_name,
                                      message="Username or Event logger path arguments "
                                              "were not provided during the run time")
        return
    try:

        client_logging.log_info(func_name=func_name, username=argv[0],
                                      message="Post request to server:http://127.0.0.1:5000/login?uuid="+argv[0])
        r = requests.post('http://127.0.0.1:5000/login?uuid=' + argv[0])
        if r.status_code != 200:
            print('Error: The user can not be created!')
            client_logging.log_error(func_name=func_name, username=argv[0],
                                          message="The user can not be created!")
            return

    except requests.exceptions.RequestException:
        # client_logging.log_error(func_name=func_name, username=argv[0],
        #                              message="The server is not available, please try it later!")
        print(ConnectionException.message)
        return

    if len(argv) > 1 and not os.path.exists(argv[1]):
        client_logging.log_error(func_name=func_name, username=argv[0],
                                      message="The given path is not available!")

        print(ReadFileException.message)
        return

    # client1 = Client('client1', 'Example.xes')
    if len(argv) == 1:
        client1 = Client_cls(argv[0])
    else:
        client1 = Client_cls(argv[0], argv[1])

    while(True):
        client_logging.log_info(func_name=func_name, username=argv[0],
                                      message="The options are displayed")
        print('There are two services:')
        if len(argv) == 2:
            print('\tPress 1, if you want to do the compliance checking')
        print('\tPress 2, if you want to show the deviation pdf')
        print('\tPress 3, if you want to exit')
        if len(argv) == 2:
            print('Note: you can interrupt with CTR_C, once you start to do the compliance checking')
        try:
            services = input()
        except Exception: #UnicodeDecodeError #TODO:maybe give some extra Exception
            pass

        if services == '1':
            client_logging.log_info(func_name=func_name, username=argv[0],
                                          message="The user selected option 1")

            client_logging.log_info(func_name=func_name,
                                          username=argv[0],
                                          message="Calling run_compliance_checker()")
            print('---------------start to do compliance checking, please wait-------------------')
            try:
                p_main = Process(target=client1.run_compliance_checker())
                p_main.start()
                p_main.join()
                client_logging.log_info(func_name=func_name,
                                              username=argv[0],
                                              message="compliance checking is completed")
                print('------------------the compliance checking is finishing------------------------')
            except ReadFileException:
                client_logging.log_error(func_name=func_name,
                                              username=argv[0],
                                              message="Input file is not readable!")
                print(ReadFileException.message)
                print('------------------the compliance checking is interrupt------------------------')
            except KeyboardInterrupt: #TODO: jingjinghuo: this exception will never happen, using control+z it will directly exit.
                client_logging.log_error(func_name=func_name,
                                              username=argv[0],
                                              message="Compliance checking is interrupted by user")
                print('------------------the compliance checking is interrupt------------------------')
        elif services == '2':
            client_logging.log_info(func_name=func_name, username=argv[0],
                                          message="The user selected option 2")
            print('-----------------start to render deviation pdf, please wait-------------------')
            client_logging.log_info(func_name=func_name, username=argv[0],
                                          message="Calling  run_show_deviation_pdf() ")
            client1.run_show_deviation_pdf()
            print('------------------------------------------------------------------------------')
        elif services == '3':
            client_logging.log_info(func_name=func_name, username=argv[0],
                                          message="The user selected option 3")
            print('Bye!')
            client_logging.log_info(func_name=func_name, username=argv[0],
                                          message="Exiting...")
            return
        else:
            client_logging.log_error(func_name=func_name, username=argv[0],
                                          message="The users input is invalid")
            print('Your input is invalid, please try again!')
            print('------------------------------------------------------------------------------')


if __name__ == '__main__':
    main(sys.argv[1:])

