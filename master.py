from elinkmanager import ELinkManager
import threading
from logger import InfoLogger , AdcsLogger


class Master:

    def start(self):
        
        #Init ELinkManager
        self.init_elink()


    def init_elink(self):
        elinkmanager = ELinkManager()
        threading.Thread(target=elinkmanager.start).start()

if __name__ == "__main__":
    Master().start()
