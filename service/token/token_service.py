from jose import jwt
from dotenv import dotenv_values
from datetime import datetime, timedelta

#from db_connect import db_connection as db

from dataModels.accounts import accountsDataModels as adm

# sorry for this big sausage. I just wrote it in 3 runs because somewhere I didn't need some of these variables and then I didn't place dotenv_values('.env') in separated variable

cfg_token = {"access_secret": dotenv_values(".env").get('JWT_ACCESS_SECRET'), 
             "refresh_secret": dotenv_values('.env').get('JWT_REFRESH_SECRET'), 
             "access_expire_mins": dotenv_values('.env').get('ACCESS_EXPIRE_TIME_MINS'), 
             "refresh_expire_days": dotenv_values('.env').get('REFRESH_EXPIRE_TIME_DAYS'), 
             "algorithm":dotenv_values('.env').get("TOKEN_ALGORITHM")}





async def genAccess(data: adm.AccountLogin__tokenGen):
    token_data = {"id":data.get('id'),
                  "email":data.get('email'),
                  "username":data.get('username'),
                  "expire_on": (datetime.utcnow()+timedelta(minutes = int(cfg_token.get('access_expire_mins')))).isoformat()}
    jwt_access = jwt.encode(token_data, cfg_token.get('access_secret'), cfg_token.get("algorithm"))
    return jwt_access






async def genRefresh(data: adm.AccountLogin__tokenGen):
    token_data = {'id':data.get('id'),
                  'email':data.get('email'),
                  'nickname':data.get('nickname'),
                  'expire_on': (datetime.utcnow()+timedelta(days=int(cfg_token.get('refresh_expire_days')))).isoformat()}
    jwt_refresh = jwt.encode(token_data, cfg_token.get('refresh_secret'), cfg_token.get('algorithm'))
    return jwt_refresh






async def getTokenInnerData__EMAIL(access_token:str, refresh_token: str): # and also refresh it
    #print(access_token)
    jwt_input = jwt.decode(access_token, cfg_token.get('access_secret'), algorithms=cfg_token.get('algorithm'))
    response={'status_code': 0}
    if(datetime.utcnow()>datetime.fromisoformat(jwt_input.get('expire_on'))):
        print('old')
        jwt_input = jwt.decode(refresh_token, cfg_token.get('refresh_secret'), algorithms=cfg_token.get('algorithm'))
        if(datetime.utcnow()>datetime.fromisoformat(jwt_input.get('expire_on'))):
            print('old refresh')
            return {'status_code': 8}
        else:
            data_constructor = {'id': jwt_input.get('id'),
                                'nickname': jwt_input.get('nickname'),
                                'email': jwt_input.get('email')}
            #print(data_constructor)
            new_access_jwt = await genAccess(data_constructor)
            new_refresh_jwt = await genRefresh(data_constructor)
            response['access_JWT'] = new_access_jwt
            response['refresh_JWT'] = new_refresh_jwt
            response['email'] = data_constructor.get('email')
            return response

    else:
        data_constructor = {'id': jwt_input.get('id'),
                            'nickname': jwt_input.get('nickname'),
                            'email': jwt_input.get('email')}
        new_access_jwt = await genAccess(data_constructor)
        response['access_JWT'] = new_access_jwt
        response['email'] = data_constructor.get('email')
        return response
    
    data_constructor = {'id': jwt_input.get('id'),
                        'nickname':jwt_input.get('nickname'),
                        'email': jwt_input.get('email')}
    return response #well, it will just response any way
            
