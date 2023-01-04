# FORMATS THE DATE BECAUSE DATE TIME IS NEVER EASY

def convertTime(time:tuple):
    day = {0:"Mon", 1:"Tue", 2:"Wed", 3:"Thu", 4:"Fri", 5:"Sat", 6:"Sun"}
    month = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
    


    fTime = f'Date: {day[time[6]]}, {time[2]}, {time[0]} {time[3]}:{time[4]}:{time[5]} GMT'

    return(fTime)