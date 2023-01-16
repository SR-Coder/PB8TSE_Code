

import os, ujson

def saveJSON(data):
    print(f"data: {data}")
    for key in data:
        temp = data[key].replace("+", " ")
        data[key] = temp

    r = open("./server/database/data.txt")
    r = r.read()
    curData = ujson.loads(r)

    for key in data:
        curData[key] = data[key]    


    json_object = ujson.dumps(curData)
    print(json_object)
    f = open("./server/database/data.txt", "w")
    f.write(json_object)
    f.close()
    return True