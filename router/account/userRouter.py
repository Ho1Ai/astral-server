#libs
from fastapi import APIRouter
from pydantic import BaseModel

#data models
from dataModels.accounts import accountsDataModels as adm # adm is an abbreviation: Accounts Data Models

#services
from service.accounts import accounts as accs_service


router = APIRouter(prefix="/api/accounts")

#class userData(BaseModel):
#    name: str
#    passwd: str
    

@router.post('/create-account')
async def createUser(candidate: adm.AccountCreation):
    test = await accs_service.create_account(candidate)
    #test = 0
    #print(candidate)
    if (test.get('status_code') != 0):
        return {"is_ok": False, "status_code": test}
    else:
        return {"is_ok": True}


@router.post('/user-login')
async def userLogin(candidate: adm.AccountLogin):
    test = await accs_service.sign_in(candidate)
    return test
