import os, time
from server.helpers.CheckFile import fileExists
from server.helpers.dateFormater import convertTime
from server.classes.TemplateEngine import TemplateEngine    


# This file will handle everything to do with getting files and parsing them so that they can be returned to the client
# eventually this will be the home of the direct parsing so that we can include python code directly in the html pages.


def View(ViewName: str, context={}):

    now = convertTime(time.gmtime())

    # we need to read in the file onto a variable and return that so that 
    # it can be sent as the response.
    errorMsg = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
    fileName = ViewName + ".html"

    # dirname = os.path.dirname(__file__)
    dirname = os.getcwd() + 'server'

    checkFile = dirname + "/" + "Views/" + fileName

    fileList = os.listdir(dirname + "/Views")

    isValidFile = fileExists(fileName, fileList)


    if isValidFile:
        fileIn = open(checkFile)
        htmlDoc = 'HTTP/1.0 200 OK\n\n'
        htmlDoc = htmlDoc + fileIn.read()
        fileIn.close()



        return htmlDoc

    return errorMsg

def redirect(funcName: str, serverObj: object):
    for func in serverObj._registeredRoutes:
        if serverObj._registeredRoutes[func].__name__ == funcName:
            resStr = f'HTTP/1.1 303 See Other\r\nCache-Control: no-cache, private\r\nLocation: {func}\r\n{convertTime(time.gmtime())}\r\n\r\n'
            return resStr
    htmlDoc = 'HTTP/1.0 404 NOT FOUND\n\nRoute Not Found'
    return htmlDoc

def jsonify(dictionary: str):
    header = f'HTTP/1.1 200 OK\r\nContent-Type: application/vnd.api+json\r\n{convertTime(time.gmtime())}\r\n\r\n'
    return header + dictionary
