import secrets

def generate_session_token():
    return secrets.token_hex(32)

def generate_session_token_user(user_id):
    pass