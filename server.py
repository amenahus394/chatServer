import socket
import threading
import sys


arguments = sys.argv
serverPort = int(arguments[1])
password = arguments[2]


active_clients = [] #list of all connected users 
active_names = []



#function to listen for upcoming messages from a client
def client_handler(serverSocket):
    
    #while True:
    try:
        message = serverSocket.recv(1024).decode('utf-8')

        message = message.split('\n')

        
        enteredpassword = message[0]
        username = message[1]


        if password == enteredpassword and not (username in active_names) and not (" " in username):
            serverSocket.send('Welcome!\n'.encode())

            for x in active_clients:
                x.send((username + " joined the chatroom\n").encode())
            print((username + " joined the chatroom").strip())
            active_clients.append(serverSocket)
            active_names.append(username)
        else: 
            serverSocket.close()
        
        while True:
            received = serverSocket.recv(1024).decode('utf-8').strip()
            if received == ':Exit' or received == '':
                active_clients.remove(serverSocket)
                active_names.remove(username)

                print((username + ' left the chatroom').strip())

                for y in active_clients:
                    y.send((username + ' left the chatroom\n').encode())
                

            elif (received.split(" ")[0] == ":dm"):
                dir = received.split(" ", 2)
                msg = (f"{username} -> {dir[1]}: {dir[2]}\n")

                counter1 = 0
                for a in active_names: 
                    if (a == dir[1]):
                        break
                    else:
                        counter1 += 1
                    
                
               
                active_clients[counter1].sendall(msg.encode())
                serverSocket.sendall(msg.encode())


                print(msg.strip())

                
            else:
                print (username + ": " + received)
                for z in active_clients:
                    z.send((username + ": " + received + "\n").encode())
    except:
        serverSocket.close()
        exit(0)


def main(): 
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serverSocket.bind(('', serverPort))
        print('Server started on port ' + str(serverPort) + '. Accepting connections...')
    except:
        print(f"Unable to bind to host and port {serverPort}")

    
    serverSocket.listen(20)


        #will keep listening to client connections
    while True:        
        clientSocket, address = serverSocket.accept()
        #print({address[0]}, {address})

        threading.Thread(target = client_handler, args = (clientSocket, )).start()

        
if __name__ == '__main__':
    main()



