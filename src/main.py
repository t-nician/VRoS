import time
import asyncio
import threading

from uuid import uuid4

from vros import *


class GlobalVariables(ReplicationModel):
    server_message: str = Field(default="server message!")
    
    class ReplicationMeta:
        exclude=[]
        include=[]


async def server():
    variables = GlobalVariables(
        replication_type=ReplicationType.SERVER_TO_CLIENT,
        replication_environment=ReplicationEnvironment.SERVER
    )
    
    
    threading.Thread(target=asyncio.run, args=(variables.establish(),)).start()
    
    variables.server_message = "Hello there!"
    

async def client():
    variables = GlobalVariables(
        replication_type=ReplicationType.SERVER_TO_CLIENT,
        replication_environment=ReplicationEnvironment.CLIENT
    )
    
    
    
    await variables.establish()
    
    
asyncio.run(server())
asyncio.run(client())