from db_connect import db_connection as db
#from dotenv import load_dotenv # removed from here, because now I use token service as a separated part of the application
from service.token import token_service as token
from dataModels.accounts import accountsDataModels as adm
import bcrypt


async def create_account(getter_data: adm.AccountCreation) -> int:
    pool = await db.db_connect()
    conn = await pool.acquire()
    #print(getter_data)
    email_test = await conn.fetchrow("select * from astraldb_users where email = $1", getter_data.email);
    nickname_test = await conn.fetchrow("select * from astraldb_users where nickname = $1", getter_data.nickname)
    if (email_test or nickname_test):
        return {'status_code': 5}
    else: 
        hashed_passwd = bcrypt.hashpw(getter_data.passwd.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        test = await conn.execute('insert into astraldb_users (email, nickname, passwd) values ($1, $2, $3) returning id', getter_data.email, getter_data.nickname, hashed_passwd)
        #print("tester goes here", test)
        conn.close()
        if test:
            return {'status_code': 0}


#def getter_data(passwd):
    

async def sign_in(getter_data: adm.AccountLogin):
    pool = await db.db_connect()
    conn = await pool.acquire()
    # there is two tests, because user can sign in using email and nickname
    work_instance = await conn.fetchrow('select * from astraldb_users where email = $1', getter_data.log_name)
    if work_instance:
        await conn.close()
        await pool.close()
        #print(work_instance)
        #passwd_test = test_passwd(getter_data.passwd)
        #passwd_test = type(work_instance.get('passwd'))
        #another_test = type(getter_data.passwd)
        passwd_test = bcrypt.checkpw(getter_data.passwd.encode('utf-8'), work_instance.get('passwd').encode('utf-8'))
        #print(passwd_test, another_test)
        if passwd_test:
            #print('is ok = true')
            token_data={'id':work_instance.get('id'),
                        'email':work_instance.get('email'),
                        'nickname':work_instance.get('nickname')}
            access_jwt = await token.genAccess(token_data)
            refresh_jwt = await token.genRefresh(token_data)
            #conn.close()
            return {"status_code": 0,
                    #'user_id': token_data.get('id'),
                    'access_JWT': access_jwt,
                    'refresh_JWT': refresh_jwt}
        else:
            print("The password is not equal to password, which is hidden in database. It means that there are a user with this email/nickname, but the password is not equal to required")
            #conn.close()
            return {'status_code': 4}
    else:
        work_instance = await conn.fetchrow('select * from astraldb_users where nickname = $1', getter_data.log_name)
        await conn.close()
        await pool.close()
        if work_instance:
            #print(work_instance)
            #passwd_test = test_passwd(getter_data.passwd)
            passwd_test = bcrypt.checkpw(getter_data.passwd.encode('utf-8'), work_instance.get('passwd').encode('utf-8'))
            if (passwd_test):
                #print('is ok = true')
                token_data = {"id": work_instance.get('id'), 
                              "email":work_instance.get('email'), 
                              'nickname': work_instance.get('nickname')}
                access_jwt = await token.genAccess(token_data)
                refresh_jwt = await token.genRefresh(token_data)
                #print("type:", type(access_jwt))
                return {'status_code': 0, 
                        'access_JWT': access_jwt,
                        'refresh_JWT': refresh_jwt}
            else:
                print("The password is not equal to password, which is hidden in database. It means that there are a user with this email/nickname, but the password is not equal to required")
                return {'status_code': 4}
        else:
            #conn.close()
            print("couldn't find such user nor by email, nor by nickname. It means that there are no users with this nickname or email")
            return {'status_code': 4}

    conn.close()




async def fetchAccInfo(raw_id):
    userid = int(raw_id)
    pool = await db.db_connect()
    conn = await pool.acquire()
    test = await conn.fetchrow('select * from astraldb_users where id = $1', userid)
    await conn.close()
    await pool.close()
    return test

