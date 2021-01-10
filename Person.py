import threading
import _thread
from time import sleep


class Person:
    TIMEOUT = 5*60


    def __init__(self,name):
        self.name = name
        self.is_active=False
        self.thread = None
        self.timeout=self.TIMEOUT

    def refresh(self):
        print(f'Refresh of {self.name}')
        self.timeout=self.TIMEOUT

    def __thread_update(self):
        self.is_active=True
        while(self.timeout>0):
            sleep(1)
            self.timeout-=1
        self.is_active=False

    def start(self):
        print(f"Start of {self.name}")
        self.timeout=self.TIMEOUT
        self.thread = _thread.start_new_thread( self.__thread_update, ())

