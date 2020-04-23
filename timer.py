import time
from threading import Thread

class Timer(Thread):
    def __init__(self, seconds, callback, *args, **kwargs):
        Thread.__init__(self)

        assert callable(callback)
        self.__callback = callback
        self.__seconds = seconds
        self.__args = args
        self.__kwargs = kwargs

        self.running = False

    def run(self):
        self.running = True
        while self.running:
            Thread(target=self.__callback, args=self.__args, kwargs=self.__kwargs).start()
            time.sleep(self.__seconds)

    def stop(self):  
        self.running = False