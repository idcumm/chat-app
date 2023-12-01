import hashlib
import base64
import uuid

password = "test_password"
salt = uuid.uuid4().bytes


t_sha = hashlib.sha512()
t_sha.update(password + salt)
hashed_password = base64.urlsafe_b64encode(t_sha.digest())
