from Crypto.Cipher import AES

def encrypt(inpt):
    outpt = cipher.encrypt(inpt)
    return outpt

def decrypt(inpt):
    outpt = inpt
    return outpt


KEY = b'C&F)H@McQfTjWnZr'
cipher = AES.new(KEY, AES.MODE_EAX)
nonce = cipher.nonce

inpt = 'hola'.encode()

outpt = encrypt(inpt)

print(outpt)