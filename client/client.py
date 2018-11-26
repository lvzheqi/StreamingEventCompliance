from simulate_stream_event import eventlog
from simulate_stream_event.exception import ReadFileException
from multiprocessing import Process
import sys
import requests
import os


class Client(object):
    def __init__(self, user_name, path):
        self.dictionary_threads = {}
        self.path = path
        self.uuid = user_name

    def run_compliance_checker(self):
        try:
            event_log = eventlog.read_log(self.path)
        except Exception:
            raise ReadFileException
        eventlog.simulate_stream_event(self.uuid, event_log)

    def run_show_deviation_pdf(self):
        try:
            r = requests.post('http://127.0.0.1:5000/show-deviation-pdf?uuid=' + self.uuid)
            if r.status_code != 200:
                print('Error: pdf can not be created')
            else:
                if r.text: # TODO: according to the status of server
                    print('The compliance checking is already done! You can get the pdf on the following link:')
                    print('http://127.0.0.1:5000/show-deviation-pdf?uuid=' + self.uuid)
                else:
                    print('Warning: You have not do the compliance checking, '
                          'please do the compliance checking at first!')
        except Exception:
            print('Error: The server is not available, please try it later!')
            return


def main(argv):
    if len(argv) < 2 or len(argv) > 3:
        print('Please give two args, e.g. python client.py user_name file_path')
        return
    try:
        r = requests.post('http://127.0.0.1:5000/login?uuid=' + argv[0])
        if r.status_code != 200:
            print('Error: The user can not be created!')
            return
    except Exception:
        print('Error: The server is not available, please try it later!')
        return
    if not os.path.exists(argv[1]):
        print('Error: The given path is not available!')
        return

    # client1 = Client('client1', 'Example.xes')
    client1 = Client(argv[0], argv[1])

    while(True):
        print('There are two services:')
        print('\tPress 1, if you want to do the compliance checking')
        print('\tPress 2, if you want to show the deviation pdf')
        print('\tPress 3, if you want to exit')
        print('Note: you can interrupt with CTR_C, once you start to do the compliance checking')
        try:
            services = input()
        except Exception: #UnicodeDecodeError #TODO:maybe give some extra Exception
            pass

        if services == '1':
            print('---------------start to do compliance checking, please wait-------------------')
            try:
                p_main = Process(target=client1.run_compliance_checker())
                p_main.start()
                p_main.join()
                print('------------------the compliance checking is finishing------------------------')
            except ReadFileException:
                print('Error: The input file is not readable!')
                print('------------------the compliance checking is interrupt------------------------')
            except KeyboardInterrupt:
                print('------------------the compliance checking is interrupt------------------------')
        elif services == '2':
            print('-----------------start to render deviation pdf, please wait-------------------')
            client1.run_show_deviation_pdf()
            print('------------------------------------------------------------------------------')
        elif services == '3':
            print('Bye!')
            return
        else:
            print('Your input is invalid, please try again!')
            print('------------------------------------------------------------------------------')


if __name__ == '__main__':
    main(sys.argv[1:])

