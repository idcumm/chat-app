from tkinter import *
from win10toast import ToastNotifier
from time import sleep
from threading import Thread


def focus_out(*args):
    global focus
    focus = False
    print('focus set to false')


def focus_in(*args):
    global focus
    focus = True
    print('focus set to true')


def thread():
    global focus
    sleep(2)
    while True:
        if focus == False:
            print('notification sent')
            n.show_toast("Chat app",
                         "1: Hola com estas yo estic molt be i tu com estas yo estic molt be i tu com estas yo estic mot be ",
                         duration=10,
                         threaded=True,)
        else:
            print('no notification')
        for i in reversed(range(5)):
            print(i+1)
            sleep(1)


root = Tk()
focus = bool()
n = ToastNotifier()
root.bind('<FocusOut>', focus_out)
root.bind('<FocusIn>', focus_in)
thread = Thread(target=thread)
thread.start()

root.mainloop()
