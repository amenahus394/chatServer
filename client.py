import socket
import threading
import sys
from time import *
import os




arguments = sys.argv
serverName = arguments[1]
serverPort = int(arguments[2])
password = arguments[3]
nickname = arguments[4]


def receive_messages_socket(client):

    while True:
      #  try:
        message1 = client.recv(1024).decode('utf-8') # no strip here
        if message1 != '':
          print(message1)
        else:
            os._exit(1)
       # except:
           # print("couldnt connect with port")
            #clientSocket.close()
            #exit(0)


def send_messages(client):
    while True:
        message = input('')
        if (message.strip() == ':Exit'):
            client.send((":Exit\n").encode())
            client.close()
            exit(0)
        elif (message.strip()== ':)'):
            client.send(("[feeling happy]\n").encode())
        elif (message.strip() == ':('):
            client.send(("[feeling sad]\n").encode())
        elif (message.strip() == ':mytime'):
            datetime = strftime("It's %H:%M on %a, %d %b, %Y.\n", gmtime())
            client.send(datetime.encode())
    
        else:
            try:
                client.send((message + "\n").encode())
            
            except ConnectionResetError:
                print("the message did not send")
                exit(1)
            except (ConnectionAbortedError, IOError):
                exit(0)



def main():
    #creating client object
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    #connect to the server
    clientSocket.connect((serverName, serverPort))
        
    print(f"Connecting to {serverName} on port {serverPort}...")

    try:
        clientSocket.send((f'{password}\n').encode())
        clientSocket.send((f'{nickname}\n').encode())
        message = clientSocket.recv(1024).decode()


    except:
        print("Error with encoding and receiving preliminary message.")

    if (message == "Welcome!\n"):
        print(message.strip())

    
        threading.Thread(target = send_messages, args = (clientSocket,)).start()
        try:
            receive_messages_socket(clientSocket)
        except:
            clientSocket.close()
            exit(0)
    else:
       print(message)


if __name__ == '__main__':
    main()




    
    















