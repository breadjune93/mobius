from fastapi import Request

def get_token_from_header(request: Request) -> bool:
    return None

def get_token_from_cookie(request: Request) -> bool:
    return None

def validate_token(token: str) -> bool:
    try:
        payload = decode_token(token)
        print(f"verify_access_token: {payload}")
        if payload.get("type") != "access":
            return None
        return payload.get("sub")
    except Exception:
        return None


def create_auth_header(token: str) -> bool:
    return None

def set_token_cookie(token: str) -> bool:
    return None

def delete_token_cookie(token: str) -> bool:
    return None