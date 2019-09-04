from multiprocessing import Process
import time, os, threading

def start_tx(name):
    os.system('python3 {name}'.format(name=name))

def kill_tx(name):
    temp_filename = 'tmp_pid'
    os.system('ps -ef | grep {name} > {temp_filename}'.format(name=name,temp_filename=temp_filename))
    with open(temp_filename, 'r') as tmp:
        lines = tmp.readlines()
        for line in lines:
            compoments = line.split()
            curr_name = compoments[-1]
            curr_command = compoments[-2]
            
            if curr_name == name and curr_command == 'python3':
                pid = compoments[1]
                os.system('kill -9 {pid}'.format(pid=pid))
                os.system('rm -f {temp_filename}'.format(temp_filename=temp_filename))

if __name__ == '__main__':
    name = 'sdr_code.py'
    threading.Thread(target=start_tx, args=(name,)).start()
    time.sleep(3)
    kill_tx(name)
