from fastapi import Depends , status , APIRouter
from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from auth.oauth2 import create_access_token
from config.db import conn
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(prefix="/authentication",tags=["authentication"])

@router.post('/token' ,  summary="authentication" , description="Give token from here")
def get_token(request:OAuth2PasswordRequestForm =Depends()):
    # find specific user from database
    user = conn.local.user.find_one({"name":request.username})
    # handling possible errors
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="incorrect value")
    # create token
    temp_token = create_access_token(data={"sub":request.username})
    
    return {
        'access_token' : temp_token,
        'type_token' : 'bearer',
        'userID' : str(user["_id"]),
        'username' : user['name'],
    }
    
    