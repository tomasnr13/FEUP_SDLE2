class Menu:
    """
    A class to display the menu.

    """
    def __init__(self):
        pass

    
    @staticmethod
    def display_menu(options):
        i = 1
        for option in options:
            print(f'{i} - {option}')
            i += 1

    
    @staticmethod
    def get_user_option(options):
        min_value = 1
        max_value = len(options)
        while True:
            try:
                option = int(input("Select an option: "))
                if option < min_value or option > max_value:
                    print(f"Select an option from {min_value} to {max_value}.")
                else:
                    return options[option - 1]
            except ValueError:
                print(f"Your input should be an integer from {min_value} to {max_value}.")