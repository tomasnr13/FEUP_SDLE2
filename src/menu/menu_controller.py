from menu.menu import Menu
from user.post import Post

import datetime


class MenuController:
    """
    A class that controls the menu input.

    Attributes
    ----------
    user : User
        user of the menu
    """
    def __init__(self, user):
        self.user = user
        self.user_options = ["Post", "Follow", "Unfollow", "See your timeline", "See complete timeline", "Show followers", "Show following", "Logout"]
        self.count = 0


    def process_user_menu_action(self):
        option = Menu.get_user_option(self.user_options)
        if option == "Post":
            print("Write your post:")
            post_content = str(input())
            if len(post_content) == 0:
                print("Post cannot be empty!")
            elif len(post_content) > 300:
                print("Post length exceeded!")
            else:
                post = Post(self.count, self.user.username, datetime.datetime.now(), post_content)
                self.user.post(post)
                self.count += 1
        elif option == "Follow":
            username = str(input("Enter the name of the user to follow: "))
            print(self.user.follow(username))
        elif option == "Unfollow":
            username = str(input("Enter the name of the user to unfollow: "))
            print(self.user.unfollow(username))
        elif option == "See your timeline":
            print("\nThis is your timeline: ")
            self.user.show_user_posts()
        elif option == "See complete timeline":
            print("\nThis is the full timeline: ")
            self.user.show_timeline()
        elif option == "Show followers":
            print(f"\nYou have {len(self.user.info.followers)} follower(s): ")
            self.user.show_followers()
        elif option == "Show following":
            print(f"\nYou follow {len(self.user.info.following)} user(s): ")
            self.user.show_following()
        elif option == "Logout":
            self.user.logout()
            exit()
