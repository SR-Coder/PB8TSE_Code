import socket, time, gc, os, machine, sys
from server.RouteParser import getRoute, favIcon
from server.FileHandler import GEThandler
from server.helpers.dateFormater import convertTime

class HttpServer:
    def __init__(self, ServerHost: str, ServerPort: int, verbose: bool):
        self._host = ServerHost
        self._port = ServerPort
        self._client_connection = ""
        self._client_address = ""
        self._request = ""
        self._response = ""
        self._logging = verbose
        self._registeredRoutes = {}
        self._serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._status = "run"

    # this decorator creates a list of all the registered function
    def route(self, *args):
            def register(func):
                self._registeredRoutes[args[0]] = func
                return func
            register.all = self._registeredRoutes
            return register

    # initializes the server, esentially taking in all the parameters and ensuring that the server is set up.
    # additionally the route function decorator is called with registers all the methods for routing.  need to add 
    # specific paths so that it can search different places for files.  

    def setupServer(self):
        addr = socket.getaddrinfo(self._host, self._port)[0][-1]
        print(addr)
        self._serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._serverSocket.bind(addr)
        self._serverSocket.listen(1)
        serverStr = 'The server setup to listen on port: '
        serverStr = serverStr + f'{self._port}'
        print(serverStr)
        regall = self.route()
        if self._logging == True:
            print("Get a list of all the routes available in the server")
            print(regall)
        return self._serverSocket

    def setStatus(self, newStatus):
        print("in set status", newStatus)
        if newStatus == None or newStatus == "":
            return None
        elif newStatus == "restart":
            self._status = "restart"
        elif newStatus == "shutdown":
            self._status = "shutdown"
        else:
            return None
    
    # This defines the main control loop of the application.  

    def start(self):
        while self._status == "run":
            curDate = f'{convertTime(time.gmtime())}'

            # wait for connections
            try:
                self._client_connection, self._client_address = self._serverSocket.accept()
            
                ######################################################################################
                # verbose logging
                if self._logging == True:
                    print(f"{curDate} :: A connection was recieved from {self._client_address}")
                ######################################################################################

                # catch the incomming client request.
                # Notes: using a local variable seems to increase reliabiltiy.
                thisRequest = self._client_connection.recv(1024).decode()
                self._request = thisRequest

                # print(thisRequest)            
                # getRoute parses the incoming request and returns a tuple that includes the request
                # type and the route ex: ('GET','/favicon.ico')
                request = getRoute(thisRequest)
                ######################################################################################
                # verbose logging
                if self._logging == True:
                    print(f"{curDate} : {self._request}")
                ######################################################################################

                else:

                    # this check catched unregestered request such as favicon or css or files directly requested.
                    # security needs to be implmented on this method so that only files in the static directory can 
                    # accessed.
                    if request != None and request[1] not in self._registeredRoutes:
                        finalRes = GEThandler(request)
                        self._client_connection.send(finalRes)    

                    elif request != None and request[1] != '/favicon.ico':
                        if request[1] in self._registeredRoutes:
                            if request[0] == "POST":
                                self._response = self._registeredRoutes[request[1]](request[2])
                            else:
                                self._response =  self._registeredRoutes[request[1]]()

                            if self._response == 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found':
                                print( f"WARNING: {curDate}, '{request[0]} {request[1]}' recieved from {self._client_address} No File exists."  )
                            else:
                                print(f"REQUEST: {curDate}: '{request[0]} {request[1]}' recieved from {self._client_address}")
                        else:
                            self._response = 'HTTP/1.0 404 NOT FOUND\n\nRoute Not Found'
                            print( f"WARNING: {curDate}, '{request[0]} {request[1]}' recieved from {self._client_address} No Route exists."  )
                        
                        self._client_connection.sendall(self._response.encode())

                
                    
                

            # Send the response
            # self._client_connection.sendall(self._response.encode())
            except Exception as e:
                print(f"ERROR: {curDate}: {e}: Something went wrong with the client connection")
                self._client_connection.close()

            self._client_connection.close()
        
        if self._status == "restart":
            for i in range(5,0,-1):
                print(f"STATUS: Restarting in: {i} seconds!")
                time.sleep(1)
                # os.system('clear')
            
            return machine.reset()
        elif self._status == "shutdown":
            for i in range(5,0,-1):
                print(f"STATUS: Shutting down in: {i} seconds!")
                time.sleep(1)
                # os.system('clear')           
            return None


    def close(self):
        self._serverSocket.close()


