from db_connect import db_connection as db
from service.token import token_service as token

async def getUserPageDataById(id: int):
    pool = await db.db_connect()
    conn = await pool.acquire()
    try:
        db_getter = await conn.fetchrow('select * from astraldb_users where id = $1', id);
    #print(db_getter)
        await conn.close()
        await pool.close()
        interested_in_data = {
            "status_code": 0,
            "nickname": db_getter.get('nickname'),
            "description": db_getter.get('description')
            }
        return interested_in_data
    except Exception:
        await conn.close()
        await pool.close()
        #print(Exception)
        return {"status_code": 9}
    #pass
    #print('пирожок')

async def getUserPageDataByJWT(access: str, refresh: str):
    pool = await db.db_connect()
    conn = await pool.acquire()
    tester = await token.getTokenInnerData__EMAIL(access, refresh)
    #print(tester)
    #print(token.getTokenData(access, 'access'))
    try:
        db_getter = await conn.fetchrow('select * from astraldb_users where email = $1', tester.get('email'))
        await conn.close()
        await pool.close()
        #print(db_getter)
        #print(db_getter)
    
        final_data = {'status_code': 0,
                      'nickname': db_getter.get('nickname'),
                      'description': db_getter.get('description')}
        if(tester.get('access_JWT')):
            final_data['access_JWT'] = tester.get('access_JWT')
        if(tester.get('refresh_JWT')):
            final_data['refresh_JWT'] = tester.get('refresh_JWT')
        #print(final_data)
        return final_data
    except Exception:
        await conn.close()
        await pool.close()
        print('exception!')
        return {'status_code': 9}
