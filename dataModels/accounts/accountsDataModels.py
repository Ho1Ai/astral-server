from pydantic import BaseModel

class AccountLogin__tokenGen(BaseModel):
    id: int
    email: str
    nickname: str

class AccountLogin (BaseModel):
    log_name:str
    passwd: str

class AccountCreation (BaseModel):
    email: str
    nickname: str
    passwd: str



class AccessVerification (BaseModel):
    page_type: str
    name: str
    page_id: int
    jwt_access: str # making some verification tasks
    jwt_refresh: str # if access token has expired


