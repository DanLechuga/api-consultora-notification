from pydantic import BaseModel


class sendNotification(BaseModel):
    phoneNumber:str |None = None 
    email:str |None = None
    message:str |None = None
      