import os
import json
import threading

from user.kInfo import KademliaInfo
from user.node import Node
from user.post import Post
from sockets.sender import Sender
from sockets.receiver import Receiver


class User:
    """
    A class to represent a user.

    Attributes
    ----------
    ip : str
        ip of the user
    port: int
        port of the user
    username: str
        name of the user
    """
    def __init__(self, ip, port, username):
        self.info = KademliaInfo(ip, port, [], [])
        self.username = username
        self.user_posts = []
        self.following_timelines = {} # username -> list of posts
        self.sender = Sender()

        self.node = Node(port)

        self.receiver = Receiver(self)
        self.recthread = threading.Thread(target=self.receiver.run, daemon=True)
        self.recthread.start()


    def authentication(self):
        user_info = self.node.get_kademlia_info(self.username)
        if (user_info is None):
            self.node.set_kademlia_info(self.username, self.info)
            print("Welcome " + self.username + "!")
        else:
            self.info = user_info
            print("Welcome back " + self.username + "!")

            file = 'posts/' + self.username + '.json'
            isExist = os.path.exists(file)

            if isExist:
                with open(file) as json_file:
                    data = json.load(json_file)
                    for p in data["posts"]:
                        post = Post.read(self.username, p)
                        self.post(post, flag=1)

            for username in self.info.following:
                info = self.node.get_kademlia_info(username)
                if (info is not None and self.sender.get(self.username, username, info.ip, info.port)):
                    print("Got posts from owner")
                else:
                    for user in self.info.followers:
                        user_info = self.node.get_kademlia_info(user)
                        if user_info is not None and username in user_info.following:
                            if (self.sender.get(self.username, username, user_info.ip, user_info.port)):
                                print("Got posts from follower")


    def logout(self):
        print("Logging out...")
        #self.node.loop.stop()
        print("Logged out!")


    def post(self, post, flag=0):
        self.user_posts.append(post)
        self.order_user_posts()
        if flag==0:
            post.save()
            # Send post to followers
            followers = self.info.followers
            for user in followers:
                info_user = self.node.get_kademlia_info(user)
                self.sender.post(post, info_user.ip, info_user.port)


    def order_user_posts(self):
        # Put most recent posts on the beginning
        self.user_posts.sort(key=lambda x: x.time, reverse=True)

  
    def show_user_posts(self):
        for post in self.user_posts:
            print("\n")
            post.show()


    def show_timeline(self):
        if not self.following_timelines:
            self.show_user_posts()
            return
        following_posts = [item for sublist in self.following_timelines.values() for item in sublist]
        timeline = following_posts + self.user_posts

        timeline.sort(key=lambda x: x.time, reverse=True)
        for post in timeline:
            print("\n")
            post.show()


    def follow(self, username):
        followed_info = self.node.get_kademlia_info(username)

        if username in self.info.following:
            return "You already follow " + username
        if username == self.username:
            return "You cannot follow yourself!" 
        if followed_info == None:
            return "The user you are trying to follow does not exist"

        if self.sender.follow(self.username, followed_info.ip, followed_info.port):
            self.info.following.append(username)
            self.node.set_kademlia_info(self.username, self.info)
            return "You started following " + username

        return "Unable to follow " + username


    def unfollow(self, username):
        unfollowed_info = self.node.get_kademlia_info(username)

        if username == self.username:
            return "You cannot unfollow yourself!"
        if unfollowed_info == None:
            return "The user you are trying to unfollow does not exist"
        if username not in self.info.following:
            return "You are already not following " + username
            
        if self.sender.unfollow(self.username, unfollowed_info.ip, unfollowed_info.port):
            self.info.following.remove(username)
            self.node.set_kademlia_info(self.username, self.info)
            if username in self.following_timelines:
                del self.following_timelines[username]
            return "You unfollowed " + username

        return "Unable to unfollow " + username


    def show_following(self):
        for username in self.info.following:
            print(username)


    def show_followers(self):
        for username in self.info.followers:
            print(username)
        