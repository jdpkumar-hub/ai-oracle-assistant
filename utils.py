import re
import bcrypt

def is_strong_password(password):
    return (
        len(password) >= 6 and
        re.search("[A-Z]", password) and
        re.search("[0-9]", password)
    )

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())