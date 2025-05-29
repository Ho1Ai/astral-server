from db_connect import db_connection as db
from pydantic import BaseModel
from dataModels.projects import globalDataModels
from service.token import token_service
from service.accounts import accounts

static_content__to_do = [
            {
                "id": 1,
                "name": "Make an Application",
                "state": 1,
                }, {
                "id": 2,
                "name": "Build a Project",
                "state": 1,
                }, {
                "id": 3,
                "name": "Deploy a Project",
                "state": 1
                }
        ]


class ToDoData (BaseModel):
    id: int
    name: str
    state: int
#added before globalDataModels.py, so it is still here. Never mind
            
        






default_projects = [
        {
            "id": 1,
            "name":"Project Astral",
            "description": "Project Astral - application for developers and their projects. Our main purpose is to create an application which can be used for free. You can make forks: it is open source. You can find everything (except backend) on GitHub. You can share your ideas on our Discord server. Together we can make good projects! We (especially me, Ho1Ai) wish you all the best. Good luck, y'all!",
            "authorTeam": "Collapse Team",
            "authorsList": ["Ho1Ai"],
            "projectLinksArray": [{
                "name": "GitHub",
                "link": "https://github.com/Ho1Ai/project-astral"
                }],
            "proj_link": "project-astral"
            }
        ]

async def getToDo(project_name:str):
   return static_content__to_do

#----------PROJECT DATA----------

async def getInfo(proj_name_by_link: str):
    pool = await db.db_connect()
    conn = await pool.acquire()

    func_return = {'is_ok': True,
                   'status_code': 0}
    proj_data_raw = await conn.fetchrow('select * from astraldb_projects where proj_link = $1', proj_name_by_link)
    array_num = 0
    print(proj_data_raw)
    for index in proj_data_raw['authors_list']:
        proj_data_raw['authors_list'][array_num] = await accounts.fetchAccInfo(index)
        array_num += 1
    print(proj_data_raw)
    #except Exception:
    #   print('exception')
    func_return['project_data']=proj_data_raw

    await conn.close()
    await pool.close()

    return func_return




async def getAvailableProjects(username: str):
    #print(default_projects)
    
    return default_projects
    

async def createProject(new_data: globalDataModels.ProjectModel):
    pool = await db.db_connect()
    conn = await pool.acquire()
    check_name_availability = await conn.fetchrow('select * from astraldb_projects where name = $1', new_data.name)
    if(check_name_availability):
        await conn.close()
        await pool.close()
        #print('can not create')
        return {'is_ok': False}
    get_token_data = token_service.getTokenData(new_data.authorsList[0], 'refresh')
    new_project_info = {
            #"id":len(default_projects)+1,
        "name": new_data.name,
        "description": new_data.description,
        "authorTeam": new_data.authorTeam,
        "authorsList": [str(get_token_data.get('data').get('id'))],
        "projectLinksArray": [{
            "name":"GitHub",
            "link":"https://github.com/Ho1Ai/project-astral"
            }],
        "proj_link": new_data.link
        }

    appendTest = await conn.execute('insert into astraldb_projects (name, description, author_team, authors_list, proj_link) values($1,$2,$3,$4,$5)', 
                                    new_project_info['name'], 
                                    new_project_info['description'],
                                    new_project_info['authorTeam'],
                                    new_project_info['authorsList'],
                                    #new_project_info['projectLinksArray'],
                                    new_project_info['proj_link'])

    await conn.close()
    await pool.close()
    return True
    


#----------INNER PROJECT----------

async def updateToDosInfo(todo_updated: ToDoData):
    static_content__to_do[todo_updated.id-1]['state'] = todo_updated.state
    return {"is_ok": True, "new_TDL": static_content__to_do}

async def appendNewToDo(name: str, state: int):
    static_content__to_do.append({
            "id": len(static_content__to_do)+1,
            "name":name,
            "state":state,
        })
    return {"is_ok": True, "new_TDL": static_content__to_do}

