from elinkmanager import ELinkManager
import threading


class Master:

    def start(self):
        elinkmanager = ELinkManager()
        threading.Thread(target=elinkmanager.start).start()

if __name__ == "__main__":
    Master().start()
