import sys, os
filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import OAuthZoomClient

import json
from configparser import ConfigParser
from pyngrok import ngrok

parser = ConfigParser()
parser.read("bots/bot.ini")
client_id = parser.get("OAuth", "client_id")
client_secret = parser.get("OAuth", "client_secret")
port = parser.getint("OAuth", "port", fallback=4001)
browser_path = parser.get("OAuth", "browser_path")
print(f'id: {client_id} browser: {browser_path}')

redirect_url = ngrok.connect(port, "http")
print("Redirect URL is", redirect_url)

client = OAuthZoomClient(client_id, client_secret, port, redirect_url, browser_path)

# user_response = client.user.get(id='me')
# user = json.loads(user_response.content)
USER_ID = "me"
# print(user)
# print ('---')


# Test Function Declaration Zone
def list_user_channels():
    channels = json.loads(client.chat_channels.list().content)["channels"]
    print("=== All Channels ===")
    for channel in channels:
        print(channel)

def create_channel():
    cname = input("Provide a name for your new channel: ")
    ctype = input("""
    Provide a type for your new channel:
    1. Private & Invite only
    2. Private & People from same organization invited only
    3. Public
    0. exit
    """)
    if (ctype == "0"): return
    elif ctype in ["1", "2", "3"]:
        members = []
        while len(members) < 5:
            member = input("Provide a valid email address to invite members (type 'stop' to stop adding). Current members {}: ".format(len(members)+1))
            if(member.lower() == "stop"): break
            members.append({"email" : member})
        if(len(members)>0):
            print("Status Code: ", client.chat_channels.create_channel(name = cname, type = int(ctype), members = members).status_code)
            print("Channel created.")
        else:
            print("Status Code: ", client.chat_channels.create_channel(name = cname, type = int(ctype)).status_code)
            print("Channel created.")
    else:
        print("Please provide a valid input...")
        create_channel()


def get_channel():
    cid = input("Provide a valid channel ID to get channel: ")
    print("Working...")
    response = client.chat_channels.get_channel(channelId = cid)
    print("Status Code: ", response.status_code)
    print(response.content)

def update_channel():
    cid = input("Provide a valid channel ID to update channel: ")
    cname = input("Enter new channel name: ")
    response = client.chat_channels.update_channel(channelId = cid, name = cname)
    print("Status Code: ", response.status_code)
    if (response.status_code == 204):
        print("Channel updated.")
    elif (response.status_code == 200):
        print("No permission to update this channel.")
    else:
        print("Update channel failed.")

def delete_channel():
    cid = input("Provide a valid channel ID to delete channel: ")
    response = client.chat_channels.delete_channel(channelId = cid)
    print("Status Code: ", response.status_code)
    if (response.status_code == 204):
        print("Channel deleted.")
    elif (response.status_code == 200):
        print("No permission to update this channel.")
    else:
        print("Update channel failed.")

def list_channel_members():
    cid = input("Provide a valid channel ID to list current members: ")
    response = client.chat_channels.list_channel_members(channelId = cid)
    print("Status Code: ", response.status_code)
    members = json.loads(response.content)["members"]
    print("=== All Members ===")
    for member in members:
        print(member)

def invite_channel_members():
    cid = input("Provide a valid channel ID to invite new members: ")
    members = []
    while len(members) < 5:
        member = input("Provide valid email address to invite members (press 'stop' to stop). Currently member {}: ".format(len(members)+1))
        if(member.lower() == "stop"): break
        members.append({"email" : member})
    response = client.chat_channels.invite_channel_members(channelId = cid, members = members)
    print("Status Code: ", response.status_code)
    if (response.status_code == 201):
        print("Members invited to the channel.")
    elif (response.status_code == 200):
        print("No permission to invite channel members.")
    else:
        print("Invite Channel members failed.")

def join_channel():
    cid = input("Provide a valid channel ID of the channel that you want to join: ")
    response = client.chat_channels.join_channel(channelId = cid)
    print("Status Code: ", response.status_code)
    if (response.status_code == 201):
        print("Successfully joined the channel.")
    else:
        print("Join channel failed.")

def leave_channel():
    cid = input("Provide a valid channel ID of the channel that you want to leave: ")
    response = client.chat_channels.leave_channel(channelId = cid)
    print("Status Code: ", response.status_code)
    if (response.status_code == 204):
        print("Left channel successfully.")
    else:
        print("Leave channel failed.")

def remove_member():
    cid = input("Provide a valid channle ID of the channel to remove a member from: ")
    uid = input("Provide a valid member ID of the member to remove: ")
    response = client.chat_channels.remove_member(channelId = cid, memberId = uid)
    print("Status Code: ", response.status_code)
    if (response.status_code == 204):
        print("Member removed.")
    elif (response.status_code == 200):
        print("No permission to remove channel member.")
    else:
        print("Failed to remove member.")

def list_messages():
    option = input(
        """
        List messages:
        1. Between you and a contact
        2. In a chat channel
        0. Exit
        """
        )
    if option == "0": return
    elif option == "1":
        contact = input("Enter a contact email: ")
        response = client.chat_messages.list(user_id = USER_ID, to_contact = contact)
        print("Status Code: ", response.status_code)
        messages = json.loads(response.content)["messages"]
        print("=== All Messages ===")
        for message in messages:
            print(message)
    elif option == "2":
        channel = input("Enter a channel ID: ")
        response = client.chat_messages.list(user_id = USER_ID, to_channel = channel)
        print("Status Code: ", response.status_code)
        messages = json.loads(response.content)["messages"]
        print("=== All Messages ===")
        for message in messages:
            print(message)
    else:
        print("Pick from available options")
        list_messages()

def send_message():
    option = input(
        """
        Send a chat message to:
        1. A contact
        2. A channel
        0. Exit
        """
    )
    if option == "0": return
    elif option == "1":
        contact = input("Enter a contact email: ")
        message = input("Enter message: ")
        response = client.chat_messages.post(to_contact=contact, message=message)
        print("Status Code: ", response.status_code)
        if (response.status_code == 201):
            print("Message sent.")
        elif (response.status_code == 5301):
            print("Message sending failed.")
        elif (response.status_code == 200):
            print("This Zoom User is not the correct contact or a member of the channel.")
        else:
            print("Error sending message.")
    elif option == "2":
        channel = input("Enter a channel ID: ")
        message = input("Enter message: ")
        response = client.chat_messages.post(to_channel=channel, message=message)
        print("Status Code: ", response.status_code)
        if (response.status_code == 201):
            print("Message sent.")
        elif (response.status_code == 5301):
            print("Message sending failed.")
        elif (response.status_code == 200):
            print("This Zoom User is not the correct contact or a member of the channel.")
        else:
            print("Error sending message.")
    else:
        print("Pick from available options")
        send_message()

def update_message():
    option = input(
        """
        Edit a message sent to:
        1. A contact
        2. A channel
        0. Exit
        """
    )
    if option == "0": return
    elif option == "1":
        contact = input("Enter a contact email: ")
        messages = json.loads(client.chat_messages.list(user_id=USER_ID, to_contact=contact).content)["messages"]
        print("=== All Messages ===")
        for message in messages:
            print(message)
        messageId = input("Enter message ID to edit a message: ")
        message = input("Enter new message: ")
        response = client.chat_messages.update_message(messageId=messageId, message=message, to_contact=contact)
        print("Status Code: ", response.status_code, " ")
        if (response.status_code == 204):
            print("Message updated successfully.")
        elif (response.status_code == 200):
            print("This Zoom User is not the correct contact or a member of the channel.")
        elif (response.status_code == 300):
            print("This message does not exist: message ID")
        else:
            print("Error updating message.")
    elif option == "2":
        channel = input("Enter a channel ID: ")
        messages = json.loads(client.chat_messages.list(user_id=USER_ID, to_channel = channel).content)["messages"]
        print("=== All Messages ===")
        for message in messages:
            print(message)
        messageId = input("Enter message ID to edit your message: ")
        message = input("Enter new message: ")
        response = client.chat_messages.update_message(messageId=messageId, message=message, to_channel = channel)
        print("Status Code: ", response.status_code, " ")
        if (response.status_code == 204):
            print("Message updated successfully.")
        elif (response.status_code == 200):
            print("This Zoom User is not the correct contact or a member of the channel.")
        elif (response.status_code == 300):
            print("This message does not exist: message ID")
        else:
            print("Error updating message.")
    else:
        print("Pick from available options")
        update_message()

def delete_message():
    option = input(
        """
        Delete a message sent to:
        1. A contact
        2. A channel
        0. Exit
        """
    )
    if option == "0": return
    elif option == "1":
        contact = input("Enter a contact email: ")
        messages = json.loads(client.chat_messages.list(user_id=USER_ID, to_contact = contact).content)["messages"]
        print("=== All Messages ===\n")
        for message in messages:
            print(message)
        messageId = input("Enter message ID to delete a message: ")
        response = client.chat_messages.delete_message(messageId=messageId, to_contact=contact)
        print("Status Code: ", response.status_code, " ")
        if (response.status_code == 204):
            print("Message deleted.")
        elif (response.status_code == 200):
            print("The contact or the channel parameter provided is invalid.")
        elif (response.status_code == 300):
            print("This message does not exist: message ID")
        else:
            print("Error updating message.")
    elif option == "2":
        channel = input("Enter a channel ID: ")
        messages = json.loads(client.chat_messages.list(user_id=USER_ID, to_channel = channel).content)["messages"]
        print("=== All Messages ===\n")
        for message in messages:
            print(message)
        messageId = input("Enter message ID to delete a message: ")
        response = client.chat_messages.delete_message(messageId=messageId, to_channel=channel)
        print("Status Code: ", response.status_code, " ")
        if (response.status_code == 204):
            print("Message deleted.")
        elif (response.status_code == 200):
            print("The contact or the channel parameter provided is invalid.")
        elif (response.status_code == 300):
            print("This message does not exist: message ID")
        else:
            print("Error updating message.")
    else:
        print("Pick from available options")
        delete_message()

# Main Method
stop = False
while not stop:
    print(
        """
        ========== Channels ===========
        1. List User's Channels
        2. Create a Channel
        3. Get a Channel
        4. Update a Channel
        5. Delete a Channel
        6. List Channel Members
        7. Invite Channel Members
        8. Join a Channel
        9. Leave a Channel
        10. Remove a Member
        ========== Messages ===========
        11. List User's Chat Messages
        12. Send a Chat Messages
        13. Update a Message
        14. Delete a Message
        0. Exit
        """
    )
    option = input("Please type in your command with a valid numeric index(0 ~ 14): ")
    if(option == "0"):
        stop = True
        break
    elif(option == "1"): list_user_channels()
    elif(option == "2"): create_channel()
    elif(option == "3"): get_channel()
    elif(option == "4"): update_channel()
    elif(option == "5"): delete_channel()
    elif(option == "6"): list_channel_members()
    elif(option == "7"): invite_channel_members()
    elif(option == "8"): join_channel()
    elif(option == "9"): leave_channel()
    elif(option == "10"): remove_member()
    elif(option == "11"): list_messages()
    elif(option == "12"): send_message()
    elif(option == "13"): update_message()
    elif(option == "14"): delete_message()
    else: print("Please provide a valid input...\n")
    input("Press any input to continue... ")