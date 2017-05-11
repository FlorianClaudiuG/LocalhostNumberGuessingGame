import socket
import random
import threading
import select

def HandleClient (conn, addr):
    try:
        message = conn.recv(80).decode()
        if message == "Hello\r\n":
            conn.send("Greetings\r\n".encode())
        message = conn.recv(80).decode()
        if message == "Game\r\n":
            conn.send("Ready\r\n".encode())
    except:
        socks.remove(conn)
        conn.close()
    else:
        connections.append(addr)
        
        RunGame(conn)
        
        connections.remove(addr)
        socks.remove(conn)
        conn.close()

def HandleAdmin (conn, addr):
    try:
        message = conn.recv(80).decode()
        if message == "Hello\r\n":
            conn.send("Admin-Greetings\r\n".encode())
            message = conn.recv(80).decode()
        if message == "Who\r\n":
            message = PrepareListOfPlayers(connections)
            conn.send(message.encode())
    except:
        socks.remove(conn)
        conn.close()
    else:
        socks.remove(conn)
        conn.close()

#Method that runs the number guessing game for the client passed in.
def RunGame(conn):
    answer = random.randrange(1, 31)
    guessed = False
    while not guessed:
        ## Wait for guess to come from the client.
        try:
            message = conn.recv(80).decode()
        except:
            break
        ## Take the number out of the 'My guess is: <int>' string.
        split = message.split(" ")
        guess = split[3]
        ## Try converting it to int. If everything is ok, operate with it.
        try:
            guess = int(guess)
        except ValueError:
            ## If it's not an int, send back Far.
            conn.send("Far\r\n".encode())
        else:
            ## If no error was caught, check how close it is to the answer
            ## and communicate with the client.
            proximity = abs(guess - answer)
            if proximity == 0:
                conn.send("Correct\r\n".encode())
                guessed = True
            elif proximity < 3:
                conn.send("Close\r\n".encode())
            else:
                conn.send("Far\r\n".encode())

#Method that creates and formats the string that represents the list of players to send to the admin.
def PrepareListOfPlayers (listOfPlayers):
    message = ""
    #Check if list is empty
    if not listOfPlayers:
        message = "\r\n"
    else:
        for element in listOfPlayers:
            address = str(element).strip('()')
            split = address.split(',')
            ip = split[0].strip('\'')
            port = split[1]
            line = ip + port + "\r\n"
            message = message + line
    return message

TCP_IP = "127.0.0.1"
TCP_PORT = 4000
TCP_ADMIN_PORT = 4001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
a.bind((TCP_IP, TCP_ADMIN_PORT))
a.listen(5)

#List of connections.
socks = []
socks.append(s)
socks.append(a)

#List of connected clients' addresses
connections = []

while True:
    #Look for reading activity on any socket.
    (inputs, outputs, errors) = select.select(socks, [], [])
    #Create a thread for each socket and handle it accordingly.
    for i in inputs:
        if (i == s):
            (conn, addr) = s.accept()
            t = threading.Thread(target = HandleClient, args = (conn, addr))
            t.start()
            socks.append(conn)
        elif (i == a):
            (conn, addr) = a.accept()
            t = threading.Thread(target = HandleAdmin, args = (conn, addr))
            t.start()
            socks.append(conn)        
        
        
    
    

    
