import asyncpg
from dotenv import dotenv_values

cfg = dotenv_values(".env")

#DB_URL = "postgresql://postgres:root@localhost/astraldb"

#print(cfg) #debug line

async def db_connect():
    return await asyncpg.create_pool(cfg.get("DB_URL"))
