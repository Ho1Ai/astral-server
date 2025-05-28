#libs
from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

#data models
from dataModels.accounts import accountsDataModels as adm # adm is an abbreviation: Accounts Data Models

#services
from service.accounts import accounts as accs_service

from basicfunctions.accounts import acc_proj_public as accs_public_funcs
from basicfunctions.accounts import acc_proj_info

#temporary
from service.token import token_service

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
                new_res['X-JWT-Access'] = tester.get('access_JWT')
            if(tester.get('refresh_JWT')):
                new_res['X-JWT-Refresh'] = tester.get('refresh_JWT')
            #print(token)
            return new_res #top 1 dumbest way of tokens refresh, lol. But it was easy to understand
            
            #new_res = {
            #        'nickname': tester.get('nickname'),
            #        'description': tester.get('description')
            #        }
            #print(tester, '\n', new_res)
        else:
            return {'status_code': 9}
        print('Я люблю острую шаурму')




#----------ACCOUNT PROJECTS----------
#btw, I'm not sure, where should I place this stuff, so... It will stay here at the moment. In the future I'll place it in a better place
@router.get('/project-list')
async def getProjectList(request: Request):
    request_body_data={'exist': True}
    request_body_data['access_jwt'] = request.headers['X-JWT-Access']
    request_body_data['refresh_jwt'] = request.headers['X-JWT-Refresh']

    response_body = {'status_code': 0} # since now and at least until I do this stuff I'm gonna use response_body instead of smth like new_res or this sort of dumb names
    
    check_jwt_status = token_service.checkJWTStatus(request_body_data['access_jwt'], request_body_data['refresh_jwt'])
    
    if(check_jwt_status.get('is_ok')==True):
        #refreshing tokens. It is easier to place this stuff here
        token_data = token_service.getTokenData(request_body_data['refresh_jwt'],'refresh').get('data')
        
        response_body['access_jwt']=await token_service.genAccess(token_data)
        if(check_jwt_status.get('is_access_token_dead')==True):
            response_body['refresh_jwt']=await token_service.genRefresh(token_data) # I don't know why "await", never ask me, I don't remember what I did here
        print(response_body)
        print(token_data)

        response_body['project_list']=await acc_proj_info.getAvailableProjects(token_data.get('nickname'))
        #print(response_body['project_list'])
    else:
        response_body['status_code']=check_jwt_status.get('status_code')
    return response_body
