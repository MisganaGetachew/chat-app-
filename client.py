from tkinter import *
import sqlite3
import socket
import threading

con = sqlite3.connect('userdata.db')

# con.execute('''CREATE TABLE users(
# user_n, password
# )''')

PORT = 2104
# HOST = '127.0.0.1'
format = 'utf-8'
Profile = []

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
 
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


def register():
    uname = username_entry.get()
    pwr =  password_entry.get()
    cursor = con.execute("SELECT * FROM users WHERE user_n = ?", (uname,))
    if cursor.fetchone() is not None:
        message.set("Invalid Username or already taken")
    else:
        if uname == '' or pwr=='':
            message.set("fill the empty field!!!")
        else:
            con.execute('INSERT INTO users(user_n, password) VALUES (?, ?)', (uname, pwr))
            chatroom()

def login():
    uname = username_entry.get()
    pwr =  password_entry.get()
    cursor = con.execute("SELECT * FROM users WHERE user_n = ? AND password = ?", (uname, pwr))
    if cursor.fetchone() is None:
        message.set("Invalid user name or password")
    else:
        if uname == '' or pwr=='':
            message.set("fill the empty field!!!")
        else:
            chatroom()



def chatroom():
    HOST = ipAddress.get()
    connected = True
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except:
        connected = False

  
    def send(msg):
        message = msg.encode('utf-8')
        client.sendall(message)
    
 
    profile = username_entry.get()
    log.destroy()
    root = Tk()
    root.title("Chatroom")
    lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="YEGNA-Chat", font=FONT_BOLD, pady=10, width=20, height=1).grid(row=0)
    lable2 = Label(root, text="", font=('times new roman', 13, 'bold'   ), pady=10)
    lable2.grid(row=1)
    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    txt.grid(row=2, column=0, columnspan=2)
    
    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)
    
    entry = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    entry.grid(row=3, column=0)

    def btn_clicked():
        sended = entry.get()
        entry.delete(0, END)
        threading.Thread(target=send, args=(sended,)).start()
    

    send_button = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=btn_clicked)
    send_button.grid(row=3, column=1)

    # connection setup
    if connected:
        lable2['text'] = f'PROFILE : {profile.upper()}'
        send(profile)
        
    else:
        lable2['text'] = 'oops server is not responding!'
        send_button['state'] = DISABLED


        
    def btn_clicked():
        sended = entry.get()
        entry.delete(0, END)
        threading.Thread(target=send, args=(sended,)).start()
    



    def show_message():
        while True:  
                try:
                    msg = client.recv(1024).decode('utf-8') 
                except(RuntimeError):
                    # print('left the room')
                    send_button['state'] = DISABLED
                    break
                except(ConnectionResetError):
                    lable2['text']  = 'failed to connect to the server!'
                    send_button['state'] = DISABLED
                    break
                except(ConnectionAbortedError, OSError):
                        # print('left the room')
                        break
                #     label1['text']  = 'failed to connect to the server!'
                #     bt['state'] = DISABLED
                #     break
                else:
                        txt.insert('end', f'\n {msg} ' ) 
        
    def start_showing():
     thread = threading.Thread(target=show_message)
     thread.start()

                

    start_showing()
    root.resizable(FALSE, FALSE)
    root.mainloop()

def sign_up(btn, sign, user, pas):
    btn.destroy()
    sign.destroy()
    user.delete(0, END)
    pas.delete(0, END)

    new_button = Button(frame, text="Register", font=FONT_BOLD, bg=BG_COLOR, fg=BG_GRAY, underline=-1, command=register)
    new_button.grid(row=4, columnspan=2, pady=20)
   
log = Tk()
log.title('Chatroom')
log.geometry('400x500')
log.configure(bg=BG_COLOR)

log.rowconfigure(0, weight=1)
log.columnconfigure(0, weight=1)

frame = Frame(log, bg=BG_COLOR,)
frame.grid()

frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1) 

logiin = Label(frame, text="YEGNA-Chat login form", font=FONT_BOLD, bg=BG_COLOR, fg=BG_GRAY).grid(row=0, columnspan=2, pady=20)

username_label = Label(frame, text="Username  ", font=FONT_BOLD, bg=BG_COLOR, fg=BG_GRAY).grid(row=1, column=0)
username_entry = Entry(frame, font=FONT_BOLD)
username_entry.grid(row=1, column=1, pady=10)

password_label = Label(frame, text="Password  ", font=FONT_BOLD, bg=BG_COLOR, fg=BG_GRAY).grid(row=2, column=0)
password_entry = Entry(frame, font=FONT_BOLD, show="*")
password_entry.grid(row=2, column=1, pady=10)
ipAddress = Label(frame, text="local network IP", font=FONT_BOLD, bg=BG_COLOR, fg=BG_GRAY).grid(row=6, column=0)
ipAddress = Entry(frame, font=FONT_BOLD)
ipAddress.grid(row=6, column=1, pady=10)


message = StringVar()
check = Label(frame, text=" check ", bg=BG_COLOR, fg=BG_GRAY, textvariable=message)
check.grid(row=3, columnspan=2)

login_button = Button(frame, text="Login", font=FONT_BOLD, bg=BG_COLOR, fg=BG_GRAY, underline=-1, command=login)
login_button.grid(row=4, columnspan=2, pady=20)

sign_button = Button(frame, text="Create new account", font=FONT_BOLD, bg=BG_COLOR, fg=BG_GRAY, 
                     command= lambda: sign_up(login_button, sign_button, password_entry, username_entry))
sign_button.grid(row=5, columnspan=2, pady=30)

log.mainloop()

con.commit()
con.close()
