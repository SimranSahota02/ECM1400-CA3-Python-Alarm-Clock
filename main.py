import logging
import sched
import time

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
import pyttsx3


import setup
import sched_handler
import alarm_handler
import notification_handler

app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
notifications, alarms = setup.setup()

@app.route('/')
def redirect_user():
    """The default app.route for a program is / however this program is run using a template
    that has app.route /index and so this function returns a built in flask method that
    redirects the user to the correct url."""
    return redirect('/index')

@app.route('/index')
def main():
    """The main function controls the program. It is responsible for calling other functions upon
    flask submissions/button presses. These are computed using the if statements that check which
    flask request has been made. The main function is also responsible for initialising the tts
    engine, logging and populating the flask webpage. The main function is linked to the /index 
    html template. Therefore it cannot be assigned to the default url and so it has app.route 
    /index."""
    global notifications
    global alarms

    engine = pyttsx3.init()
    logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.ERROR)
    
    #handle flask request for notification removal
    if request.args.get("notif"):
        notifications = notification_handler.remove_notification(request.args.get("notif"), 
        notifications)
    else:
        pass
    
    #handle flask request for new alarm creation
    if request.args.get("two"):
        alarms = alarm_handler.add_alarm(request.args.get("alarm"),
        request.args.get("two"), request.args.get("news"), 
        request.args.get("weather"), alarms)
        
        scheduled_alarms = sched_handler.schedule_alarms(s,alarm_handler.get_alarms("log.log"))
        
        for i in range(0,len(scheduled_alarms)):
            s.enter(float((scheduled_alarms[i])["time"]), 1, 
            sched_handler.read_alarm((scheduled_alarms[i])["alarm"],engine))
    else:
        pass

    #handle flask request for alarm removal
    if request.args.get("alarm_item"):
        alarms = alarm_handler.cancel_alarm(request.args.get("alarm_item"))

        scheduled_alarms = sched_handler.schedule_alarms(s,alarm_handler.get_alarms("log.log"))
        
        for i in range(0,len(scheduled_alarms)):
            s.enter(float((scheduled_alarms[i])["time"]), 1, 
            sched_handler.read_alarm((scheduled_alarms[i])["alarm"],engine))
    else:
        pass
    
    return render_template("index.html", notifications=notifications, alarms=alarms,
    image="image.jpg", title="Create alarm")

if __name__ == "__main__":
    s.run(blocking=False)
    app.run()   