#libs
from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

#data models
from dataModels.accounts import accountsDataModels as adm # adm is an abbreviation: Accounts Data Models

#services
from service.accounts import accounts as accs_service

from basicfunctions.accounts import acc_proj_public as accs_public_funcs

router = APIRouter(prefix="/api/accounts")

#class userData(BaseModel):
#    name: str
#    passwd: str
    

#----------SIGN IN AND SIGN UP LOGIC----------
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
    #print(candidate) #debug line
    test = await accs_service.sign_in(candidate)
    return test



#----------ACCOUNTS PUBLIC DATA LOGIC----------
#@router.get('/get-user-info_by-id')
#async def getUserData_id(id: int):
#    pass

@router.get('/get-user-info')
async def getUserData_JWT(request: Request, response: Response):
    rtype=request.query_params.get('rtype')
    if(rtype=='id'):
        onSearch_infoGetter=(int(request.query_params.get('id')))
        tester = await accs_public_funcs.getUserPageDataById(onSearch_infoGetter)
        #print('Я люблю шаурму с сыром')
        if(tester.get('status_code') == 0):
            #print('ok\n', tester)
            return(tester)
        else:
            return {'status_code': 9}

    if(rtype=='jwt'):
        onHeader_infoGetter={'access': request.headers.get('X-JWT-Access'),
                             'refresh': request.headers.get('X-JWT-Refresh')}
        tester = await accs_public_funcs.getUserPageDataByJWT(onHeader_infoGetter.get('access'), onHeader_infoGetter.get('refresh'))
        if tester.get('status_code') == 0:
            new_res = {'status_code': 0,
                       'nickname': tester.get('nickname'),
                       'description': tester.get('description')}
            if (tester.get('access_JWT')):
                new_res['x-jwt-access'] = tester.get('access_JWT')
            if(tester.get('refresh_JWT')):
                new_res['x-jwt-refresh'] = tester.get('refresh_JWT')
            return new_res #top 1 dumbest way of tokens refresh, lol. But it was easy to understand
            
            #new_res = {
            #        'nickname': tester.get('nickname'),
            #        'description': tester.get('description')
            #        }
            #print(tester, '\n', new_res)
        else:
            return {'status_code': 9}
        print('Я люблю острую шаурму')

