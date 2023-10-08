from customtkinter import *

set_appearance_mode("dark")
set_default_color_theme("dark-blue")

root = CTk()
root.geometry("500x300")


def login():
    print("Test")


frame = CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = CTkLabel(master=frame, text="Login system", font=("Roboto", 24))
label.pack()

entry1 = CTkEntry(master=frame, placeholder_text="username")
entry1.pack(pady=12, padx=10)

entry2 = CTkEntry(master=frame, placeholder_text="password", show="*")
entry2.pack(pady=12, padx=10)

button = CTkButton(master=frame, text="login", command=login)
button.pack(pady=12, padx=10)

checkbox = CTkCheckBox(master=frame, text="Remember me")
checkbox.pack(pady=12, padx=10)

root.mainloop()
