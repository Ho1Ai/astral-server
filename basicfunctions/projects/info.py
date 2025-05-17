from db_connect import db_projects
from pydantic import BaseModel
from dataModels.projects import globalDataModels

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
            "authorTeam": "Morlix Team",
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

async def getInfo(project_name: str):
    return default_projects

async def getAvailableProjects(username: str):
    #print(default_projects)
    return default_projects
    

async def createProject(new_data: globalDataModels.ProjectModel):
    default_projects.append({
        "id":len(default_projects)+1,
        "name": new_data.name,
        "description": new_data.description,
        "authorTeam": new_data.authorTeam,
        "authorList": ['Ho1Ai'],
        "projectLinksArray": [{
            "name":"GitHub",
            "link":"https://github.com/Ho1Ai/project-astral"
            }],
        "proj_link": new_data.link
        })
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

