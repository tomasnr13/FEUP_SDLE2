from dataclasses import asdict, dataclass
from dataclasses_json import dataclass_json

import json


@dataclass_json
@dataclass
class KademliaInfo:
    """
    A class that represents the information being saved on dht

    """
    ip: str
    port: int
    following: list
    followers: list

    def set(self):
        return json.dumps(asdict(self))
        

    def get(json_str: str):
        kademlia_info_json = json.loads(json_str)
        return KademliaInfo(
            kademlia_info_json["ip"],
            kademlia_info_json["port"],
            kademlia_info_json["following"],
            kademlia_info_json["followers"])