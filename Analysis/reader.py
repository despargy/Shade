from file_read_backwards import FileReadBackwards

class Reader():

    def __init__(self,filename,name, read_time , directory='../Logs/'):
        self.name = name
        self.READ_TIME = read_time
        self.directory = directory
        self.file_name = filename
        self.last_index = 0

    def get_id(self,log):
        try:
            return int(log.split(',')[0])
        except:
            pass

    def get_unread_logs(self):
        last_index = -1
        unread_logs = []
        with FileReadBackwards(self.directory + self.file_name, encoding="utf-8") as log_file:
            for line in log_file:
                line_index = self.get_id(line)
                if last_index == -1 :
                    last_index = line_index

                if line_index == self.last_index:
                    break

                unread_logs.insert(0,line)
            self.last_index = last_index
        return unread_logs, len(unread_logs)