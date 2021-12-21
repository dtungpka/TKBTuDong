import datetime
import os.path
import os
import traceback
import googleapiclient
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import time
# If modifying these scopes, delete the file token.json.
class Calendar():
    def __init__(self, CREDENTIALS_FILE):
        self.CREDENTIALS_FILE = CREDENTIALS_FILE
    def get_calendar_service(self):
       SCOPES = ['https://www.googleapis.com/auth/calendar']

       creds = None
       # The file token.json stores the user's access and refresh tokens, and
       # is
       # created automatically when the authorization flow completes for the
       # first
       # time.
       if os.path.exists('token.json'):
           with open('token.json', 'r') as token:
               creds = Credentials.from_authorized_user_file('token.json', SCOPES)
       # If there are no (valid) credentials available, let the user log in.
       if not creds or not creds.valid:
           if creds and creds.expired and creds.refresh_token:
               creds.refresh(Request())
           else:
               flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_FILE, SCOPES)
               creds = flow.run_local_server(port=0)

           # Save the credentials for the next run
           with open('token.json', 'w') as token:
               token.write(creds.to_json())

       service = build('calendar', 'v3', credentials=creds)
       return service




    def CreateEvent(self,Subject="",desc="",start=datetime(1900,1,1),end=datetime(1900,1,1),organizer="",location=''):
       # creates one hour event tomorrow 10 AM IST
       service = self.get_calendar_service()
       print(Subject)
       print(desc)
       print(start)
       print(end)
       print(organizer)
       print(location)
       Success = False
       ErrorCount = 0
       while Success == False:
        try:
         event_result = service.events().insert(calendarId='primary',
           body={
               "summary": Subject,
               "description": desc,
               "location:":location,
               "start": {"dateTime": start, "timeZone": 'Asia/Ho_Chi_Minh'},
               "organizer": {"displayName": organizer},
               "end": {"dateTime": end, "timeZone": 'Asia/Ho_Chi_Minh'},"reminders": {"useDefault": False,"overrides": [{ "method": "popup","minutes": 5},{ "method": "popup","minutes": 30}]},

  }).execute()
         Success = True
        except:
            print("Error! retrying..")
            ErrorCount += 1
            if ErrorCount == 10:
                print("Loi Tai Khoan Google! Xin dang nhap lai")
                os.remove('token.json')
                service = self.get_calendar_service()
       time.sleep(0.5)
       return event_result['id'],event_result['summary'],event_result['start']['dateTime'],event_result['end']['dateTime']
    def DeleteEvent(self,ID):
       # Delete the event
       Success = False
       ErrorCount = 0
       while Success == False:
        
        ErrorCount += 1
        if ErrorCount > 5:
            print("Error while deleting event..")
            break
        try:
           service = self.get_calendar_service()
           service.events().delete(calendarId='primary',eventId=ID,).execute()
           Success = True
           print("Event deleted")
           time.sleep(0.5)
        except googleapiclient.errors.HttpError.error_details:
            print("Failed to delete event")
            
        