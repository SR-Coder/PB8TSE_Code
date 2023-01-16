import os


def getRoute(request):
    # print("REQUEST IN GET ROUTE FUNC -->", request)
    # need to add checking to make sure that this does not break on load.
    head = request.split('\n')
    
    data = {}
    if len(head) < 2:
        print("ERROR: Bad Request --> ", head)
        return None
    requestType = head[0].split()[0]
    requestRoute = head[0].split()[1]
    if requestType == 'POST':
        if head[len(head)-1] is not "":
            dataList = head[len(head)-1].split('&')

            for d in dataList:
                temp = d.split('=')
                data[f'{temp[0]}'] = temp[1]
    if requestRoute == "/favicon.ico":
        return ('GET', '/favicon.ico')
    else:
        return (requestType,requestRoute, data)


def favIcon():
    dirname = os.path.dirname(__file__)
    reldir = os.path.join(dirname, '../Static/favicon.ico')
    header = 'HTTP/1.1 200 OK\n'
    mimetype = 'image/x-icon'

    header += 'Content-Type: '+str(mimetype)+'<strong>\n\n</strong>'

    header.encode("utf-8")
    fileIco = open(reldir, 'rb') # reads the file as binary
    iconStream = fileIco.read()
    fileIco.close()

    finalRes = header.encode("utf-8")
    finalRes += iconStream


    return finalRes