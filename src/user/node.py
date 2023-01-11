import asyncio
import threading

from kademlia.network import Server
from user.kInfo import KademliaInfo
from utils.var import IP, PORT


class Node:
    """
    A class that represents the node on dht

    Attributes
    ----------
    port : int
        port for the node
    """
    def __init__(self, port):
        self.port = port
        self.server = Server()
        self.loop = asyncio.new_event_loop()
        self.run()

    
    def set_kademlia_info(self, key: str, kademlia_info):
        asyncio.run_coroutine_threadsafe(self.server.set(key, kademlia_info.set()), self.loop)


    def get_kademlia_info(self, key: str):
        info = asyncio.run_coroutine_threadsafe(self.server.get(key), self.loop).result()
        if info is None:
            return None
        return KademliaInfo.get(info)


    def run(self):
        try:
            self.loop.run_until_complete(self.server.listen(self.port))
        except:
            print(f"ERROR: The port {self.port} is already being used!")
            exit()
        self.loop.run_until_complete(self.server.bootstrap([(IP, PORT)]))
        threading.Thread(target=self.loop.run_forever, daemon=True).start()