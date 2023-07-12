from pydantic import BaseModel
    # basic model for create and update user
class User(BaseModel):
    name : str
    email : str
    password : str