import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# oauth constants
# TODO add write scope
READ_SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SCOPES = [READ_SCOPE]
CREDS_FILE = 'credentials.json'
PICKLE_FILE = 'token.pickle'

# spreadsheet constants
SPREADSHEET_ID = '1M7-7F_tau989WaFDC4leQIgt6PXKOslDb5E7kXlNPM8'
RANGE_NAME = 'Sheet1'
FILTER_FIELD = 2


def init_config(config_dict):
    try:
        CREDS_FILE = config_dict["oauthInfo"]["credentialFile"]
        PICKLE_FILE = config_dict["oauthInfo"]["pickleFile"]

        SPREADSHEET_ID = config_dict["spreadsheetInfo"]["spreadsheetId"]
        RANGE_NAME = config_dict["spreadsheetInfo"]["sheetName"]
        FILTER_FIELD = config_dict["spreadsheetInfo"]["filterField"]
    except Exception:
        print("ERROR: unable to load api configuration file")
        exit(11)


def retrieve_spreadsheet_data():
    creds = None
    bool_field = FILTER_FIELD

    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    # creds not valid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()

    values = result.get('values', [])

    filter_values = []
    error_values = []

    if not values:
        print('No data')
    else:
        for row in values:
            print('ROW: %s' % row)
            # check the bool flag to see if work needs to be done
            if row[bool_field] == 'TRUE':
                print('adding %s to return values' % row)
                filter_values.append(row)
            elif row[bool_field] == 'FALSE':
                print('false value, value was %s' % row[bool_field])
                continue
            else:
                error_values.append(row)

    # print all error lines for review
    # TODO flush to log file
    print("Error Rows")
    print("#" * 60)
    for err in error_values:
        print(err)
    print("#" * 60)

    return filter_values



