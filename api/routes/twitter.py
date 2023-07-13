import requests
from config.db import conn
from requests_oauthlib import OAuth1
from fastapi import APIRouter , HTTPException 
from serializers.user import serializer_group , serializer_single

router = APIRouter(prefix="/twitter" , tags=["twitter"])
    # we can takes them from developer.twitter.com

@router.get("/get_info" , summary="login to twitter" , description="Makes a request to login to the Twitter")
async def get_info():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-csrf-token': '5260734251631632e664f9058ed0d587e183ded8942b29a52487705290cc72daf21734d0a10b2ead83521d2e833e046b77e2e5e532241603ef1642419540d65f40eff3df733fb706115e3177debe63af'
    ,'X-Client-Transaction-Id': '578515divn4lgeBRO0MfxPUfJu+eH2cLAGGXppZsZOiYdBRrN0Q4QvUUQDkjtaHJezu6XwBKlVr3t0KN/Fsx5zSOF3wX'
    ,'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
    ,'Proxy-Authorization': 'Basic LnN2QDIwMTkwMjM2O2lyLjo5RHMvc0wvK0V6MjBqYW9PdE1vdjNRSHVVZWpOZ0JzNmhSWGF0SmRFRUdOMi8wa2RjeDh2NkE9PQ=='
    ,'Connection': 'keep-alive'
    ,'Cookie': 'eu_cn=1; dnt=1; kdt=n6BvuPArAbGxmxkPLOj9C4bGvM9919K7kic1J4AK; d_prefs=MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; guest_id_ads=v1%3A168907575455046643; guest_id_marketing=v1%3A168907575455046643; mbox=PC#1e6f46493db3478383c00f4eea13a788.37_0#1752351135|session#7852614e915a4005b45deb1c050476ab#1689108195; _ga_BYKEBDM7DS=GS1.1.1689067591.1.1.1689068404.0.0.0; _ga=GA1.2.734822766.1689066923; _gid=GA1.2.2039220934.1689067653; _ga_34PHSZMC42=GS1.1.1689101917.6.1.1689106328.0.0.0; des_opt_in=Y; _gcl_au=1.1.295583959.1689071062; gt=1679253027662831616; personalization_id="v1_8LKwDOTptHxWBTKxqH1DiA=="; guest_id=v1%3A168920024310248575; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCENGLkyJAToMY3NyZl9p%250AZCIlMGFmNjE0NWM2NjU5NDM1ODM1ZGQyZmNlYTE5N2Y1OWI6B2lkIiUzOWY4%250AY2FkZmVjZjg3MjZkN2NhYmJiMDhhMGIyMjcxYQ%253D%253D--ebde7db0c1908c82bb2d7f0ebf8e147d788ba29f; ct0=5260734251631632e664f9058ed0d587e183ded8942b29a52487705290cc72daf21734d0a10b2ead83521d2e833e046b77e2e5e532241603ef1642419540d65f40eff3df733fb706115e3177debe63af; twid=u%3D1455171192919232519; auth_token=e9ff5be553c65f2b894c0a96b63c3af685ae3691; att=1-Hn7O8d3WibHiXC0igsCN6GyMDmZ7AI5jewLpMSex'
    ,'TE': 'trailers'
    }
    params = {
        'include_mention_filter':'true',
        'include_nsfw_user_flag':'true',
        'include_nsfw_admin_flag':'true',
        'include_ranked_timeline':'true',
        'include_alt_text_compose':'true',
        'ext':'ssoConnections',
        'include_country_code':'true',
        'include_ext_dm_nsfw_media_filter':'true',
        'include_ext_sharing_audiospaces_listening_data_with_followers':'true'
    }

    # Make GET request to retrieve user information
    response = requests.get(
        "https://api.twitter.com/1.1/account/settings.json",
        headers=headers,
        params=params,
        timeout=99
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=400, detail="Invalid Twitter credentials")
    
    # save the credentials to database
    conn.local.twitter.insert_one(response.json())
    return serializer_single(conn.local.twitter.find_one({},{'_id:true'}))
