import asyncio
import sys
import shutil

from utils.var import IP, PORT
from utils.utils import set_logger
from kademlia.network import Server


class Bootstrap:
    """
    A class to represent the bootstrap of the network.

    """
    def __init__(self) -> None:
        self.ip = IP
        self.port = PORT
        self.server = Server()
        set_logger()


    def run(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.server.listen(self.port))
        try:
            print(f"Started Bootstrap on ip {self.ip} and port {self.port}")
            loop.run_forever()
        except KeyboardInterrupt:
            print(f"Stopped Bootstrap on ip {self.ip} and port {self.port}")
        finally:
            shutil.rmtree('passwords')
            shutil.rmtree('posts')
            self.server.stop()
            loop.close()


def check_arguments():
    if (len(sys.argv) != 1):
        print("ERROR: run as $python bootstrap.py")
        exit()


def main():
    bootstrap = Bootstrap()
    bootstrap.run()


if __name__ == '__main__':
    check_arguments()
    main()