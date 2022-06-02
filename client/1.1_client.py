from ast import While
from cgitb import reset
from functools import cache
import pathlib
import socket
import os.path
from os import path
from time import sleep
from urllib import request

cache={}

def Main():
        f=open('test.txt', 'r')
        lines = f.read().splitlines()
        i = 0
        host = 0
        port = 0
        while i < len(lines):
            line = lines[i].split(" ")
            host = line[2]
            port  = 80
            if len(line) > 2:
                port = line[3]
                if line[1][0] != "/":
                    line[1] = "/" + line[1]
            request = line[0] + " " + line[1] + " " + "HTTP/1.1\r\n" + "Host: " + host + ":" + port + "\r\n\r\n"
            fileData = request
            if line[0] == "POST":
                    if(line[1].strip('/').lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
                        f = open(line[1].strip('/'), "rb")
                        dataF = f.read()
                    else:
                        f = open(line[1].strip('/'), "r")
                        dataF = f.read()
                    fileData = request + dataF
                    f.close()
            lines[i] = fileData.encode()
            i= i +1
            print(lines)
        try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, int(port)))
                    
                    for line in lines: 
                        print(" CONNECTED ")
                        s.sendall(line)
                        print(line)
                        temp = line.decode().split("\r\n\r\n")
                        line1 = temp[0].split(" ")
                        if line1[0] == 'POST':
                            response = b""
                            while True:
                                chunk = s.recv(1024)
                                response = response + chunk
                                if len(chunk) < 1024 or not chunk:     # No more data received, quitting
                                    break  
                            print("\nResponse:\n" + response.decode())
                        elif line1[0] == 'GET':
                            print("\nRequest:\n"+ line.decode())                         
                            response = b""
                            while True:
                                chunk = s.recv(1024)
                                response = response + chunk
                                if len(chunk) < 1024:     # No more data received, quitting
                                    break
                            if(line1[1].strip('/').lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
                                fs = open(os.path.join(pathlib.Path(__file__).parent.resolve(), line1[1].strip("/")),"wb")
                                data = response.split(b'\r\n\r\n')
                                fs.write(data[1])
                                print("Response:\n" + data[0].decode())
                            else:
                                print(line1[1])
                                test=response.decode().split(" ")
                                if test[1] == '200':   
                                    # print(test)
                                    fs = open(os.path.join(pathlib.Path(__file__).parent.resolve(), line1[1].strip("/")),"w+")
                                    j = 1
                                    data = response.decode().split("\r\n\r\n")
                                    # print(data)
                                    l = len(data)
                                    while j < l:
                                        fs.writelines(data[j])
                                        j = j+1     
                                    fs.close()
                                    print("Response:\n" + response.decode()) 
                                else:
                                    print("Response:\n" + response.decode())
                            #print("\nResponse:\n" + response.decode() + " YAAY")  
                    sleep(15)
        except Exception as e:
                print(e)
                print("couldn't connect to this server") 
                print("\n") 


if __name__ == '__main__':
    Main()