import os
import hashlib
from typing import Tuple

def hash_password(password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
    """Hashes a password using PBKDF2 HMAC with SHA-256."""
    """Returns a tuple of (hash, salt)."""
    if salt is None:
        salt = os.urandom(32)
    
    # Use PBKDF2 HMAC with SHA-256
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000 # Number of iterations
    )
    return pwd_hash, salt

def verify_password(password: str, stored_hash: bytes, salt: bytes) -> bool:
    """Verifies a password against a stored hash and salt."""
    re_hashed, _ = hash_password(password, salt)
    return re_hashed == stored_hash
