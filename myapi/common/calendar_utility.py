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
    #Check which Events are needed "today" or "tomorrow" or "lunch" and set minTime and maxTime
    if time == 'today':
        minTime=datetime.datetime(today.year, today.month, today.day, 0, 0, 1).isoformat() + 'Z'
        maxTime=datetime.datetime(today.year, today.month, today.day, 23, 59, 59).isoformat() + 'Z'
    elif time == 'tomorrow':
        minTime=datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 1).isoformat() + 'Z'
        maxTime=datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59).isoformat() + 'Z'
    elif time == 'lunch':
        minTime=datetime.datetime(today.year, today.month, today.day, 11, 0, 0).isoformat() + 'Z'
        maxTime=datetime.datetime(today.year, today.month, today.day, 15, 0, 0).isoformat() + 'Z'
    else:
        return 'Not a valid Date'

    #build service with GoogleCalendar API
    service=build('calendar', 'v3', credentials=cred)
    
    events_result = service.events().list(calendarId='primary', timeMin=minTime,
                                        timeMax=maxTime, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    #For the get_lunchteam we need the events 
    if time=='lunch':
        #return needed events
        return get_lunchtime(events)
    else:
        #generate List to store data from events in foor-Loop
        info=[]

        #for-Loop to store eventdata in python-Dict
        for event in events:
           start = event['start'].get('dateTime', event['start'].get('date'))
           title = event['summary'] or 'Kein Titel'
           link = event['htmlLink']
           end = event['end'].get('dateTime', event['end'].get('date'))
           informations = {"start": start,
                           "title": title,
                            "end": end,
                            "link": link}
           info.append(informations)

    #Add "message" and "speakMessage" to the data an return JSON-format
    data = {"message": 'Folgende Termine stehen heute an',
            "data": info,
            "speakMessage": True}
    return data

def get_lunchtime(eventslist):
    #Define needed Variables
    counter=0
    starts=[]
    ends=[]
    differences=[]
    today=datetime.date.today()
    minTime=datetime.datetime(today.year, today.month, today.day, 11, 0, 0).isoformat() + 'Z'
    maxTime=datetime.datetime(today.year, today.month, today.day, 15, 0, 0).isoformat() + 'Z'

    # Difference between the amout of events in lunchbreaktime
    # 0 Events means that lunchbreaktime can be at any time
    if eventslist:
            for event in eventslist:
                start = event['start'].get('dateTime', event['start'].get('date'))
                starts.append(start)
                end = event['end'].get('dateTime', event['end'].get('date'))
                ends.append(end)

            #Get Duration from 11am to start from first event
            #Then get Duration from End of the last Event to 3pm
            difference=datetime.datetime.strptime(starts[0], "%Y-%m-%dT%H:%M:%S+01:00")-datetime.datetime.strptime(minTime, "%Y-%m-%dT%H:%M:%SZ")
            differences.append(difference.seconds/60)
            difference=datetime.datetime.strptime(maxTime, "%Y-%m-%dT%H:%M:%SZ")-datetime.datetime.strptime(ends[-1], "%Y-%m-%dT%H:%M:%S+01:00")
            differences.append(difference.seconds/60)

            #Delete fist start and last end, because they were already used above
            newStarts=starts.copy()
            newEnds=ends.copy()
            del newStarts[0]
            del newEnds[-1]

            #Get the difference between the start and end times of the not used Events
            #The first Item in starts is the starttime of the 2nd Event and the last Item in ends is the enddtime of the secondlast Event
            for starttime in newStarts:
                difference=datetime.datetime.strptime(starttime, "%Y-%m-%dT%H:%M:%S+01:00")-datetime.datetime.strptime(newEnds[counter], "%Y-%m-%dT%H:%M:%S+01:00")
                differences.append(difference.seconds/60)
                counter=counter+1

            #Find largest Breaktime in differences
            maxBreakTime=max(differences)

            #Get Index of maxTime from differences
            index=differences.index(maxBreakTime)

            if index==0:
                startBreak=minTime
                endBreak=starts[0]
            elif index==1:
                startBreak=ends[-1]
                endBreak=maxTime
            else:
                startBreak=ends[index-2]
                endBreak=starts[index-1]

            info={
                "start": startBreak,
                "ende": endBreak,
                "Dauer": maxBreakTime
            }
            data = {"message": 'Deine vorgeschlagene Pausenzeit',
            "data": info,
            "speakMessage": True}
    else:
        data = {"message": 'Du hast heute Nachmittag frei',
            "data": None,
            "speakMessage": True}

    return data