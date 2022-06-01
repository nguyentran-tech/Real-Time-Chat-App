# import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000

LARGE_FONT = ("Roboto", 14)
MEDIUM_FONT = ("Roboto", 12)
SMALL_FONT = ("Roboto", 10)

# create a socket object
# AF_INET: use IPv4 addresses
# SOCK_STREAM: use TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    # try except block
    try:
        # connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST}:{PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("No message", "Message cannot be empty")

root = tk.Tk()
root.geometry("600x800")
root.title("Real Time Chat App")
root.resizable(False, False)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=6)
root.rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg='#7FB5FF')
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=600, bg='#C4DDFF')
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg='#FEE2C5')
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Type in your username: ", font=LARGE_FONT, bg='#7FB5FF', fg='#fff')
username_label.pack(side=tk.LEFT, padx=20)

username_textbox = tk.Entry(top_frame, font=MEDIUM_FONT, bg='#C4DDFF', fg='#035397', width=20)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Let's Chat", font=SMALL_FONT, bg='#035397', fg='#fff', command=connect, width=10)
username_button.pack(side=tk.LEFT, padx=40)

message_textbox = tk.Entry(bottom_frame, font=MEDIUM_FONT, bg='#C4DDFF', fg='#035397', width=45)
message_textbox.pack(side=tk.LEFT, padx=30)

message_button = tk.Button(bottom_frame, text="Send", font=SMALL_FONT, bg='#035397', fg='#fff', command=send_message, width=10)
message_button.pack(side=tk.LEFT, padx=5)

message_box = scrolledtext.ScrolledText(middle_frame, font=MEDIUM_FONT, bg='#C4DDFF', fg='#035397', width=70, height=35)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split(":")[0]
            content = message.split(":")[1]
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            add_message(f"[{date_now}] {username}: {content}")
        else:
            messagebox.showerror("Error", "No messages received from client")

# main function
def main():
    root.mainloop()

if __name__ == '__main__':
    main()