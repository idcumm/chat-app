import bcrypt
from os import system


def get_hashed_password(password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return (bcrypt.hashpw(password.encode(), bcrypt.gensalt())).decode()


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password)


# hash_ = get_hashed_password(input())
# print(hash_)
# print(check_password(input(), hash_))

system("cls")

while True:
    print()
    num = int(input("Choose an option: "))
    if num == 1:
        hash_ = get_hashed_password(input("Input: "))
        print(hash_)
    elif num == 2:
        print(check_password(input("Input: "), hash_))
    elif num == 3:
        print(check_password(input("Input: "), input("Input: ").encode()))
