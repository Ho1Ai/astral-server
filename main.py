from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.project.projectRouter import router as project_router
from router.account.userRouter import router as accs_router

from basicfunctions.projects import info

app = FastAPI()

allowed_origins=[
        "http://localhost:5173"
        ]

app.add_middleware(CORSMiddleware, 
                   allow_origins=["*"], 
                   allow_methods=["*"],
                   allow_credentials=True, 
                   allow_headers=["*"],
)

app.include_router(accs_router)
app.include_router(project_router)
