from fastapi import FastAPI
from routes import user , authentication , twitter

app = FastAPI()
    # It connects other routers to the main app
app.include_router(twitter.router)
app.include_router(user.router)
app.include_router(authentication.router)
