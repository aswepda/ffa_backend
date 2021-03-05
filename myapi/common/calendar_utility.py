from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json



def calendar_events(credentials, time):
    #Save Variables 
    cred=credentials
    time = time
    
    #Get todays and tomorrows day, month and year
    today=datetime.date.today()
    tomorrow=today + datetime.timedelta(days=1)
    #Check which Events are needed "today" or "tomorrow" and set minTime and maxTime
    if time == 'today':
        minTime=datetime.datetime(today.year, today.month, today.day, 0, 0, 1).isoformat() + 'Z'
        maxTime=datetime.datetime(today.year, today.month, today.day, 23, 59, 59).isoformat() + 'Z'
    elif time == 'tomorrow':
        minTime=datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 1).isoformat() + 'Z'
        maxTime=datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59).isoformat() + 'Z'
    else:
            return 'Not a valid Date'
    # now = datetime.datetime.utcnow().isoformat() + 'Z' 
    #build service with GoogleCalendar API
    service=build('calendar', 'v3', credentials=cred)
    
    events_result = service.events().list(calendarId='primary', timeMin=minTime,
                                        timeMax=maxTime, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    #generate List to store data from events in foor-Loop
    info=[]

    #for-Loop to store eventdata in python-Dict
    for event in events:
       start = event['start'].get('dateTime', event['start'].get('date'))
       title = event['summary']
       link = event['htmlLink']
       end = event['end'].get('dateTime', event['end'].get('date'))
       informations = {"start": start,
                       "title": title,
                        "end": end,
                        "link": link}
       info.append(informations)

       #Add "message" and "speakMessage" to the data
    data = {"message": 'Die ist eine Nachricht',
            "data": info,
            "speakMessage": True}
    return data