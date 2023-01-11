import json
import os

from datetime import datetime


class Post:
    """
    A class to represent a post.

    Attributes
    ----------
    id : int
        id of the post
    username : str
        username of the post's publisher
    time : datetime
        time of the post
    content : str
        content of the post
    """
    def __init__(self, id, username, time, content):
        self.id = id
        self.username = username
        self.time = time
        self.content = content

        if not os.path.isdir('posts'):
            os.mkdir('posts')


    def show(self):
        print(f'{self.content}\nby {self.username} on {self.time.date()} at {str(self.time.time())[:-7]}')


    def save(self):
        file = 'posts/' + self.username + ".json"
        isExist = os.path.exists(file)
        post = {
            "id": self.id,
            "time": str(self.time),
            "content": self.content
        }
        
        if not isExist:
            init = {"posts": []}
            with open(file,'w') as file1:
                json.dump(init, file1)

        with open(file,'r+') as file2:
            # First we load existing data into a dict.
            file_data = json.load(file2)
            # Join new_data with file_data inside posts
            file_data["posts"].append(post)
            # Sets file's current position at offset.
            file2.seek(0)
            # convert back to json.
            json.dump(file_data, file2, indent=4)

            
    def read(username, json_str):
        return Post(
            json_str["id"],
            username,
            datetime.strptime(json_str["time"], '%Y-%m-%d %H:%M:%S.%f'),
            json_str["content"])


    def __eq__(self, other): 
        if not isinstance(other, Post):
            return False

        return self.id == other.id and self.username == other.username and self.time == other.time and self.content == other.content