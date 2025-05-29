from pydantic import BaseModel

class AccessVerification(BaseModel):
    proj_name: str
    user_id: int
