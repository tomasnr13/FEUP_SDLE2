import sys
import os
import json
import socket
import utils.utils as utils

from user.user import User
from menu.menu import Menu
from menu.menu_controller import MenuController


def check_arguments():
    if len(sys.argv) != 4:
        print("ERROR: run as $python main.py <port> <username> <password>")
        exit()
    
    if len(sys.argv[2]) < 5 or len(sys.argv[2]) > 20:
        print("ERROR: username length must be between 5 and 24")
        exit()

    if len(sys.argv[3]) < 8 or len(sys.argv[3]) > 20:
        print("ERROR: password length must be between 8 and 24")
        exit()


def check_password(username: str, password: str):
    file =  "passwords/passwords.json"
    isExist = os.path.exists(file)
    if not isExist:
            init = {"passwords": {}}
            with open(file,'w') as file1:
                json.dump(init, file1)
    
    with open(file, 'r+') as json_file:
        data = json.load(json_file)
        if username not in data["passwords"].keys():
            data["passwords"][username] = password
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            print("Account created successfuly!")
            return True
        elif data["passwords"][username] == password:
            print("Login was successful!")
            return True
    return False
 
 
def main(port: int, username: str, password: str):
    port = int(port)
    utils.valid_port(port)

    if not os.path.isdir('passwords'):
            os.mkdir('passwords')

    if not check_password(username ,password):
        print("Wrong password!")
        exit()

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    user = User(ip, port, username)
    menu = Menu()
    menu_controller = MenuController(user)
    user.authentication()

    while True:
        print("\n")
        menu.display_menu(menu_controller.user_options)
        menu_controller.process_user_menu_action()


if __name__ == '__main__':
    check_arguments()
    args = sys.argv
    main(args[1], args[2], args[3])