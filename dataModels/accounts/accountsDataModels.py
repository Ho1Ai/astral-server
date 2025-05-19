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
