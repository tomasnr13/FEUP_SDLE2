import zmq
import utils.zmq_utils as zmq_utils


class Sender:
    """
    A class that sends messages

    Attributes
    ----------
    user : User
        user receiving messages
    """
    def __init__(self) -> None:
        # Create Publisher Socket
        self.context = zmq.Context()


    def connect_to_user(self, ip, port):
        self.proxy_socket = self.context.socket(zmq.REQ)
        self.proxy_socket.connect(f'tcp://{ip}:{int(port)}')


    def follow(self, username, ip, port):

        follow_message = 'follow ' + username

        self.connect_to_user(ip, port)

        res = zmq_utils.send_msg(self.context, self.proxy_socket, ip, port, follow_message)
        if res != -1:
            return True
        else:
            return False


    def unfollow(self, username, ip, port):
        unfollow_message = 'unfollow ' + username

        self.connect_to_user(ip ,port)
        
        res = zmq_utils.send_msg(self.context, self.proxy_socket, ip, port, unfollow_message)
        if res != -1:
            return True
        else:
            return False


    def post(self, post, ip, port):
        post_message = 'post {} {} {} {}'.format(post.id, post.username, post.time, post.content)

        self.connect_to_user(ip ,port)
        
        res = zmq_utils.send_msg(self.context, self.proxy_socket, ip, port, post_message)
        if res != -1:
            return True
        else:
            return False


    def get(self, username1, username2, ip, port):
        get_message = 'get ' + username1 + " " + username2

        self.connect_to_user(ip ,port)
        
        res = zmq_utils.send_msg(self.context, self.proxy_socket, ip, port, get_message)
        if res != -1:
            return True
        else:
            return False

    