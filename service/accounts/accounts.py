from db_connect import db_connection as db
#from dotenv import load_dotenv # removed from here, because now I use token service as a separated part of the application
from service.token import token_service as token
from dataModels.accounts import accountsDataModels as adm
import bcrypt


async def create_account(getter_data: adm.AccountCreation) -> int:
    pool = await db.db_connect()
    conn = await pool.acquire()
    print(getter_data)
    email_test = await conn.fetchrow("select * from astraldb_users where email = $1", getter_data.email);
    nickname_test = await conn.fetchrow("select * from astraldb_users where nickname = $1", getter_data.nickname)
    if (email_test or nickname_test):
        return 5
    else: 
        hashed_passwd = bcrypt.hashpw(getter_data.passwd.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        test = await conn.execute('insert into astraldb_users (email, nickname, passwd) values ($1, $2, $3) returning id', getter_data.email, getter_data.nickname, hashed_passwd)
        print("tester goes here", test)
        if test:
            return 0


#def getter_data(passwd):
    

async def sign_in(getter_data: adm.AccountLogin):
    pool = await db.db_connect()
    conn = await pool.acquire()
    # there is two tests, because user can sign in using email and nickname
    work_instance = await conn.fetchrow('select * from astraldb_users where email = $1', getter_data.log_name)
    if work_instance:
        print(work_instance)
        #passwd_test = test_passwd(getter_data.passwd)
        passwd_test = bcrypt.checkpw(getter_data.passwd.encode('utf-8'), work_instance.get('passwd'))
        if passwd_test:
            return 0
        else:
            print("Password is not equal to password, which is hidden in database. It means that there are a user with this email/nickname, but password is not equal to required")
            return 4
    else:
        work_instance = await conn.fetchrow('select * from astraldb_users where nickname = $1', gettee_data.log_name)
        if work_instance:
            print(work_instance)
            #passwd_test = test_passwd(getter_data.passwd)
            passwd_test = bcrypt.checkpw(getter_data.passwd, work_instance.get('passwd'))
        else:
            print("couldn't find such user nor by email, nor by nickname. It means that there are no users with this nickname or email")
            return 4
