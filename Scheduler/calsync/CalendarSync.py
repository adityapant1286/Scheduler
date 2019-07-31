
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class CalendarSync:

    # If modifying these scopes, delete the  file token.pickle.
    _SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    _CREDENTIAL_FILE_PATH = "resources/gcal-credentials.json"
    _TOKEN_FILE_PATH = "resources/gcal-token.pickle"
    _G_API = 'calendar'
    _G_API_VERSION = 'v3'

    def __init__(self):
        self._credential_file = os.path.join(os.getcwd(), CalendarSync._CREDENTIAL_FILE_PATH)
        self._token_file = os.path.join(os.getcwd(), CalendarSync._TOKEN_FILE_PATH)

    def main(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if self._token_file:
            with open(self._token_file, 'rb') as token:
                creds = pickle.load(token)
        # # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self._credential_file, CalendarSync._SCOPES)
                creds = flow.run_local_server()
        #     # Save the credentials for the next run
            with open(self._token_file, 'wb') as token:
                pickle.dump(creds, token)

        service = build(CalendarSync._G_API, CalendarSync._G_API_VERSION, credentials=creds)

        # # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming events')
        # events_result = service.calendarList().list().execute()

        events_result = service\
            .events()\
            .list(calendarId='3o25999e6er995p814k4lsic50@group.calendar.google.com', timeMin=now,
                  # maxResults=10,
                  singleEvents=True, orderBy='startTime')\
            .execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            print(">>> ")
            print(event)
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])


# gcal = GCalSync()
