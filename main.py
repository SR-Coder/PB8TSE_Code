# main.py -- put your code here!
# from server.classes.ServerClass import HttpServer
# from server.ViewHelper import View, redirect, jsonify
# from server.controlers.main_controller import toggle, getValue, led
from server.helpers import networkConnection
# from server.helpers.jsonSaver import saveJSON
import json, gc, ujson
import socket, time, select, re, math

_DATAFRAME = 1024

def reqHandler(req: str):
    print("in reqHandler", req)
    return '''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>SimpleServer</title><link rel="stylesheet" href="../Static/style.css"></head><body><div class="header"><h1>Welcome to Simple Server</h1><a href="/postTest">Try some post data</a></div><div class="main"><form action="/turnOn" method="POST"><button id="ledBtn">Turn Led On</button></form></div><script src="/Static/main.js"></script></body></html>'''

def getContentLength(data):
    dataArr = data.split('\r')
    length = ""
    for entry in dataArr:
        if "Content-Length" in entry:
            length = entry.split(': ')[1]
            length = int(length)-_DATAFRAME
            if length < 0:
                return 0
            else: return math.ceil(length/_DATAFRAME)
    
    return 0

def getReqType(data):
    dataArr = data.split('\r')
    reqType = dataArr[0].split(' /')[0]
    return reqType
    

def run_server():
    s = socket.socket()
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 80))

    s.listen(1)


    print("Running....")

    while True:
        
        cSock, cAddr = s.accept()
        cSock.setblocking(False)
        req = cSock.read(_DATAFRAME)
        reqSize = None
        if  req:
            head = req.decode('utf-8')
            reqType = getReqType(head)
            print(type(reqType), len(reqType))
            if reqType == 'POST':
                bytesRemaining = getContentLength(head)
                reqSize = bytesRemaining
                while bytesRemaining > 0:
                    temp = cSock.read(_DATAFRAME)
                    req += temp
                    bytesRemaining -= 1
            print("The payload size: ", reqSize)
            res = reqHandler(req.decode('utf-8'))
            cSock.sendall(res)
        cSock.close()






run_server()