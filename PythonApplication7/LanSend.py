import socket        
import pickle
import json
      
 # Import socket module
soc1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc1.connect(( '192.168.137.3',12345))
#soc1.send('WILL SEND')
       # Create a socket object
 # Get local machine nam    ;        # Reserve a port for your service.
#s.connect((host, port))]

def send_dron(stri):
    global soc1
    soc1.send(str(stri))
def send_letter(char_seq):
    global soc1
    message = json.dumps(char_seq)
    soc1.send(message)   
def close_port():
    global soc1
    soc1.close()

        