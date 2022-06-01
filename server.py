# import required modules
import socket
import threading

HOST = '127.0.0.1'
PORT = 5000
LISTENER_LIMIT = 5
active_clients = [] # list of all currently connected client

# function to listen for upcoming messages from client
def listen_for_messages(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + ':' + message
            send_messages_to_all(final_msg)
        else:
            print(f"No messages from client {username}")


# function to send message to single client
def send_message_to_client(client, message):
    client.sendall(message.encode())


# function to send any new messages to all client that
# are connected to the server
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)


# function to handle client
def client_handler(client):
    # server will listen for client messages that will
    # contain the username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "[SERVER]:" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()


# main function
def main():
    # create the socket class object
    # AF_INET: use IPv4 addresses
    # SOCK_STREAM: use TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # create a try catch block
    try:
        # provide an address in form of HOST IP and POST to the server
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST}:{PORT}")
    except:
        print(f"Unable to connect host {HOST} to port {PORT}")

    # set server limit
    server.listen(LISTENER_LIMIT)

    # this while loop keep listening to client connections
    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]}  {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()
