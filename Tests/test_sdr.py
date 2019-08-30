import subprocess
from time import sleep
import os
import signal

def test1():
    p = subprocess.Popen("python3 sdr_code.py", shell=True)
    print("Process ID of subprocess %s" % p.pid)
    sleep(4)
    #os.system("kill -9 {}".format(p.pid))
    subprocess.Popen("kill -9 {}".format(p.pid), shell=True).communicate()
    #p.kill()
    #os.killpg(os.getpgid(p.pid), signal.SIGTERM)  # Send the signal to all the process groups
    # Send SIGTER (on Linux)
    #p.terminate()
    # Wait for process to terminate
    #returncode = p.wait()
    #print("Returncode of subprocess: %s" % returncode)

def test2():

    p = subprocess.Popen("python3 sdr_code.py")
    sleep(4)
    #os.killpg(os.getpgid(p.pid), signal.SIGTERM)  # Send the signal to all the process groups
    p.terminate()
    #print(p.communicate())

if __name__ == '__main__':
    test1()