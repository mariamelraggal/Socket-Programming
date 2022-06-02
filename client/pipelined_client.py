from ast import While
from cgitb import reset
from functools import cache
import pathlib
import socket
import os.path
from os import path
from time import sleep
from urllib import request

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
            fileData = request.encode()
            if line[0] == "POST":
                if(line[1].strip('/').lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))):
                    f = open(line[1].strip('/'), "rb")
                    dataF = f.read()
                else:
                    f = open(line[1].strip('/'), "r")
                    dataF = f.read().encode()
                fileData = request.encode() + dataF
                f.close()
            lines[i] = fileData
            i= i + 1
        print(lines)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, int(port)))
            print(" cONNECTED ")
            for line in lines: 
                s.sendall(line)
            while i != 0:
                response = b""
                while True:
                    chunk = s.recv(1024)
                    response = response + chunk
                    if len(chunk) < 1024 or not chunk:     # No more data received, quitting
                        break
                response_splitted = response
                #print(response_splitted)
                if response_splitted[1] is None:
                    response_splitted = response.split(b"\r\n\r\n")
                    print(" LENGTH  = 2")
                    print("Response: \n" + response_splitted[0].decode())
                    i = i - 1
                else:
                    i = i - 1
                    print(response_splitted.split(b"\r\n\r\n")[0].split()[1].decode() + "  S.dbc;OBOCVJ;alca")
                    if response_splitted.split(b"\r\n\r\n")[0].split()[1] == b'200':
                            # incase of image
                            try:
                                data = response_splitted.split(b"\r\n\r\n")[1].decode()
                                print("decoding text")
                                fs = open("textFile.txt","w+")
                            except:
                                print("imageeee")
                                fs = open("img.png","wb")
                                data = response_splitted.split(b'\r\n\r\n')[1]  
                            fs.write(data)
                            print("Response: \n" + response_splitted.split(b"\r\n\r\n")[0].decode() + "\n")
                            fs.close()
                    else:
                            print("ELSEEE 404")
                            print("Response:\n" + response_splitted.decode())
                sleep(15)



if __name__ == '__main__':
    Main()