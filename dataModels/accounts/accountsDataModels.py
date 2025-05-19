from pydantic import BaseModel

class AccountLogin (BaseModel):
    log_name:str
    passwd: str

class AccountCreation (BaseModel):
    email: str
    nickname: str
    passwd: str
