# main.py -- put your code here!
from server.classes.ServerClass import HttpServer
from server.ViewHelper import View, redirect, jsonify
from server.controlers.main_controller import toggle, getValue, led
from server.helpers import networkConnection
from server.helpers.jsonSaver import saveJSON
import json, gc, ujson

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

@server.route('/switch/settings')
def Settings():
    return View("Settings")

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

@server.route("/settings/savesettings")
def saveSettings(data):
    saveJSON(data)
    return redirect("Settings", server)

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

@server.route("/data/getsettingvalues")
def getSettingValues():
    f = open("./server/database/data.txt")
    temp = f.read()
    return ujson.dumps(temp)

@server.route("/data/getconfig")
def getConfig():
    f = open("./server/database/config.json")
    temp = f.read()
    return ujson.dumps(temp)



# SETUP AND START THE MAIN SERVER LOOP
server.setupServer()
server.start()

