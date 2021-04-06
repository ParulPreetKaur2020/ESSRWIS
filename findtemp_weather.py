import re
from datetime import datetime

##Finding the exact value of temperature from the API as API returns a string and we are interested in just the value
def findtemperature(string):
    Intnumber=re.findall('\d+', string)
    Floatnumber=re.findall("\d+\.\d+", string)
    if (Floatnumber):
        return(Floatnumber)
    else:
        return(Intnumber)

###converting created_at(timeztamp without timezone in the format 2020-11-19 23:55:00 from current time and date
def findcreated_at(now):
    time = str(now.time()).split(':')
    time[2] = '00'##changing the microseconds to 00
    Time = time[0] + ":" + time[1] + ":" + time[2]
    date = now.date()
    created_at = str(date) + " " + Time
    return(created_at)
