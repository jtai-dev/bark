import commands
import os

class Option:

    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command

        # optional step to call before executing the command
        self.prep_call = prep_call

    def choose(self):
        # calls the preparation step if there is any given
        data = self.prep_call() if self.prep_call else None

        # data is being passed as a parameter in the execute method
        message = self.command.execute(data) if data else self.command.execute()
        print(message)

    def __str__(self):
        return self.name

def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()

def option_choice_is_valid(choice, options):
    # allows lower case input and check if the option is available
    return choice in options or choice.upper() in options

def get_option_choice(options):
    choice = input('Choose an option: ')
    while not option_choice_is_valid(choice, options):
        print('Invalid choice')
        choice = input('Choose an option: ')
    return options[choice.upper()]

# this is used linearly and does not provide options to the user
def get_user_input(label, required=True):
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value

def get_new_bookmark_data():
    # the name and function as key value pair is to be noted
    return {
    'title': get_user_input('Title'),
    'url': get_user_input('URL'),
    # notes is a optional parameter so, required is set to False
    'notes': get_user_input('Notes', required=False)
    }

def get_bookmark_id_for_deletion():
    message = commands.ListBookmarksCommand().execute()
    print(message)
    return get_user_input('Enter a bookmark ID to delete')

# clear the terminal display environment, similar to CTRL+L
def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)

# creates an infinite loop, so does not need to restart the program to use
# another command
def loop():

    options = {
    'A': Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data),
    'B': Option('List bookmarks by date', commands.ListBookmarksCommand()),
    'T': Option('List bookmarks by title', commands.ListBookmarksCommand(order_by='title')),
    'D': Option('Delete a bookmark', commands.DeleteBookmarkCommand(), prep_call=get_bookmark_id_for_deletion),
    'Q': Option('Quit', commands.QuitCommand())
    }

    print_options(options)
    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()
    print()
    _ = input('Press ENTER to return to menu')

if __name__ == '__main__':

    print('Welcome to Bark!')
    print("\n"
          "Bark is a simple to use bookmarking application that runs on a command"
          "line interface (CLI). This creates a local storage of bookmarks without"
          " the need of a browser."
          "\n"
          )
    commands.CreateBookmarksTableCommand().execute()

    while True:
        loop()
        clear_screen()
