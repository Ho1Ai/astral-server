from fastapi import APIRouter
from basicfunctions.projects import info
from basicfunctions.accounts import acc_proj_info 

from dataModels.projects import globalDataModels

router = APIRouter(prefix="/api/projects", tags=["projects API"])



#----------PROJECT CREATOR AND OTHERS----------#
@router.post('/create-new-project')
async def createNewProject(new_project_data: globalDataModels.ProjectModel):
    new_list = await info.getAvailableProjects('default')
    return new_list






#----------PROJECT DATA, TODOS AND PROJECT LIST RECEIVER----------#
@router.get('/get-project-info')
async def getProjectInfo(project_name:str):
    to_do_list = await info.getToDo(project_name)
    project_info= await info.getInfo(project_name)
    return {"to_do_list":to_do_list, "project_main_info":project_info}

@router.get('/get-available-projects')
async def getAvailableProjects(username:str):
    #to_do_list = info.getToDo(project_name)
    #project_info = info.getInfo(username)
    #return [{"todo":getToDo, "project info": project_info}] #misprint
    available_projects = await acc_proj_info.getAvailableProjects(username);
    return available_projects

@router.put('/update-todo')
async def updateToDoState(updateData: globalDataModels.ToDoModel):
    updater = await info.updateToDosInfo(updateData)
    
    return {"ok": updater.get("is_ok"), "new_TDL": updater.get("new_TDL")};
    #is_ok = True if id == 25 else False
    #is_ok = True
    #return {'status': 201} if is_ok else {'status': 422}

@router.post('/append-todo')
async def appendToDo(new_to_do: globalDataModels.ToDoAppender):
    appender = await info.appendNewToDo(new_to_do.name, new_to_do.state)
    #print(new_to_do.name)
    return {"ok": appender.get("is_ok"), "new_TDL": appender.get("new_TDL")}
