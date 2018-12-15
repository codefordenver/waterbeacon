from sys import stdout
from time import sleep
from threading import Thread


'''
Simple spinner for animating CLI loading using a separate thread
All credit to Victor Moyseenko (https://goo.gl/L998MQ)
'''


class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\':
                yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay):
            self.delay = delay

    def spinner_task(self):
        while self.busy:
            stdout.write(next(self.spinner_generator))
            stdout.flush()
            sleep(self.delay)
            stdout.write('\b')
            stdout.flush()

    def start(self):
        self.busy = True
        Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        sleep(self.delay)
