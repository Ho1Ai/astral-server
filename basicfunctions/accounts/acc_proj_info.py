from db_connect import db_connection as db 

#default_answer = [{"name": "Project Astral", "project_link": "project-astral"}]

async def getAvailableProjects(nickname: str):
    pool = await db.db_connect()
    conn = await pool.acquire()
    
    func_return = []

    data = await conn.fetch('select * from astraldb_projects where $1 = any(authors_list)', nickname)

    func_return = data
    #return func_return

    await conn.close()
    await pool.close()

    return func_return

    #if(username == "Ho1Ai"):
    #    return default_answer 
