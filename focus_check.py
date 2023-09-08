from tkinter import *
from time import sleep
from win10toast import ToastNotifier

def focus_check():
    if not root.focus_displayof():
        Label(root, text="False").pack()
        n.show_toast("Chat app",
                    "You got a new message",
                    duration = 10,
                    threaded = True)
    else:
        Label(root, text="True").pack()

root = Tk()
n = ToastNotifier()
button = Button(root, text='Check for focus', command=focus_check)
button.pack()
focus_check()
root.mainloop()


# ...

# def send_notification(*args):
#     """triggers when the window loses focus."""
#     ...

# root = tk.Tk()
# root.bind('<FocusOut>', send_notification)
# ...




# def send_notification(*args):
#     """triggers when the window loses focus."""
#     if not focus_check.get():
#         ...

# root = tk.Tk()

# focus_check = tk.BooleanVar()
# root.bind('<FocusIn>', lambda _: focus_check.set(True))
# root.bind('<FocusOut>', lambda _: focus_check.set(False))