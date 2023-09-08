import tkinter as tk

def notify(message="Hello World!", image=None, timeout=5000, command=None):
    def on_click(event=None):
        if command: command()
        popup.destroy()
    popup = tk.Toplevel(bg='black', relief=tk.RAISED, bd=3)
    popup.overrideredirect(True)
    popup.geometry("200x50-10-50")
    if isinstance(image, str):
        image = tk.PhotoImage(file=image)
        popup.ref = image
    if image:
        lbl = tk.Label(popup, image=image)
        lbl.pack(side=tk.LEFT)
        lbl.bind('<1>', on_click)
    lbl = tk.Message(popup, bg='black', fg='white', border=2, text=message)
    lbl.pack()
    lbl.bind('<1>', on_click)
    if timeout: popup.after(timeout, popup.destroy)

### demo:

def callback():
    notify("hi I'm a popup", image="\OFF.gif", command=lambda: print('clicked'))

root= tk.Tk()
root.geometry('200x200')
btn = tk.Button(root, text="Click me!", command=notify)
btn.pack(expand=True)
btn = tk.Button(root, text="incl image demo", command=callback)
btn.pack(expand=True)
root.mainloop()