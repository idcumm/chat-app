import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from tkinter import *


def encrypt(raw, event=None):
    raw = pad(raw.encode(), 16)
    cipher = AES.new(KEY, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw)).decode("utf-8", "ignore")


def decrypt(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(KEY, AES.MODE_ECB)
    return unpad(cipher.decrypt(enc), 16).decode("utf-8", "ignore")


def encrypt_(event=None):
    raw = data_entry.get()
    text = encrypt(raw)
    text_label.insert(END, text)


def decrypt_(event=None):
    enc = data_entry.get()
    text = encrypt(enc)
    text_label.insert(END, text)


root = Tk()
data = StringVar()
data_entry = Entry(root, textvariable=data)
key = StringVar()
key_entry = Entry(root, textvariable=key, show='*')
encrypt_button = Button(root, command=encrypt_, text='encrypt')
decrypt_button = Button(root, command=decrypt_, text='decrypt')
data_label = Label(root, text='Escriba el texto que desea encriptar')
key_label = Label(root, text="\nEscriba la contraseña que desea usar")
text_label = Text(root, state="disabled", width=50, height=10)
data_label.grid(column=1, row=0)
data_entry.grid(column=1, row=1)
key_label.grid(column=1, row=2)
key_entry.grid(column=1, row=3)
encrypt_button.grid(column=0, row=4, padx=50, pady=50)
decrypt_button.grid(column=2, row=4, padx=50, pady=50)
text_label.grid(column=1, row=5, padx=50, pady=50)


KEY = hashlib.sha256(key_entry.get().encode()).digest()
root.mainloop()
