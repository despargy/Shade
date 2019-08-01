from file_read_backwards import FileReadBackwards
from abc import ABC, abstractmethod
import time , threading

class Reader(ABC):

    def __init__(self,filename):
        self.file_name = filename
        self.last_index = 1
        self.total_lost_logs = 0
        self.total_logs = 0
        self.lost_log_rate = 0


    def get_unread_logs(self):
        last_line = -1
        unread_logs = []
        with FileReadBackwards(self.file_name, encoding="utf-8") as BigFile:
            for line in BigFile:
                line_id = int(line.split(',')[0])
                if last_line == -1 :
                    last_line = line_id


                if line_id == self.last_index:
                    break

                unread_logs.insert(0,line)
            self.last_index = last_line
        return unread_logs



    def calc_lost_log_rate(self):
        logs = self.get_unread_logs()
        #print(logs)
        total_log_num = len(logs)
        if total_log_num == 0 : return
        prev_log = logs[0]
        for log in logs:
            if log == prev_log: continue

            prev_log_id = int(prev_log.split(',')[0])
            curr_log_id = int(log.split(',')[0])

            if prev_log_id != (curr_log_id -1):
                lost_logs = curr_log_id - prev_log_id
                self.total_lost_logs += lost_logs

            prev_log = log
        self.total_logs = curr_log_id
        self.lost_log_rate = round((self.total_lost_logs / self.total_logs) * 100 , 2 )

    def get_lost_log_rate(self):
        print('Lost logs rate for {file_name} is {lost_log_rate}% or {total_lost_logs} / {total_logs}'.format(
                                                file_name = self.file_name,
                                                lost_log_rate=self.lost_log_rate,
                                                total_lost_logs=self.total_lost_logs,
                                                total_logs=self.total_logs))

def read_error_logs():
    reader = Reader('elink.info.log')
    while True:
        logs = reader.get_unread_logs()
        for log in logs:
            if 'error' in log.lower():
                print(log)
        time.sleep(2)

if __name__ == '__main__':
    #read_error_logs()
    #info_statistics()

    readers = [Reader('elink.info.log'), Reader('elink.data.log') ]
    #readers = [Reader('elink.info.log') ]

    while True:
        thread_list = []
        for reader in readers:
            t = threading.Thread(target=reader.calc_lost_log_rate)
            t.start()
            thread_list.append(t)

        for thread in thread_list:
            thread.join()

        for reader in readers:
            reader.get_lost_log_rate()
            pass
        time.sleep(30)
