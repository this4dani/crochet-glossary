from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Set up credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Create the spreadsheet
spreadsheet = {
    'properties': {
        'title': "DANI'S Crochet Glossary - Master Database"
    }
}

sheet = service.spreadsheets().create(body=spreadsheet).execute()
spreadsheet_id = sheet.get('spreadsheetId')

print(f"✅ Created spreadsheet!")
print(f"📋 Spreadsheet ID: {spreadsheet_id}")
print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
print("\n⚠️  IMPORTANT: Save the Spreadsheet ID above!")
print("You'll need it for the sync script.")

# Set up the header row
headers = [
    ['ID', 'Status', 'Name_US', 'Name_UK', 'Symbol', 'Category', 'Tags', 
     'Description', 'Added_Date', 'Priority', 'Verified']
]

body = {'values': headers}

service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range='A1:K1',
    valueInputOption='RAW',
    body=body
).execute()

print("\n✅ Headers added!")
print("\nNext steps:")
print("1. Open the spreadsheet URL above")
print("2. Share it with your service account email")
print("3. The service account email is in your credentials.json file")