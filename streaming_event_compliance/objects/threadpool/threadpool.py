from queue import Queue
from threading import Thread
from streaming_event_compliance.objects.exceptions.exception import ThreadException


class ThreadPoolManager:
    def __init__(self, thread_num):
        self.work_queue = Queue()
        self.error_queue = Queue()
        self.thread_num = thread_num
        self.__init_threading_pool(self.thread_num)

    def __init_threading_pool(self, thread_num):
        for i in range(thread_num):
            thread = ThreadManager(self.work_queue, self.error_queue)
            thread.start()

    def wait_completion(self):
        self.work_queue.join()
        if not self.error_queue.empty():
            error_mess = ""
            while not self.error_queue.empty():
                mess = self.error_queue.get().message
                error_mess += mess
            raise ThreadException(error_mess)

    def add_job(self, func, *args):
        self.work_queue.put((func, args))


class ThreadManager(Thread):
    def __init__(self, work_queue, error_queue):
        Thread.__init__(self)
        self.work_queue = work_queue
        self.daemon = True
        self.error_queue = error_queue
        self.response = Queue()

    def run(self):
        while True:
            target, args = self.work_queue.get()
            try:
                self.response.put(target(*args))
            except ThreadException as e:
                self.error_queue.put(e)
            self.work_queue.task_done()
