from tkinter import *
import socket
import threading
from datetime import datetime

current_time = datetime.now().strftime("%I:%M %p")


combined_string = f'server started at {current_time}\n'


windows = Tk()
windows.title("YEGNA-Chat")

PORT = 2104
# socket.gethostbyname(socket.gethostname())  # '127.0.0.1'  #192.168.50.147
HOST = '192.168.94.179'
print(HOST)
disMessage = '!disconnect'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
clients_online = []


windows.minsize(width=300, height=400)
labelONe = Label(windows, text='CHAT SEAMLESSLY !!!', font=(
    'times new roman', 11, 'bold'), fg='grey').pack(side='top')
label1 = Label(windows, text='', font=('times new roman', 11), fg='grey')
label1.pack(side='top')


def start():
    server.listen()
    label1['text'] += f"LISTENING ON {HOST}"

    while True:
        connection, address = server.accept()

        label1['text'] += f"connected to {address}"
        thread = threading.Thread(target=handleClient, args=(connection,))
        thread.start()


def send_to_client(client, message):
    client.send(message.encode('utf-8'))


def send_to_all(message):
    for user in clients_online:
        try:
            send_to_client(user[1], message)
        except:
            continue


def accept_message(client, userName):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
        except:
            message = f'{userName} left the chat'
            send_to_all(message)
            break
        else:
            message = f'{userName}: {msg}'
            send_to_all(message)


def handleClient(con):
    send_to_client(con, combined_string)
    connected = True
    while connected:
        userName = con.recv(1024).decode('utf-8')
        if userName:
            clients_online.append([userName, con])
            note = f'{userName} joined chat'
            send_to_all(note)

            break

        else:
            label1['text'] = 'empty User Name'

    threading.Thread(target=accept_message, args=(con, userName)).start()


def start_server():
    thread = threading.Thread(target=start)
    thread.start()


start_server()
windows.mainloop()
