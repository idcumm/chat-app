from Crypto.Cipher import AES


def enc(inpt):
    global cipher
    cipher = AES.new(KEY, AES.MODE_EAX)
    outpt = cipher.encrypt(inpt)
    return outpt


def dec(inpt):
    global cipher
    nonce = cipher.nonce
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    outpt = cipher.decrypt(inpt)
    return outpt


KEY = b"C&F)H@McQfTjWnZr"  # 16 bytes long


inpt = "hola com estas".encode()
encrypted_text = enc(inpt)
print(encrypted_text)
decrypted_text = dec(encrypted_text)
print(decrypted_text)
