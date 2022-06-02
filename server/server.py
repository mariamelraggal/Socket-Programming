from logging import exception
import pathlib
from pickle import FALSE
import socket
import os, signal
import sys
import time
import multiprocessing
import re
# import thread module
from _thread import *
import threading
from unittest.mock import DEFAULT

print_lock = threading.Lock()
GLOBAL_COUNT_CLIENTS = 0

# thread function
def threaded(c,time,clients):
    flag = 0
    data = b''
    try:
        while True:

                # looping to recieve the data from the client
                while True:
                    data33 = c.recv(1024)
                    data = data + data33
                    if len(data33) < 1024 or not data33:
                        break
                # data is still available
                if data:
                    # splitting the recieved data into arrays that start with post/get
                    indexesPost = [m.start() for m in re.finditer(b'POST ', data)]
                    indexesGet = [m.start() for m in re.finditer(b'GET ', data)]
                    indexes = indexesPost + indexesGet
                    indexes.sort()
                    requestsData11 = list()
                    for i in range (len(indexes)):
                        start = indexes[i]
                        if i == len(indexes)-1:
                            requestsData11.append(data[start:])
                        else:
                            end = indexes[i+1]
                            requestsData11.append(data[start:end])
                    # looping on each requests
                    for req in requestsData11:  
                        data = req
                        x = data.split(b'\r\n')[0].decode().split()

                        if x[2] == "HTTP/1.1" and flag == 0:
                            flag = 1
                        # WE SHOULD PRINT THE REQUEST FROM CLIENT
                        print("Request:\n" + data.split(b'\r\n\r\n')[0].decode())
                        # in case of get request
                        if x[0] == 'GET':
                            try:
                                # check if requested file is a picture
                                if(x[1].strip('/').lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
                                    f = open(os.path.join(pathlib.Path(__file__).parent.resolve(), x[1].strip("/")), "rb")
                                    data2 = f.read()
                                # check if requested file is a normal file
                                else:
                                    f = open(os.path.join(pathlib.Path(__file__).parent.resolve(), x[1].strip("/")), "r") # read file content
                                    data2 = f.read().encode()
                                # check if request is http 1.1 or 1.0
                                if x[2] == "HTTP/1.1":
                                    msg = 'HTTP/1.1 200 OK\r\n\r\n'.encode()
                                else :
                                    msg = 'HTTP/1.0 200 OK\r\n\r\n'.encode()
                                # concatenate the message data with the header
                                msg = msg + data2
                                f.close()
                            except Exception as e :
                                # file is not found
                                if x[2] == "HTTP/1.1":
                                    msg=b'HTTP/1.1 404 Not Found\r\n\r\n'  
                                else :
                                    msg=b'HTTP/1.0 404 Not Found\r\n\r\n'
                        # in case of post requests
                        elif x[0] == 'POST':
                            # in case of a picture file
                            if(x[1].strip('/').lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
                                f = open(os.path.join(pathlib.Path(__file__).parent.resolve(), x[1].strip("/")), "wb")
                                fileData = data.split(b'\r\n\r\n')[1]
                            # in case of a normal file
                            else:
                                f = open(os.path.join(pathlib.Path(__file__).parent.resolve(), x[1].strip("/")), "w+")
                                fileData = data.split(b'\r\n\r\n')[1].decode()
                            f.write(fileData)
                            f.close()
                            if x[2] == "HTTP/1.1":
                                msg='HTTP/1.1 200 OK\r\n\r\n'
                            else :
                                msg='HTTP/1.0 200 OK\r\n\r\n'
                            print("\nResponse:\n" + msg)
                            msg = msg.encode()
                        c.sendall(msg)
                    if flag == 0:
                        # lock released on exit
                        print_lock.release()
                        break      
                    data=b''
                    # connection closed
                else:
                    if flag == 0:
                        # lock released on exit
                        print_lock.release()
                        print("\n")
                        break
    except Exception as e:
        print_lock.release()
        print(e)
        print("exception\n")
        exception_type, exception_object, exception_traceback = sys.exc_info()
        line = exception_traceback.tb_lineno
        print(line)
        #break
    global GLOBAL_COUNT_CLIENTS
    GLOBAL_COUNT_CLIENTS = GLOBAL_COUNT_CLIENTS - 1
    c.close()

def Main():
    host = "127.0.0.1"
    DEFAULT_TIME = 10
    port = 65432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
    #s.setblocking(0)
    
    # put the socket into listening mode
    
    print("socket is listening")
    # a forever loop until client wants to exit
    while True:
        try:
            s.listen()
            print("LISTEN ---------------------")
            # establish connection with client
            c, addr = s.accept()
            # the number of clients connected
            global GLOBAL_COUNT_CLIENTS 
            GLOBAL_COUNT_CLIENTS = GLOBAL_COUNT_CLIENTS + 1
            time = int(DEFAULT_TIME / GLOBAL_COUNT_CLIENTS )
            c.settimeout(time)
            # lock acquired by client
            print_lock.acquire()
            print('Connected to :', addr[0], ':', addr[1])
            thread = threading.Thread(target = threaded, args = (c,time,GLOBAL_COUNT_CLIENTS,))
            # Start a new thread and return its identifier
            #start_new_thread(threaded, (c,time,GLOBAL_COUNT_CLIENTS,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            line = exception_traceback.tb_lineno
            print(line)
            print(e)
            c.close()

 
 
if __name__ == '__main__':
    Main()