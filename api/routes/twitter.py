import requests
from config.db import conn
from requests_oauthlib import OAuth1
from fastapi import APIRouter , HTTPException 
from serializers.user import serializer_group , serializer_single

router = APIRouter(prefix="/twitter" , tags=["twitter"])
    # we can takes them from developer.twitter.com
consumer_key = "private :)"
consumer_secret = "------"
access_token = "------"
access_token_secret = "------"
    # set up OAuth1 authentication
oauth = OAuth1(
    consumer_key,consumer_secret,access_token,access_token_secret,
    )
@router.get("/twitter_login" , summary="login to twitter" , description="Makes a request to login to the Twitter")
async def twitter_login():
    # make a request to the Twitter
    response = requests.get("https://api.twitter.com/1.1/account/verify_credentials.json", auth=oauth, timeout=100)

    # return the account information as JSON
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=400, detail="Invalid Twitter credentials")
    
    # save the credentials to database
    conn.local.twitter.insert_one(response.json())
    return serializer_single(conn.local.twitter.find_one({},{'_id:true'}))