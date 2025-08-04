from fastapi import APIRouter, Request
from basicfunctions.projects import info
from basicfunctions.accounts import acc_proj_info 
#import time

from dataModels.projects import globalDataModels

from service.projects import projects
from service.token import token_service as token

router = APIRouter(prefix="/api/projects", tags=["projects API"])



#----------PROJECT CREATOR AND OTHERS----------#
@router.post('/create-new-project')
async def createNewProject(new_project_data: globalDataModels.ProjectModel):
    #print(new_project_data.link, "nan?")
    is_added = await info.createProject(new_project_data)
    if is_added:
        new_list = await info.getAvailableProjects('default')
        return new_list






#----------PROJECT DATA, TODOS AND PROJECT LIST RECEIVER----------#
@router.get('/get-project-info')
async def getProjectInfo(project_name:str):
    to_do_list = await getToDoList(project_name)
    project_info= await info.getInfo(project_name)
    func_return = {'is_ok': True,
                   'status_code':0}
    if(to_do_list.get('is_ok')):
        func_return['to_do_list']=to_do_list.get('to_do_list')
    else:
        func_return['to_do_list']=[]    
    #return {"to_do_list":to_do_list, "project_main_info":project_info}
    func_return['project_main_info'] = project_info
    #print(func_return)
    return func_return




@router.get('/get-available-projects')
async def getAvailableProjects(userid:str):
    #to_do_list = info.getToDo(project_name)
    #project_info = info.getInfo(username)
    #return [{"todo":getToDo, "project info": project_info}] #misprint
    
    available_projects = await info.getAvailableProjects(userid);
    return available_projects

@router.get('/get-to-do-list')
async def getToDoList(project_name: str):
    #print(project_name)
    
    func_return = {'is_ok': True,
                   'status_code': 0}

    project_id_getter = await projects.getProjID(project_name)
    if(project_id_getter.get('is_ok')==True and project_id_getter.get('target_id')):
        #print(project_id_getter.get('target_id'))
        response_constructor = await projects.getToDos(project_id_getter.get('target_id'))
        if response_constructor.get('is_ok') == True:
            func_return['to_do_list'] = response_constructor.get('return_data')
        else:
            func_return['is_ok']=False
            func_return['status_code']=response_constructor.get('status_code')
    else:
        func_return['is_ok'] = False
        func_return['status_code']=projectIdGetter.get('status_code')
    #print('QWPA', func_return)
    return func_return




@router.put('/update-todo')
async def updateToDoState(request: Request, updateData: globalDataModels.ToDoModel):
	func_return = {'is_ok': True,
                   'status_code': 0} 
	checkJWT = token.checkJWTStatus(request.headers.get('X-JWT-Access'), request.headers.get('X-JWT-Refresh'))
    #time.sleep(1)
	if(checkJWT.get('is_ok')==True):
		token_data = token.getTokenData(request.headers.get('X-JWT-Refresh'), 'refresh')
        #time.sleep(1)
        #print("/////   token data   /////  ",token_data)
        #if(request.get(''))
		#print(request)
		#print(updateData.state)
		getter_id = await info.getProjId(updateData.id)
		#print(token_data)
		#print(getter_id, "asdf")
		func_return['access_JWT'] = await token.genAccess(token_data.get('data'))
		if(checkJWT.get('is_access_token_dead')):
			func_return['refresh_JWT'] = await token.genRefresh(token_data.get('data'))
		updater = await info.updateToDosInfo(updateData.id, updateData.state, token_data.get('data').get('id'), getter_id)
		func_return['new_tdl'] = updater
        #time.sleep(1)
        #print(func_return)
    
    #time.sleep(1)
    #print(func_return)
    #time.sleep(1)
	return func_return
	#print(request.headers, '\n--------\n',updateData)
    
    #if(getUnameData.get('access_JWT')):
    #    func_return[''] # what the f*** it was supposed to do?!
    #return {"ok": updater.get("is_ok"), "new_TDL": updater.get("new_TDL")};
    #is_ok = True if id == 25 else False
    #is_ok = True
    #return {'status': 201} if is_ok else {'status': 422}

@router.post('/append-todo')
async def appendToDo(new_to_do: globalDataModels.ToDoAppender):
    #appender = await info.appendNewToDo(new_to_do.name, new_to_do.state)
    #print(new_to_do.name)
    func_return = {'is_ok': True,
                   'status_code': 0}


    append_id_getter = await projects.getProjID(new_to_do.proj_link)
    if(append_id_getter.get('is_ok')==True and append_id_getter.get('target_id')):
        append_test = await projects.appendToDo(append_id_getter['target_id'], new_to_do.name)
    else:
        func_return['is_ok']=False
        func_return['status_code']=-1 # -1 is a default error. Sometimes I write while I'm sleepy so it is the best way to keep errors, but not to make it more complex for sleepy brain

    #return {"ok": appender.get("is_ok"), "new_TDL": appender.get("new_TDL")}
    return func_return
