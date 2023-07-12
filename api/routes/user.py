from fastapi import APIRouter , Depends , Response , status
from config.db import conn
from schemas.user import User
from bson import ObjectId
from auth.oauth2 import oauth2_scheme
from serializers.user import userEntity , usersEntity , serializer_single , serializer_group

router = APIRouter(prefix='/user' ,tags=["User"])

@router.get("find_all_user/" , summary="find all user" , description="Creates a list of users from the database")
    # makes query to database to return all users
async def find_all_user():
    return serializer_group(conn.local.user.find())

@router.get("find_single_user/" , summary="find specific user" , description="Finds a specific user from the database")
    # makes query to database to return single specific user
async def find_single_user(id):
    return serializer_single(conn.local.user.find_one({"_id":ObjectId(id)}))

    # Requires authentication
@router.post('create_user/' )
    # makes query to database to create user
async def create_user(user:User , token:str=Depends(oauth2_scheme) ,  summary="create user" , description="Creates your own custom user"):
    conn.local.user.insert_one(dict(user))
    return serializer_group(conn.local.user.find())

@router.delete('delete_user/', summary="delete specific user" , description="Deletes a specific user from the database" )
    # makes query to database to delete specific user
async def delete_user(id):
    conn.local.user.find_one_and_delete({"_id":ObjectId(id)})
    
    return Response(status_code=200 , content="the operation well done")

@router.put('update_user/', summary="update specific user" , description="Updates a specific user from the database" )
    # makes query to database to update specific user
async def update_user(id , user:User):
    conn.local.user.find_one_and_update({"_id":ObjectId(id)},{
        "$set" : dict(user)
    })
    return serializer_single(conn.local.user.find_one({"_id":ObjectId(id)}))
