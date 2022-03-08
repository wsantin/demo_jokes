import bcrypt
import hmac

def createPassword(email, password):
    password_to_encrypt = email.strip()+password.strip()
    password_to_encrypt = password_to_encrypt.encode("utf-8")

    salt = bcrypt.gensalt(rounds=12, prefix="2a".encode("utf-8"))
    hashed = bcrypt.hashpw(password_to_encrypt, salt)

    return hashed.decode("utf-8")

def comparePassword(password_hash, email, password):
    password_hash = password_hash.encode("utf-8")
    password_to_encrypt = email.strip()+password.strip()
    password_to_encrypt = password_to_encrypt.encode("utf-8")

    verify = hmac.compare_digest(bcrypt.hashpw(password_to_encrypt, password_hash), password_hash)
    if verify:
        return True
    else:
        return False
