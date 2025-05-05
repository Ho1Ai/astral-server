from fastapi import APIRouter
from basicfunctions.projects import info
from basicfunctions.accounts import acc_proj_info 

router = APIRouter(prefix="/api/projects", tags=["projects API"])

@router.get('/get-project-info')
async def getProjectInfo(project_name:str):
    to_do_list = await info.getToDo(project_name)
    project_info = await info.getInfo(project_name)
    return {"to_do_list":to_do_list, "project_main_info":project_info}

@router.get('/get-available-projects')
async def getAvailableProjects(username:str):
    #to_do_list = info.getToDo(project_name)
    #project_info = info.getInfo(username)
    #return [{"todo":getToDo, "project info": project_info}] #misprint
    available_projects = await acc_proj_info.getAvailableProjects(username);
    return available_projects
