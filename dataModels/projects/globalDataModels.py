from pydantic import BaseModel

class ToDoModel (BaseModel):
    id: int
    name: str
    state: int

def ToDoModelo():
    pass
