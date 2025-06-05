from pydantic import BaseModel
from typing import List

#----------PROJECTS----------#

class ProjectModel(BaseModel):
    name: str
    description: str
    authorTeam: str
    authorsList: list
    link: str
    #projectLinks: dict










# ----------TO DO LIST----------#
class ToDoModel (BaseModel):
    id: int
    name: str
    state: int
    #takenBy: int

class ToDoUpdater(BaseModel):
    id: int
    newState: int
    takenBy: int

class ToDoAppender(BaseModel):
    proj_link: str
    name: str


#class TDAF(BaseModel):
#    proj_id: id
#    name: str



#test, never mind
def ToDoModelo():
    pass
