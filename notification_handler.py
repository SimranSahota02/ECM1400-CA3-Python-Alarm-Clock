import logging

def remove_notification(notification, notifications) -> list:
    """This function uses a list of notifcations and a given notification
    to delete to return a list of notifications without the deleted 
    notification."""
    index = None
    found_index = False
    
    try:
        while not found_index:
            for i in range(0,len(notifications)):
                if (notifications[i])["title"] == notification:
                    index = i
                    found_index = True
                else:
                    pass
        notifications.pop(index)    
        return notifications
    except:
        logging.error("Detected value error in remove_notification method. No matching existing notification.")

    