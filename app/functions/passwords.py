import bcrypt

def hash_password(passw):
    return bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())

def verify_password(provided_password, stored_hashed_password):
    if isinstance(stored_hashed_password, memoryview):
        stored_hashed_password = stored_hashed_password.tobytes()
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hashed_password)
