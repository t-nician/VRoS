SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

from enum import Enum
from uuid import uuid4

from typing import Any
from socket import socket, AF_INET, SOCK_STREAM

from pydantic import BaseModel, ConfigDict, Field


class BaseField(BaseModel):
    name: str = Field(default="?")
    data: Any = Field(default=None)
    

class BytesField(BaseField):
    data: bytes = Field(default=b"")


class ReplicatorType(Enum):
    UNKNOWN = "unknown_replicator"
    SERVER = "server_replicator"
    CLIENT = "client_replicator"
        

class ReplicationType(Enum):
    UNKNOWN = "unknown_replication"
    
    CREATE = "create_replication"
    UPDATE = "update_replication"
    DELETE = "delete_replication"
    
    EMIT = "emit_replication"    
    

class ReplicationCommand(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    
    replication_type: ReplicationType = Field(default=ReplicationType.UNKNOWN)
    

class BaseReplicator(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    
    server_host: str = Field(default=SERVER_HOST)
    server_port: int = Field(default=SERVER_PORT)
    
    replicator_type: ReplicatorType = Field(default=ReplicatorType.UNKNOWN)
    
    connection_socket: socket = Field(
        default_factory=lambda: socket(AF_INET, SOCK_STREAM)
    )
    
    available_fields: list[BaseField] = Field(default_factory=list)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def add_field(self, field: BaseField) -> BaseField:
        self.available_fields.append(field)
    

class ClientReplicator(BaseReplicator):
    replicator_type: ReplicatorType = Field(default=ReplicatorType.CLIENT)
    
    def establish(self):
        self.connection_socket.connect(
            (self.server_host, self.server_port)
        )


class ServerReplicator(BaseReplicator):
    listen: int = Field(default=2)
    
    replicator_type: ReplicatorType = Field(default=ReplicatorType.SERVER)
    
    def establish(self):
        self.connection_socket.bind(
            (self.server_host, self.server_port)
        )
            
        self.connection_socket.listen(self.listen)
    
    
    def replicate_field(self, field_name: str) -> BaseField:
        pass