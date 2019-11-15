import socket
from appJar import gui
import threading

"""Client for game/chat application"""


def receive_from_server(client_socket):
    try:
        while True:
            incoming_message = client_socket.recv(1024)

            if not incoming_message:
                break

            incoming_message = incoming_message.decode('utf-8')
            print(incoming_message)
            if incoming_message[0] == "S":
                app.setTextArea('Display', incoming_message)
            elif incoming_message[0] == "C":
                # TODO challange logic
                pass

    except ConnectionAbortedError as error:
        print('Receive_from_server error: ', error)

# TODO
def send_message_button():

    send_message = app.getTextArea('Message_entry')

    send_message = f"S{send_message}".encode('utf-8')
    client_socket.sendall(send_message)

    app.clearTextArea('Message_entry')


def name_submit_button():

    name = app.getEntry('NameEntry')
    if len(name) != 0:
        client_socket.sendall(name.encode('utf-8'))
        name_validation = bool(int(client_socket.recv(1024).decode('utf-8')))

        if not name_validation:
            app.destroyAllSubWindows()
            app.show()
            receive_messages = threading.Thread(target=receive_from_server, args=(client_socket,), daemon=True)
            receive_messages.start()

        else:
            app.errorBox('Invalid name', 'Name is not available\nPlease try another one.')
            app.clearEntry('NameEntry')
    else:
        app.errorBox('Invalid name', 'Name needs to contain at least one character')


def cancel_button():
    client_socket.close()
    app.stop()

# TODO
def accept_challange_button():
    pass

# TODO
def decline_challange_button():
    pass



def buttons(name):

    button_dict = {'Submit': name_submit_button,
                   'Cancel': cancel_button,
                   'Send': send_message_button,
                   'Close': cancel_button,
                   'Accept': accept_challange_button,
                   'Decline': decline_challange_button}

    for k, v in button_dict.items():
        if k == name:
            v()

# TODO Create subwindow for game
def create_gui():

    # SUBWINDOW LOGIN
    app.startSubWindow("NameSubWindow", modal=True)
    app.setSize("280x135")
    app.setResizable(canResize=False)
    app.startLabelFrame('ChatGame', 1, 0)

    app.setPadding([5, 0])
    app.addLabel('leftfiller', '        ', 0, 0)
    app.addLabel('rightfiller', '        ', 0, 2)

    app.startFrame('functionality', 0, 1)

    app.addLabel("usernamelabel", "- Enter Username -", 0, 0, colspan=2)
    app.getLabelWidget("usernamelabel").config(font="verdana 11 bold")
    app.addEntry('NameEntry', 1, 0, colspan=2)
    app.setEntryAnchor('NameEntry', 'center')

    # Subwindow Button
    app.startFrame('buttonframe', 2, 0)
    app.setPadding([0, 15])
    app.setSticky('')
    app.addButton('Submit', buttons, 2, 0)
    app.addLabel('buttonfiller', '', 2, 1)
    app.addButton('Cancel', buttons, 2, 2)
    app.stopFrame()

    app.stopFrame()  # functionality
    app.stopLabelFrame()
    app.stopSubWindow()


    # MAIN WINDOW
    app.setSize('750x400')
    app.setResizable(canResize=False)

    app.startFrame('Outer_frame', 1, 0)
    app.startLabelFrame('')

    # Makes a column of empty labels to the left
    for i in range(8):
        if i == 7:
            i += 1
        app.addEmptyLabel('Label' + str(i), i, 0)

    # DISPLAY
    app.addScrolledTextArea('Display', 0, 1, 6, 6)
    app.disableTextArea('Display')
    app.setTextAreaHeight('Display', 20)
    app.setTextAreaWidth('Display', 60)

    # PLAYERS ONLINE LIST
    app.addListBox('Online_users_listbox', online_users, 0, 7, rowspan=4)

    # MESSAGE ENTRY
    app.addTextArea('Message_entry', 7, 1, 6)
    app.setTextAreaHeight('Message_entry', 6)
    app.setTextAreaWidth('Message_entry', 60)

    # BUTTONS
    app.startFrame('button_frame', 4, 7, rowspan=5)
    app.setPadding([1, 8])
    app.addLabel('bl1', ' ', 1, 0)
    app.addLabel('bl2', ' ', 1, 4)

    #Challange buttons
    app.addButton('CHALLANGE', buttons, 0, 1, colspan=3)
    app.addLabel('challangelabel', 'Challanged by:', 1, 1, colspan=2)
    app.setLabelFg('challangelabel', 'darkgray')                        # Turns black when challanged
    app.addLabel('challanger_name', '', 2, 1, colspan=2)                # Challengers name goes in here when challanged
    app.addButton('Accept', buttons, 3, 1)
    app.addButton('Decline', buttons, 3, 3)
    app.disableButton('Accept')
    app.disableButton('Decline')

    #Chat buttons
    app.addButton('Send', buttons, 4, 1)
    app.addLabel('filler', '', 4, 2)
    app.addButton('Close', buttons, 4, 3)
    app.stopFrame()  # button_frame

    app.stopLabelFrame()
    app.stopFrame()  # Outer_frame

    # GENERAL DESIGN
    app.setFont(size=10, family='Verdana', weight='bold')
    ta1 = app.getTextAreaWidget("Message_entry")
    ta2 = app.getTextAreaWidget("Display")
    ta1.config(font=("Verdana 10 bold"))
    ta2.config(font=("Verdana 10 bold"))


if __name__ == '__main__':

    online_users = []
    IP = "127.0.0.1"
    PORT = 1234

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    app = gui()
    create_gui()
    app.go(startWindow='NameSubWindow')
