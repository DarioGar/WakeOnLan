import re
import bcrypt

def checkMAC(MAC):
    """
    Checks if the format of the given MAC is correct
    """
    print(MAC)
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", MAC.lower()):
        return MAC
    else:
        return False

def get_hashed_password(plain_text_password):
    """
    Hash a password for the first time
    (Using bcrypt, the salt is saved into the hash itself)
    """
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    """
    Check hashed password. Using bcrypt, the salt is saved into the hash itself
    """
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)
    