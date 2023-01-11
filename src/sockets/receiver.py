import zmq

from datetime import datetime
from user.post import Post


class Receiver:
    """
    A class that processes received messages

    Attributes
    ----------
    user : User
        user receiving messages
    """
    def __init__(self, user) -> None:
        self.user = user
        self.ip = user.info.ip
        self.port = user.info.port
        self.context = zmq.Context()
        self.router = self.context.socket(zmq.REP)
        self.router.bind(f'tcp://{self.ip}:{self.port}')

        # Create Poller to handle the messages
        self.poller = zmq.Poller()
        self.poller.register(self.router, zmq.POLLIN)


    def run(self):
        while True:
            try:
                socks = dict(self.poller.poll(2))
            except: #zmq.ZMQError
                print(f"ERROR: Listener on ip {self.ip} and port {self.port} failed!")
                exit()
            if socks.get(self.router) == zmq.POLLIN:
                message = self.router.recv_multipart()
                self.parse_msg(message)


    def parse_msg(self, msg_bytes):
        message = msg_bytes[0].decode('utf-8').split(" ")
        reply = 'ERROR: Incorrect Message Format. Message received: ' + str(message)

        # FOLLOW MESSAGE
        if message[0] == 'follow':
            username = str(message[1])
            print(f"\n{username} started following you!")    
            reply = "success"
            self.user.info.followers.append(username)
            self.user.node.set_kademlia_info(self.user.username, self.user.info)
            follower_info = self.user.node.get_kademlia_info(username)
            if follower_info != None:
                for post in self.user.user_posts:
                    self.user.sender.post(post, follower_info.ip, follower_info.port)

        # UNFOLLOW MESSAGE
        if message[0] == 'unfollow':
            username = str(message[1])
            print(f"{username} unfollowed you!")    
            reply = "success"
            self.user.info.followers.remove(username)
            self.user.node.set_kademlia_info(self.user.username, self.user.info) 
        
        # POST MESSAGE
        if message[0] == 'post':
            id = message[1]
            username = message[2]
            time = str(message[3]) + " " + str(message[4])
            time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
            content = ' '.join(message[5:])
            post = Post(id, username, time, content) 
            
            if username in self.user.following_timelines.keys():
                if post not in self.user.following_timelines[username]:
                    self.user.following_timelines[username].append(post)
            else:
                self.user.following_timelines[username] = [post]
            reply = "success"

        # GET POSTS MESSAGE
        if message[0] == 'get':
            req_username = str(message[1])
            sender_username = str(message[2])    
            reply = "success"
            req_info = self.user.node.get_kademlia_info(req_username)
            if req_info != None:
                # IF IM THE OWNER OF THE POSTS
                if self.user.username == sender_username:
                    for post in self.user.user_posts:
                        self.user.sender.post(post, req_info.ip, req_info.port)
                # IF I FOLLOW THE OWNER OF THE POSTS
                else:
                    if sender_username in self.user.following_timelines.keys():
                        posts = self.user.following_timelines[sender_username]
                        for post in posts:
                            self.user.sender.post(post, req_info.ip, req_info.port)


        self.router.send_multipart([reply.encode('utf-8')])