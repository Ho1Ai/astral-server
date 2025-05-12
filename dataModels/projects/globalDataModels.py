from pydantic import BaseModel
from typing import List

#----------PROJECTS----------#

class ProjectModel(BaseModel):
    name: str
    description: str
    authorTeam: str
    authorsList: list











# ----------TO DO LIST----------#
class ToDoModel (BaseModel):
    id: int
    name: str
    state: int

class ToDoAppender(BaseModel):
    name: str
    state: int





def ToDoModelo():
    pass
