from pydantic import BaseModel

# well, I guess I had better place migration models in dataModels/migrations
class TokenFunctionsMigration(BaseModel):
    access_jwt: str
    refresh_jwt: str
