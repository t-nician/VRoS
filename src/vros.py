from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ReplicationType(Enum):
    LOCAL_ONLY = "local_only"
    
    SERVER_TO_CLIENT = "server_to_client"
    CLIENT_TO_SERVER = "client_to_server"


class ReplicationEnvironment(Enum):
    UNKNOWN = "unknown_environment"
    
    SERVER = "server_environment"
    CLIENT = "client_environment"





class ReplicationModel(BaseModel):
    replication_type: ReplicationType = Field(
        default=ReplicationType.LOCAL_ONLY
    )
    
    replication_environment: ReplicationEnvironment = Field(
        default=ReplicationEnvironment.UNKNOWN
    )
    
    def __replicate(self, name: str, value: Any):
        print("replicating", name, value)
    
    def __setattr__(self, name: str, value: Any) -> None:
        if self.replication_type is ReplicationType.SERVER_TO_CLIENT:
            if self.replication_environment is ReplicationEnvironment.CLIENT:
                raise Exception(
                    "Client cannot setattr to a model controlled by the server!"
                )
        
        if self.replication_type is ReplicationType.CLIENT_TO_SERVER:
            if self.replication_environment is ReplicationEnvironment.SERVER:
                raise Exception(
                    "Server cannot setattr to a model controlled by the server!"
                )
        
        if not self.replication_type is ReplicationType.LOCAL_ONLY:
            replication_meta = type(self).ReplicationMeta
     
            include = None
            exclude = None
            
            try:
                include = getattr(replication_meta, "include")
                include.extend(
                    ReplicationModel.ReplicationMeta.include
                )
            except:
                include = ReplicationModel.ReplicationMeta.include
            
            try:
                exclude = getattr(replication_meta, "exclude")
                exclude.extend(
                    ReplicationModel.ReplicationMeta.exclude
                )
            except:
                exclude = ReplicationModel.ReplicationMeta.exclude
            
            if exclude.count(name) == 0:
                if len(include) > 0:
                    if include.count(name) == 1:
                        self.__replicate(name, value)
                else:
                    self.__replicate(name, value)
        
        return super().__setattr__(name, value)
    
    async def establish(self):
        pass
    
    async def on_establish(self):
        
    
    class ReplicationMeta:
        exclude=[
            "replication_type", "replication_owner"
        ]
        
        include=[]