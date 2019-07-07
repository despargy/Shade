from elinkmanager import ELinkManager
import threading


class Master:

    def start(self):
        elinkmanager = ELinkManager()
        threading.Thread(target=elinkmanager.start).start()

        x = input("Enter to Continue")

        elinkmanager.send_photo('FSM-ADC.png')


if __name__ == "__main__":
    Master().start()
