from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

API_NAME = 'calendar'
API_VERSION = 'v3'

def calendar_events(credentials):
    cred=credentials
    now = datetime.datetime.utcnow().isoformat() + 'Z' 
    service=build('calendar', 'v3', credentials=cred)
    
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=2, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    info=[]
    i = 0
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
    test = {"message": 'Die ist eine Nachricht',
            "data": info,
            "speakMessage": True}
    return test