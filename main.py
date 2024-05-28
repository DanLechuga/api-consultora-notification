import http
from typing import Annotated
from notification_middleware.dto.request import sendNotification
from notification_Service import notificationService
from fastapi import FastAPI,HTTPException,Depends
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jose import jwt
import os
import datetime
from starlette import status

def getEnviromentVariable(name):
    return os.environ.get(name,"NOT FOUND")

get_token_bearer = HTTPBearer(auto_error=False,
description="Autoritazion JWT esquema. \r\n\r\n Write your token \r\n\r\n Example: \'12345abcdf\'")

app = FastAPI(
    title='Service - Notification',
    openapi_tags=[{
        "name":"Notification",
        "description":"Send emails to team"
        }],
    swagger_ui_parameters={
        'syntaxHighligth.theme':'obsidian'
    }
)

SECRET_KEY = getEnviromentVariable("key_jwt")
ALGORITH = "HS256"
TOKEN_EXPIRES = 1440


@app.get("/",include_in_schema=False,response_class=RedirectResponse)
async def redirectToSwagger():
    return "/docs"


@app.get("/notifications/test",tags=['Notification'],status_code=status.HTTP_200_OK)
def Test():
    return JSONResponse(
        status_code= status.HTTP_200_OK,
        content={"date":f"{datetime.datetime.now()}","version":"1.0.0"} 
    )

@app.post("/notifications/sendMail",tags=['Notification'],status_code=status.HTTP_200_OK)
async def sendMail(notification : sendNotification.sendNotification,auth: Annotated[HTTPAuthorizationCredentials,Depends(get_token_bearer)]):
    try:
        if(auth == None):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incoorectas",
                headers={"WWW-Autenticate":"Bearer"}
            )
        if(auth.credentials != "" and len(auth.credentials) > 7 and auth.scheme == "Bearer"):
            payload = jwt.decode(auth.credentials,SECRET_KEY,algorithms=[ALGORITH])    
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incoorectas",
                headers={"WWW-Autenticate":"Bearer"}
            )
        await notificationService.sendMail(notification)     
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{e}"
            )
        
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message":"Notification Send"}
    )         
