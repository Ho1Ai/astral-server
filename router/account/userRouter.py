from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class userData(BaseModel):
    name: str
    passwd: str
    

@router.get('/userLogin')
async def userLogin():
    return 0
