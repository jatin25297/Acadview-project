from termcolor import colored, cprint
from spy_details import spy, Spy, ChatMessage, friends
from steganography.steganography import Steganography

STATUS_MESSAGES = ['My name is Bond, James Bond', 'Shaken, not stirred.', 'Keeping the British end up, Sir']


print "Hello! Let\'s start with it"
# Asking the user to start with given user
question = "Do you want to continue as " + spy.salutation + " " + spy.name + " (Y/N)? "
existing = raw_input(question)


def add_status():

    updated_status_message = None

    if spy.current_status_message != None:
        # current status message
        print 'Your current status message is %s \n' % spy.current_status_message
    else:
        cprint('Sorry,you don\'t have any status message currently \n', "red")

    default = raw_input("Do you want to select from the older status (y/n)? ")

    if default.upper() == "N":
        new_status_message = raw_input(colored("What status message do you want to set? ","green"))

        if len(new_status_message) > 0:
            STATUS_MESSAGES.append(new_status_message)
            updated_status_message = new_status_message

    elif default.upper() == 'Y':

        item_position = 1

        for message in STATUS_MESSAGES:
            print '%d. %s' % (item_position, message)
            item_position = item_position + 1
# asking the user to choose from inbuilt statuses
        message_selection = int(raw_input("\nChoose from the above messages "))

        if len(STATUS_MESSAGES) >= message_selection:
            updated_status_message = STATUS_MESSAGES[message_selection - 1]

    else:
        print 'The option you chose is invalid! Press y or n.'

    if updated_status_message:
        cprint('Your updated status message is: %s' % updated_status_message, "green")
    else:
        cprint('Oops! You don\'t have a status update',"yellow")

    return updated_status_message


def add_friend():

    friend = Spy('', '', 0, 0.0)
# taking details of the user
    friend.name = raw_input("Please add your friend's name: ")
    friend.salutation = raw_input("Are they Mr. or Ms.?: ")

    friend.name = friend.salutation + " " + friend.name

    friend.age = raw_input("Age?")
    friend.age = int(friend.age)

    friend.rating = raw_input("Spy rating?")
    friend.rating = float(friend.rating)

    if len(friend.name) > 0 and friend.age > 12 and friend.rating >= spy.rating:
        friends.append(friend)
        print 'Friend Added!'
    else:
        print 'Sorry! Invalid entry. We can\'t add spy with the details you provided'

    return len(friends)


def select_a_friend():
    item_number = 0

    for friend in friends:
        print '%d. %s %s aged %d with rating %.2f is online' % (item_number + 1, friend.salutation, friend.name,
                                                   friend.age,
                                                   friend.rating)
        item_number = item_number + 1

    friend_choice = raw_input("Choose from your friends")

    friend_choice_position = int(friend_choice) - 1

    return friend_choice_position


def send_message():

    friend_choice = select_a_friend()
# using steganography encoding the data to then image
    original_image = raw_input("What is the name of the image?")
    output_path = "output.jpg"
    text = raw_input("What do you want to say? ")
    Steganography.encode(original_image, output_path, text)

    new_chat = ChatMessage(text, True)

    friends[friend_choice].chats.append(new_chat)

    print "Your secret message image is ready!"


def read_message():

    sender = select_a_friend()

    output_path = raw_input(colored("What is the name of the file?", "yellow"))

    secret_text = Steganography.decode(output_path)

    def verify_message(self, message, friend_id):
        # conditioning and removing the friend if length of the message is above 100 letters
        if len(message) > 100:
            print "Your Friend %s %s is removed due to spamming" % (
             self.spy.friends[friend_id].salutation, self.spy.friends[friend_id].name)
            self.spy.friends.pop(friend_id)
            return False
# special messages with their definitions
        elif message == "SOS":
            print "Save Our Ship"
        elif message == "SAVE ME":
            print "Hey save me I'm in Danger"
        elif message == "HELP ME":
            print "I need Help as soon as possible"
        return True

    new_chat = ChatMessage(secret_text, False)

    friends[sender].chats.append(new_chat)

    print "Your secret message has been saved!"


def read_chat_history():

    read_for = select_a_friend()

    print '\n6'

    for chat in friends[read_for].chats:
        if chat.sent_by_me:
            print '[%s] %s: %s' % (chat.time.strftime("%d %B %Y"), 'You said:', chat.message)
        else:
            print '[%s] %s said: %s' % (chat.time.strftime("%d %B %Y"), friends[read_for].name, chat.message)


def start_chat(spy):

    spy.name = spy.salutation + " " + spy.name

    if spy.age > 12 and spy.name < 50:

        print "Authentication complete. Welcome " + spy.name + " age: " \
              + str(spy.age) + " and rating of: " + str(spy.rating) + " Proud to have you onboard"

        show_menu = True
# asking user to take perform a action from given functions
        while show_menu:
            menu_choices = "What do you want to do? \n " \
                           "1. Add a status update \n " \
                           "2. Add a friend \n " \
                           "3. Send a secret message \n " \
                           "4. Read a secret message \n " \
                           "5. Read Chats from a user \n " \
                           "6. Close Application \n"
            menu_choice = raw_input(menu_choices)

            if len(menu_choice) > 0:
                menu_choice = int(menu_choice)

                if menu_choice == 1:
                    spy.current_status_message = add_status()
                elif menu_choice == 2:
                    number_of_friends = add_friend()
                    print 'You have %d friends' % number_of_friends
                elif menu_choice == 3:
                    send_message()
                elif menu_choice == 4:
                    read_message()
                elif menu_choice == 5:
                    read_chat_history()
                else:
                    show_menu = False
    else:
        print 'Sorry you are not of the correct age to be a spy'

if existing == "Y":
    start_chat(spy)
else:

    spy = Spy('', '', 0, 0.0)

    spy.name = raw_input("Welcome to spy chat, you must tell me your spy name first: ")

    if len(spy.name) > 0:
        spy.salutation = raw_input("Should I call you Mr. or Ms.?: ")

        spy.age = raw_input("What is your age?")
        spy.age = int(spy.age)

        spy.rating = raw_input("What is your spy rating?")
        spy.rating = float(spy.rating)

        start_chat(spy)
    else:
        print 'Please add a valid spy name'
