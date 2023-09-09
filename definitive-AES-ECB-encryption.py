import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

# AES ECB mode without IV

data = input('input: ')
# Must Be 16 char for AES128
key = 'Hola como estas macarra a mi me gusta matar a niños pequeños perque me lo paso mejor'
key = hashlib.sha256(key.encode()).digest()


def encrypt(raw):
    raw = pad(raw.encode(), 16)
    cipher = AES.new(key, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw)).decode("utf-8", "ignore")


def decrypt(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(enc), 16).decode("utf-8", "ignore")


try:
    encrypted = encrypt(data)
    print('Encrypted: ', encrypted)
except ValueError:
    print(ValueError)


try:
    decrypted = decrypt(data)
    print('Decrypted: ', decrypted)
except ValueError:
    print('Decrypted: Impossible to decrypt message')
