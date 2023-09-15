import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from tkinter import *


def encrypt(raw):
    KEY = hashlib.sha256(enc_key_entry.get().encode()).digest()
    raw = pad(raw.encode(), 16)
    cipher = AES.new(KEY, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw)).decode("utf-8", "ignore")


def decrypt(enc):
    KEY = hashlib.sha256(dec_key_entry.get().encode()).digest()
    enc = base64.b64decode(enc)
    cipher = AES.new(KEY, AES.MODE_ECB)
    return unpad(cipher.decrypt(enc), 16).decode("utf-8", "ignore")


def encrypt_(event=None):
    x = enc_data_entry.get()
    enc_data.set('')
    text = encrypt(x)
    print(text)
    text_label.configure(state="normal")
    text_label.insert(END, f'+ {text}\n')
    text_label.configure(state="disabled")
    text_label.yview(END)


def decrypt_(event=None):
    x = dec_data_entry.get()
    dec_data.set('')
    text = decrypt(x)
    print(text)
    text_label.configure(state="normal")
    text_label.insert(END, f'- {text}\n')
    text_label.configure(state="disabled")
    text_label.yview(END)


root = Tk()
enc_data = StringVar()
dec_data = StringVar()
enc_data_entry = Entry(root, textvariable=enc_data)
enc_data_entry.bind("<Return>", encrypt_)
enc_data_entry.focus()
dec_data_entry = Entry(root, textvariable=dec_data)
dec_data_entry.bind("<Return>", decrypt_)
enc_key = StringVar()
enc_key.set("1234")
dec_key = StringVar()
dec_key.set("1234")
enc_key_entry = Entry(root, textvariable=enc_key, show='*')
enc_key_entry.bind("<Return>", encrypt_)
dec_key_entry = Entry(root, textvariable=dec_key, show='*')
dec_key_entry.bind("<Return>", decrypt_)
enc_button = Button(root, command=encrypt_, text='encrypt')
dec_button = Button(root, command=decrypt_, text='decrypt')
enc_label = Label(root, text='Escriba el texto que desea cifrar')
dec_label = Label(root, text='Escriba el texto que desea descifrar')
enc_key_label = Label(
    root, text="\nEscriba la contraseña que desea usar para cifrar el mensaje")
dec_key_label = Label(
    root, text="\nEscriba la contraseña que desea usar para descifrar el mensaje")
text_label = Text(root, state="disabled", width=50, height=10)
enc_label.grid(column=0, row=0)
dec_label.grid(column=1, row=0)
enc_data_entry.grid(column=0, row=1)
dec_data_entry.grid(column=1, row=1)
enc_key_label.grid(column=0, row=2)
dec_key_label.grid(column=1, row=2)
enc_key_entry.grid(column=0, row=3)
dec_key_entry.grid(column=1, row=3)
enc_button.grid(column=0, row=4, padx=50, pady=50)
dec_button.grid(column=1, row=4, padx=50, pady=50)
text_label.grid(column=1, row=5, padx=50, pady=50)

if __name__ == "__main__":
    root.mainloop()
