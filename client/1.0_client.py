from ast import While
from functools import cache
import pathlib
import socket
import os.path
from os import path
import json
import sys

cache={}
def Main():
        f=open(sys.argv[1], 'r')
        lines = f.read().splitlines()
        # reading the file and getting each line of command
        for line in lines:
            line1 = line.split(' ')
            host = line1[2]
            port = 80
            if len(line1) > 2:
                port = line1[3]   
            if line1[1][0] != "/" :
                line1[1] = "/" + line1[1]

            request = line1[0] + " "+ line1[1] + " " + "HTTP/1.0\r\n" + "Host: " + host + ":" + port +"\r\n\r\n"
            # Checking Cache!
            flag=0
            for key in cache.keys():
                if key == request:
                    print("cached request: ")                    
                    print(key)
                    print("cached response: ")
                    for x in range(len(cache[key])):
                        print(cache[key][x] + " ")
                    flag=1
            if flag==1:
                continue
            # End of Caching!
            
            # in case of post get the data of the file
            if line1[0] == "POST":
            # in case the file is a picture
                if(line1[1].strip('/').lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
                    f = open(line1[1].strip('/'), "rb")
                    dataF = f.read()
                # in case the file is a normal file
                else:
                    f = open(line1[1].strip('/'), "r")
                    dataF = f.read().encode()
                fileData = request.encode() + dataF
                f.close() 
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    # connect with the server
                    s.connect((host, int(port)))
                    print("\nRequest:\n"+request) 
                    if line1[0] == 'POST':
                        s.sendall(fileData)
                        response = b""
                        # recieving response from the server
                        while True:
                            chunk = s.recv(1024)
                            response = response + chunk
                            if len(chunk) < 1024 or not chunk:     # No more data received, quitting
                                break
                            # save in the cache
                        cachePost = response.decode()
                        cache[request] = [cachePost]
                        print("Response: \n" + cachePost)
                    # in case of get
                    elif line1[0] == 'GET':
                        s.sendall(request.encode())
                        response = b""
                        # recieving response from the server
                        while True:
                            chunk = s.recv(1024)
                            response = response + chunk
                            if len(chunk) < 1024 or not chunk:     # No more data received, quitting
                                break
                        # response 200 OK
                        # seperating header from data
                        if response.split(b"\r\n\r\n")[0].split()[1] == b'200':
                            # incase of image
                            if(line1[1].strip('/').lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
                                fs = open(os.path.join(pathlib.Path(__file__).parent.resolve(), line1[1].strip("/")),"wb")
                                data = response.split(b'\r\n\r\n')[1]
                                cacheDp = line1[1].strip("/")
                            # write the response data in a file
                            else:
                                fs = open(os.path.join(pathlib.Path(__file__).parent.resolve(), line1[1].strip("/")),"w+")
                                data = response.split(b"\r\n\r\n")[1].decode()
                                cacheDp = data 
                            fs.write(data)
                            # saving in the cache
                            cache[request] = [response.split(b"\r\n\r\n")[0].decode(), cacheDp]
                            print("Response: \n" + response.split(b"\r\n\r\n")[0].decode() + "\n")
                            fs.close()
                        else:
                            print("Response:\n" + response.decode())
                            cache[request] = [response.split(b"\r\n\r\n")[0].decode()]
            except:
                print("couldn't connect to this server")
                print("\n") 

if __name__ == '__main__':
    Main()