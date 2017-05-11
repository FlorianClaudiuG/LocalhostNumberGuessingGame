import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("\t\tWELCOME to the NUMBER GUESSING GAME!\n")
print("Your goal is to guess a number between 1 and 30!\n")
try:
    s.connect(("127.0.0.1", 4000))
    print("Connecting to:", "127.0.0.1, 4000\n")
except:
    print("Could not connect to server.")
else:
    try:
        s.send("Hello\r\n".encode())
        message = s.recv(80).decode()
        if message == "Greetings\r\n":
            s.send("Game\r\n".encode())
        message = s.recv(80).decode()
        if message == "Ready\r\n":
            print("We've connected you to your host! Your game has begun!\n")
    except:
        print("There are issues with the server. Connection has been terminated.\n")
        s.close()
    else:
        guessed = False
        while not guessed:
            guess = input("Guess a number: ")
            guessMessage = "My Guess is: " + str(guess) + "\r\n"
            try:
                s.send(guessMessage.encode())
                message = s.recv(80).decode()
            except:
                print("There are issues with the server. Connection has been terminated.\n")
                s.close()
                break
            if message == "Far\r\n":
                print("Your guess was far! Try again!")
            elif message == "Close\r\n":
                print("So close! Keep it up!")
            elif message == "Correct\r\n":
                print("You got it! Congratulations, you win! Server connection will now be terminated.")
                guessed = True
                s.close()

    
