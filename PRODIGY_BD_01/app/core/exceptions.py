from fastapi import HTTPException

def response_format(code: int, message: str, data=None):
    return {
        "code": code,
        "message": message,
        "data": data
    }

def raise_exception(code: int, message: str, infos=None):
    raise HTTPException(status_code=code, detail=response_format(code, message, infos))
