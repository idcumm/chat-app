from win10toast import ToastNotifier


def not1():
    n = ToastNotifier()

    n.show_toast("Chat app",
                 "You got a new message",
                 duration=10,
                 threaded=True)


def not2():
    n = ToastNotifier()

    n.show_toast("GEEKSFORGEEKS", "Notification body", duration=20,
                 icon_path="https://media.geeksforgeeks.org/wp-content/uploads/geeks.ico")


not1()
