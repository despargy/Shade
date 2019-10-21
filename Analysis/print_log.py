import reader as reader
import sys
from time import sleep

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Invalid args - e.x. python3 print_logs data')
        sys.exit(0)

    if(sys.argv[1] == 'data'):
        reader = reader.Reader('elink.data.log','name')
    elif(sys.argv[1] == 'info'):
        reader = reader.Reader('elink.info.log','name')

    while True:
        data, total_rows = reader.get_unread_logs()
        for d in data:
            print(d)

