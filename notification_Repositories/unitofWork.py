from pymongo import MongoClient
import os

def getVariable(name):
    return os.environ.get(name,"NOT FOUND")


uri = getVariable("bd_notification")

client = MongoClient(uri)


async def connectBd ()-> bool:
    isConnect = False
    try: 
        client.admin.command("ping")
        isConnect = True
    except Exception as e:
        print(f"{e}")
    return isConnect        
        
    