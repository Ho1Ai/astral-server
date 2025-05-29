from dataModels.verify import verificationDataModels as vdm
from db_connect import db_connection as db 

async def can_access_proj(data: vdm.AccessVerification):
    pool = await db.db_connect()
    conn = await pool.acquire()

    func_return = {'is_ok': False,
                   'status_code': 3} # by default it returns an error
    
    project = await conn.fetchrow('select * from astraldb_projects where name = $1', data.proj_name)
    
    print(project)

    #if(user_id in project.get(''))

    await conn.close()
    await pool.close()

    return func_return
