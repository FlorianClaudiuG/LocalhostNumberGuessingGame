import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("\t\tWELCOME, ADMIN!\n")
print("Connecting to:", "127.0.0.1, 4001\n")

try:
    s.connect(("127.0.0.1", 4001))
except:
    print("There are issues with the server. Connection has been terminated.\n")
    s.close()
else:
    try:
        s.send("Hello\r\n".encode())
        message = s.recv(80).decode()
        if message == "Admin-Greetings\r\n":
            s.send("Who\r\n".encode())
        #receive list of players
        message = s.recv(800).decode()
    except:
        print("There are issues with the server. Connection has been terminated.\n")
    else:
        if message == "\r\n":
            print("There are no players on the server.")
        else:
            print("The players currently playing are:\n")
            print(message)

    s.close()
