import os, json, base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds_json = base64.b64decode(os.getenv("GOOGLE_CREDENTIALS_JSON")).decode()
    creds_dict = json.loads(creds_json)

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(os.getenv("GOOGLE_SHEET_ID")).sheet1
    return sheet

def append_event(row):
    sheet = get_sheet()
    sheet.append_row(row)
