from datetime import datetime
import logging

import setup

def schedule_alarms(scheduler,alarms) -> list:
    """This function returns a list of dictionaries that contain an alarm dictionary and a time 
    delay. The time delay and alarm are to be used with the scheduler run through the main
    function to schedule alarm tts announcements."""

    #First all currently scheduled alarms are deleted as to avoid duplicate events
    list(map(scheduler.cancel, scheduler.queue))
    scheduled_alarms = []

    for i in range(0,len(alarms)):

        #Calculates difference in seconds between alarm trigger and current time
        date_now = create_datetime_date(str(datetime.now()))
        date_alarm = create_datetime_date(str((alarms[i])["datetime"]))
        alarm_due_in = (date_alarm - date_now).total_seconds()

        if alarm_due_in > 0:
            play_alarm = {}
            play_alarm["alarm"] = alarms[i]
            play_alarm["time"] = alarm_due_in
            scheduled_alarms.append(play_alarm)
        else:
            pass
    
    return scheduled_alarms

def create_datetime_date(date_string):
    """Given a string of valid format this function will return a datetime object that 
    contains that contains the date input in the string."""
    try:
        year = int(date_string[0:4])
        month = int(date_string[5:7])
        day = int(date_string[8:10])
        hour = int(date_string[11:13])
        minute = int(date_string[14:16])
        
        created_date = datetime(year,month,day,hour,minute,00)
        return created_date
    except:
        logging.error("Detected value error in create_datetime_date method."
        + "String passed into function is not in valid format.")
        raise TypeError

def read_alarm(alarm, ttsengine):
    """This function takes an alarm dictionary and a pytts engine as arguements, assembling
    the data within the alarm dictionary into a readable announcement and then reading it
    out with the text to speech engine. This is the function called by the scheduler."""
    to_read = ""
    data_to_read_from = setup.construct_brief()
    to_read += alarm["two"] + " "

    #News and weather reports are appended to the end of the string to be read when applicable
    if alarm["weather"] == "weather":
        to_read += ((data_to_read_from[0])["title"] + " " + (data_to_read_from[0])["content"])
    else:
        pass

    if alarm["news"] == "news":
        for i in range(2,len(data_to_read_from)):
            to_read += (" " + (data_to_read_from[i])["title"])
    else:
        pass

    ttsengine.say(to_read)
    ttsengine.runAndWait()

    return None