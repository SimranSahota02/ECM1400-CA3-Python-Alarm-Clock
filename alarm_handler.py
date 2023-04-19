import logging

import setup

def get_alarms(file) -> list:
    """Function get_alarms uses a reads a file and appends each line with the designated alarm
    format to a list of dictionaries which it returns. The alarm dictionaries use key names
    that are consistent with the html template indexes input fields so that the fields translate
    directly."""
    alarms = []
    with open(file) as log_file:
        log_lines = log_file.readlines()

    log_file.close()

    #Each line in the file is read through as locations of alarm fields in line are consistent     
    for i in range(0, len(log_lines)):
        if (log_lines[i])[0:5] == "ALARM":
            alarm = {}
            alarm["datetime"] = (log_lines[i])[5:21]

            if (log_lines[i])[21] == "T":
                alarm["news"] = "news"
            else:
                alarm["news"] = None

            if ((log_lines[i])[22]) == "T":
                alarm["weather"] = "weather"
            else:
                alarm["weather"] = None

            alarm["two"] = ((log_lines[i])[23:len(log_lines[i])]).strip("\n")
            alarms.append(alarm)
        else:
            pass

    return alarms

def displayable_alarms(alarms) -> list:
    """This function takes a list of alarm dictionaries and iterates through it, using string
    manipulation to convert the dictionaries into formatted dictionaries that have only two
    keys, title and content. The values associated with these keys are readable strings and
    are consistent with the fields that the html template index uses to display alarms."""
    formatted_alarms = []
    
    for i in range(0,len(alarms)):
        alarm = {}
        formatted_time = (((alarms[i])["datetime"])[8:10] + "/" + ((alarms[i])["datetime"])[5:7]
        + "/" + ((alarms[i])["datetime"])[0:4] + " at " + ((alarms[i])["datetime"])[11:16])
        
        if (alarms[i])["news"] and (alarms[i])["weather"]:
            reports = " with news and weather reports."
        elif (alarms[i])["news"]:
            reports = " with news report."
        elif (alarms[i])["weather"]:
            reports = " with weather report."
        else:
            reports = "."

        alarm["title"] = (alarms[i])["two"]
        alarm["content"] = "Alarm on " + formatted_time + reports

        formatted_alarms.append(alarm)
    
    return formatted_alarms

def add_alarm(datetime,name,news,weather,alarms):
    """The add alarm function takes inputs from the flask page and converts them into the
    format that alarms are saved as. It then appends the alarm to the log file by writing
    to it. Finally it returns the setup module function construct alarms as this rereads the
    log file and will add the new alarm to the list of alarms."""
    alarm = ""

    if news:
        n = "T"
    else:
        n = "F"
    
    if weather:
        w = "T"
    else:
        w = "F"
    
    alarm = "ALARM" + datetime + n + w + name
    alarms.append(alarm)
    with open("log.log", "a+") as file:
        file.write(alarm + "\n")

    return setup.construct_alarms()

def cancel_alarm(name):
    """The add alarm function takes inputs from the flask page and reads the log file for the
    line containing the same alarm as the input name. It then deletes the alarm from the log 
    file by changing the text on the line with the same index as the matching alarm, then
    writing the amended file back to the log file. Finally it returns the setup module function 
    construct alarms as this rereads the log file and will remove the deleted alarm."""
    with open("log.log") as file:
        file_lines = file.readlines()
    
    file.close()
    index = 0

    #Locate index of alarm line in file
    try:
        for i in range(0,len(file_lines)):
            if (file_lines[i])[23:len(file_lines[i])+1].strip("\n") == name:
                index = i
            else:
                pass
    except:
        logging.error("Detected value error in cancel alarm method. No matching existing alarm.")
        
    file_lines[int(index)] = "CANCELLED\n"

    with open("log.log", "w") as file:
        for i in range(0,len(file_lines)):
            file.write(file_lines[i])
    
    file.close()

    return setup.construct_alarms()