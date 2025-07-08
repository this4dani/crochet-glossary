from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import re

SPREADSHEET_ID = '1WXt17J7Bn7nuRG3SV1HvvoWX4mvgZmY7dAeLRIlIh3A'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Connect to sheets
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Read glossarydata.js
with open('glossarydata.js', 'r') as f:
    content = f.read()

# Extract terms (basic parser)
terms = []
current_term = {}
lines = content.split('\n')

for line in lines:
    line = line.strip()
    
    if 'id:' in line:
        if current_term:
            terms.append(current_term)
        current_term = {}
        match = re.search(r'id:\s*"([^"]+)"', line)
        if match:
            current_term['ID'] = match.group(1).upper()
    
    elif 'name_us:' in line:
        match = re.search(r'name_us:\s*"([^"]+)"', line)
        if match:
            current_term['Name_US'] = match.group(1)
    
    elif 'name_uk:' in line:
        match = re.search(r'name_uk:\s*"([^"]+)"', line)
        if match:
            current_term['Name_UK'] = match.group(1)
    
    elif 'symbol:' in line:
        match = re.search(r'symbol:\s*"([^"]+)"', line)
        if match:
            current_term['Symbol'] = match.group(1)
    
    elif 'tags:' in line:
        match = re.search(r'tags:\s*\[(.*?)\]', line)
        if match:
            tags = match.group(1).replace('"', '').replace("'", '')
            current_term['Tags'] = tags
    
    elif 'notes:' in line:
        match = re.search(r'notes:\s*"([^"]+)"', line)
        if match:
            current_term['Description'] = match.group(1)

# Add last term
if current_term:
    terms.append(current_term)

print(f"Found {len(terms)} terms in glossarydata.js")

# Prepare data for sheets
headers = [['ID', 'Status', 'Name_US', 'Name_UK', 'Symbol', 'Category', 'Tags', 'Description', 'Priority']]

# Add headers
sheet.values().update(
    spreadsheetId=SPREADSHEET_ID,
    range='A1:I1',
    valueInputOption='RAW',
    body={'values': headers}
).execute()

# Format headers (bold, colored)
requests = [{
    'repeatCell': {
        'range': {
            'sheetId': 0,
            'startRowIndex': 0,
            'endRowIndex': 1
        },
        'cell': {
            'userEnteredFormat': {
                'backgroundColor': {'red': 0, 'green': 0.22, 'blue': 0.25},
                'textFormat': {
                    'foregroundColor': {'red': 1, 'green': 1, 'blue': 1},
                    'bold': True
                }
            }
        },
        'fields': 'userEnteredFormat(backgroundColor,textFormat)'
    }
}]

sheet.batchUpdate(
    spreadsheetId=SPREADSHEET_ID,
    body={'requests': requests}
).execute()

# Prepare rows
rows = []
for term in terms:
    # Determine category from tags
    tags = term.get('Tags', '')
    category = 'Other'
    if 'basic' in tags:
        category = 'Basic'
    elif 'shaping' in tags:
        category = 'Shaping'
    elif 'texture' in tags or 'post' in tags:
        category = 'Texture'
    elif 'foundation' in tags or 'starting' in tags:
        category = 'Foundation'
    
    row = [
        term.get('ID', ''),
        'Existing',  # Status
        term.get('Name_US', ''),
        term.get('Name_UK', ''),
        term.get('Symbol', ''),
        category,
        term.get('Tags', ''),
        term.get('Description', ''),
        ''  # Priority
    ]
    rows.append(row)

# Add all rows at once
if rows:
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f'A2:I{len(rows)+1}',
        valueInputOption='RAW',
        body={'values': rows}
    ).execute()

print(f"✅ Imported {len(rows)} terms to Google Sheets!")
print(f"📊 Open your sheet: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
print("\nCategories found:")
categories = {}
for row in rows:
    cat = row[5]
    categories[cat] = categories.get(cat, 0) + 1

for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count} terms")