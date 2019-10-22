import reader as reader
import sys
import time




def get_logs(logs,str_filter):
    filtered_logs = []
    for index,log in enumerate(logs):
        if str_filter in log:
            filtered_logs.append(logs.pop(index))

    return filtered_logs


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Invalid args - e.x. python3 print_logs.py data')
        sys.exit(0)

    if(sys.argv[1] == 'data'):
        rd = reader.Reader('elink.data.log','name')
    elif(sys.argv[1] == 'info'):
        rd = reader.Reader('elink.info.log','name')

    str_filters = sys.argv[2]
    while True:
        data, total_rows = rd.get_unread_logs()

        if total_rows == 0:
            time.sleep(3)
            continue
        

        for log in get_logs(data,str_filters):
            print(log)


