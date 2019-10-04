from threading import Thread
from time import sleep
class test_thread:

    def __init__(self):
        self.direction = 0
        self.step_counter = 0

    def run(self):
        thread_data = Thread(target=self.threaded_function_data)
        thread_data.start()
        sleep(2)
        thread_data.killed = True

    def threaded_function_data(self):
        c = 0
        while c < 100000000000000000:
            print('lala')
            c += 1

if __name__ == '__main__':
    t = test_thread()
    t.run()
