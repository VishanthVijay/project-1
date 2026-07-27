import bcrypt


def hash_password(plain_password: str) -> str:
    """
    Hashes a plain text password using bcrypt with automatic salt generation.

    Never store plain text passwords in a database!
    """
    # Truncate password to 72 bytes as per bcrypt specification
    password_bytes = plain_password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a stored bcrypt hash.
    Returns True if the password matches, False otherwise.
    """
    password_bytes = plain_password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)
