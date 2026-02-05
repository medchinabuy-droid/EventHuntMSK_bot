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
    return client.open_by_key(os.getenv("GOOGLE_SHEET_ID")).worksheet("events")

def get_all_uids():
    sheet = get_sheet()
    records = sheet.get_all_records()
    return set(r.get("UID") for r in records if r.get("UID"))

def append_event(row):
    sheet = get_sheet()
    sheet.append_row(row)
