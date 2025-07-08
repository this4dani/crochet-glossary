from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SPREADSHEET_ID = '11Q5FZ2iYvNhWwnJQwkB7VKyx74b7jjQLzprIBEFxUb8'
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# Share with your email
your_email = input("Enter your Gmail address: ")

permission = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': your_email
}

service.permissions().create(
    fileId=SPREADSHEET_ID,
    body=permission,
    sendNotificationEmail=False
).execute()

print(f"✅ Shared with {your_email}")
print(f"📋 Try opening: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")