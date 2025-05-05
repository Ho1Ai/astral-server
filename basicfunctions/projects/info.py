from db_connect import db_projects

static_content__to_do = [
            {
                "name": "Make an Application",
                "state": 1,
                }, {
                "name": "Build a Project",
                "state": 1,
                }, {
                "name": "Deploy a Project",
                "state": 1
                }
        ]


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
                }]
            }
        ]

async def getToDo(project_name:str):
   return static_content__to_do

async def getInfo(project_name: str):
    return default_projects

async def getAvailableProjects(username: str):
    return default_projects
    

