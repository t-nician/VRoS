import time
import asyncio
import threading

from vros import ServerReplicator, ClientReplicator, BytesField


async def client():
    client = ClientReplicator()
    
    @client.field("echo")
    async def echo_field(bytes_field: BytesField):
        print("bytes field was updated to", bytes_field)
    
    
    await client.establish()
    


async def server():
    server = ServerReplicator()
    
    echo_field = BytesField(
        name="echo",
        data=b"hello world?"
    )
    
    # Add your replicateable fields.
    server.add_field(echo_field)
    
    threading.Thread(target=server.establish, args=()).start()
    
    while True:
        time.sleep(1)
        
        # Field is being replicated!
        echo_field.data = b"Huhh!?"
        server.replicate_field(echo_field.name)
    #print(server.connection_socket)
    


if __name__ == "__main__":
    threading.Thread(target=asyncio.run, args=(server(),)).start()
    asyncio.run(client())