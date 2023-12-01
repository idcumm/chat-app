import hashlib, uuid

password = input().encode()
salt = uuid.uuid4().hex.encode()
hashed_password = hashlib.sha512(password + salt).hexdigest()
print(hashed_password)
