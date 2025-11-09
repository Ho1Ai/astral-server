#created before "to do list migration" (making todos in postgres)
from db_connect import db_connection as db
from dataModels.projects import globalDataModels as proj_models

async def getToDos(project_id: str):
    pool = await db.db_connect()
    conn = await pool.acquire()
    print("id:",project_id)
    
    func_return={'is_ok': True,
                 'status_code': 0}
    
    toDoList = await conn.fetch('select * from astraldb_tdl where target_project_id = $1', project_id)

    if toDoList:
        func_return['return_data']=toDoList
    else:
        func_return['is_ok']=False
        func_return['status_code']=-1

    await conn.close()
    await pool.close()
    return func_return

async def updateToDo(tdid: int, new_state: int, taken_by: int):
    pool = await db.db_connect()
    conn = await pool.acquire()
    
    func_return={"is_ok": True,
                 "status_code": 0}

    try:
        instance_test = await conn.fetchrow('select * from astraldb_tdl')
        if instance_test:
            if new_state == 2:
                update_test = await conn.execute('update astraldb_tdl set state = $1, taken_by = $2 where id = $3', new_state, [taken_by], tdid)
            else:
                update_test = await conn.execute('update astraldb_tdl set state = $1, taken_by = $2 where id = $3', new_state, [], tdid)
    except Exception:
        func_return['is_ok']=False
        func_return['status_code']=-1

    await conn.close()
    await pool.close()
    return func_return

async def appendToDo(proj_id: int, name: str):
    pool = await db.db_connect()
    conn = await pool.acquire()
    
    func_return = {
            'is_ok': True,
            'status_code': 0
            }

    creation_test = await conn.execute('insert into astraldb_tdl (name, state, target_project_id) values ($1,$2,$3)', name, 1, proj_id)

    if creation_test:
        func_return['is_ok']=True
        func_return['status_code']=0
    else:
        func_return['is_ok']=False
        func_return['status_code']=-1

    await conn.close()
    await pool.close()
    
    return func_return





async def getProjID(project_name: str):
    pool = await db.db_connect()
    conn = await pool.acquire()
    
    func_return = {'is_ok': True,
                   'status_code': 0}
    getID = await conn.fetchrow('select * from astraldb_projects where proj_link = $1', project_name)
    if getID:
        func_return['target_id'] = getID.get('id')
    else:
        func_return['is_ok']=False
        func_return['status_code']=-1
    await conn.close()
    await pool.close()
    return func_return
