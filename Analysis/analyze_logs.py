from file_read_backwards import FileReadBackwards
from abc import ABC, abstractmethod
import time , threading
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

class Reader(ABC):

    def __init__(self,filename,name, read_time):
        self.name = name
        self.READ_TIME = read_time
        self.file_name = filename
        self.last_index = 0
        self.total_lost_logs = 0
        self.total_logs = 0
        self.lost_log_rate = 0
        self.last_line_read = ''
        self.total_inactivity_time = 0
        self.error_logs = []
        self.is_not_successively = lambda prev_id , id : prev_id != (id - 1)
        self.has_big_delay = lambda : self.total_inactivity_time >= (2* self.READ_TIME)


    def get_unread_logs(self):
        last_index = -1
        unread_logs = []
        with FileReadBackwards(self.file_name, encoding="utf-8") as log_file:
            for line in log_file:
                line_index = self.get_id(line)
                if last_index == -1 :
                    last_index = line_index

                if line_index == self.last_index:
                    break

                unread_logs.insert(0,line)
            self.last_index = last_index
        return unread_logs

    def get_id(self,log):
        try:
            return int(log.split(',')[0])
        except:
            pass

    def calc_statistics(self):
        logs = self.get_unread_logs()
        self.calc_lost_log_rate(logs)
        self.read_error_logs(logs)
        

    def read_error_logs(self,logs):
        self.error_logs = filter(lambda log: 'error' in log.lower(), logs)

    def calc_lost_log_rate(self,logs):
        total_log_num = len(logs)

        #no logs.
        if total_log_num == 0 :
            self.total_inactivity_time += self.READ_TIME
            return

        #set inactivity time to 0 because there is new logs.
        self.total_inactivity_time = 0

        prev_log = logs[0]
        first_line = True
        for log in logs:

            curr_log_id = self.get_id(log)

            if first_line:
                try:
                    last_line_id = self.get_id(self.last_line_read)
                    #if log were written two times , skip
                    if last_line_id == curr_log_id: continue
                    
                    #if is not successively, count lost logs
                    if self.is_not_successively(last_line_id,curr_log_id):
                        lost_logs = curr_log_id - last_line_id - 1
                        self.total_lost_logs += lost_logs
                except:
                    pass

                first_line = False
                continue

            prev_log_id = self.get_id(prev_log)
            
            #if log were written two times , skip
            if prev_log_id == curr_log_id: continue

            #if is not successively, count lost logs     
            if self.is_not_successively(prev_log_id,curr_log_id):
                lost_logs = curr_log_id - prev_log_id - 1
                self.total_lost_logs += lost_logs

            prev_log = log

        self.last_line_read = logs[total_log_num-1]
        self.total_logs = curr_log_id
        self.lost_log_rate = round((self.total_lost_logs / self.total_logs) * 100 , 2 )

    def print_lost_log_rate(self):
        print('Lost logs rate for {file_name} is {lost_log_rate}% or {total_lost_logs} / {total_logs}'.format(
                                                file_name = self.file_name,
                                                lost_log_rate=self.lost_log_rate,
                                                total_lost_logs=self.total_lost_logs,
                                                total_logs=self.total_logs))


    def print_innactivity_time(self):
        inactivity_minutes = int(self.total_inactivity_time / 60)
        inactivity_seconds = self.total_inactivity_time % 60
        print('No logs from {name} for {minutes}.{seconds} minutes'.format(
             name=self.name,
             minutes=inactivity_minutes,
             seconds=inactivity_seconds
        ))

    def print_error_logs(self):
        print(*self.error_logs, sep='\n')




def plot_heat():
        style.use('ggplot')
    
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        lim = 0
        def animate(i):
            graph_data = open('info.log','r').read()
            lines = graph_data.split('\n')
            xs = []
            ys = []
            for line in lines:
                if len(line) > 1:
                    data = line.split()[3]
                    x,y = data.split(',')
                    xs.append(float(x))
                    ys.append(float(y))
            

            ax1.clear()
            x = float(x)
            y = float(y)
            ax1.set_xlim([max(0,x-100), x])
            color = 'b'
            if y > 50:
                color = 'r'
            ax1.plot(xs,ys, color=color)

        
        ani = animation.FuncAnimation(fig, animate , interval=1000)
        plt.show()

def print_prompt():
    print("""
          [+] Run Reader program with one argument.
          [+] The argument indicates the seconds
          [+] between statistics reports
          [+] e.g python read_logs.py 10
          """)

def get_args():
    try:
        return int(sys.argv[1])
    except:
        print_prompt()
        sys.exit(0)

def start_readers(readers):
    thread_list = []
    for reader in readers:
        t = threading.Thread(target=reader.calc_statistics)
        t.start()
        thread_list.append(t)

    for thread in thread_list:
        thread.join()

def create_readers(seconds):
    info_reader = Reader('elink.info.log','Info Logs' , seconds)
    data_reader = Reader('elink.data.log','Data Logs', seconds)
    return [info_reader, data_reader]

def print_statistics(readers):
    current_time = time.strftime("%H:%M:%S", time.gmtime())
    print('\n\n######## Print statistics at {current_time} ########\n\n'.format(current_time=current_time))
    for reader in readers:
        print('--------- {name} ---------'.format(name=reader.name))
        reader.print_lost_log_rate()
        if reader.has_big_delay():
            reader.print_innactivity_time()

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print_prompt()
        sys.exit(0)

    if(sys.argv[1] == 'heat'):
        plot_heat()
        sys.exit(0)
    seconds = get_args()
    readers = create_readers(seconds)

    while True:
        start_readers(readers)
        print_statistics(readers)
        time.sleep(seconds)