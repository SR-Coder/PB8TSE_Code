# main.py -- put your code here!
from server.classes.ServerClass import HttpServer
from server.ViewHelper import View, redirect, jsonify
from server.controlers.main_controller import toggle, getValue, led
from server.helpers import networkConnection
import json, gc

server = HttpServer("0.0.0.0", 80, False)


gc.enable()

# ADD ROUTES HERE -->
# DISPLAY ROUTES
@server.route("/")
def Index():
    return View("Index")

@server.route("/postTest")
def PostTest():
    return View("PostTest")

@server.route('/switch')
def Switch():
    return View("Switch")

# ACTION ROUTES

@server.route("/goback")
def goBack():
    return redirect("Index", server)

@server.route("/turnOn")
def turnOn(data):
    toggle()
    return redirect("Index", server)

@server.route("/submitPostData")
def submitData(data):
        
    return redirect("Index", server)

@server.route("/system/restart")
def restart():
    server._status = "restart"
    print("status set to restert")
    return redirect("Index", server)

@server.route("/system/shutdown")
def shutdown():
    server._status = "shutdown"
    return redirect("Index", server)

# JSON DATA ROUTES UNTIL (REGEX IS FULLY IMPLEMENTED)

@server.route("/data/ledStatus")
def ledStatus():
    temp = {
        "ledStat":getValue(led)
    }
    return json.dumps(temp)
server.setupServer()



server.start()

