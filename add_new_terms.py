from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

SPREADSHEET_ID = '1WXt17J7Bn7nuRG3SV1HvvoWX4mvgZmY7dAeLRIlIh3A'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Connect to sheets
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# PRIORITY 1: Missing Basic Stitches (10 terms)
basic_stitches = [
    {
        'ID': 'DTR',
        'Name_US': 'Double Treble Crochet',
        'Name_UK': 'Triple Treble Crochet',
        'Symbol': 'TTT',
        'Category': 'Basic',
        'Tags': 'basic, tall, advanced',
        'Description': 'Very tall stitch with 2 yarn overs before inserting hook'
    },
    {
        'ID': 'TRTR',
        'Name_US': 'Triple Treble Crochet',
        'Name_UK': 'Quadruple Treble Crochet',
        'Symbol': 'TTTT',
        'Category': 'Basic',
        'Tags': 'basic, tall, advanced',
        'Description': 'Extremely tall stitch with 3 yarn overs'
    },
    {
        'ID': 'SLIPKNOT',
        'Name_US': 'Slip Knot',
        'Name_UK': 'Slip Knot',
        'Symbol': '○',
        'Category': 'Foundation',
        'Tags': 'foundation, starting, basic',
        'Description': 'The very first loop to start any crochet project'
    },
    {
        'ID': 'YO',
        'Name_US': 'Yarn Over',
        'Name_UK': 'Yarn Over Hook',
        'Symbol': '/',
        'Category': 'Technique',
        'Tags': 'basic, technique, fundamental',
        'Description': 'Wrap yarn around hook - fundamental movement in crochet'
    },
    {
        'ID': 'LOOP',
        'Name_US': 'Loop',
        'Name_UK': 'Loop',
        'Symbol': '○',
        'Category': 'Basic',
        'Tags': 'basic, fundamental',
        'Description': 'A loop of yarn on the hook'
    }
]

# PRIORITY 2: Common Pattern Terms (10 terms)
pattern_terms = [
    {
        'ID': 'REP',
        'Name_US': 'Repeat',
        'Name_UK': 'Repeat',
        'Symbol': '*',
        'Category': 'Pattern',
        'Tags': 'pattern, instruction',
        'Description': 'Repeat instructions between asterisks'
    },
    {
        'ID': 'SK',
        'Name_US': 'Skip',
        'Name_UK': 'Miss',
        'Symbol': '-',
        'Category': 'Pattern',
        'Tags': 'pattern, instruction, shaping',
        'Description': 'Skip the next stitch without working into it'
    },
    {
        'ID': 'SP',
        'Name_US': 'Space',
        'Name_UK': 'Space',
        'Symbol': '_',
        'Category': 'Pattern',
        'Tags': 'pattern, instruction',
        'Description': 'Gap between stitches, often created by chains'
    },
    {
        'ID': 'TURN',
        'Name_US': 'Turn',
        'Name_UK': 'Turn',
        'Symbol': '↻',
        'Category': 'Technique',
        'Tags': 'technique, rows',
        'Description': 'Turn work around to start next row'
    },
    {
        'ID': 'JOIN',
        'Name_US': 'Join',
        'Name_UK': 'Join',
        'Symbol': 'J',
        'Category': 'Technique',
        'Tags': 'technique, joining, rounds',
        'Description': 'Join round with slip stitch to first stitch'
    },
    {
        'ID': 'FO',
        'Name_US': 'Fasten Off',
        'Name_UK': 'Cast Off',
        'Symbol': '✂',
        'Category': 'Technique',
        'Tags': 'technique, finishing',
        'Description': 'Cut yarn and pull through last loop to secure'
    },
    {
        'ID': 'BEG',
        'Name_US': 'Beginning',
        'Name_UK': 'Beginning',
        'Symbol': '→',
        'Category': 'Pattern',
        'Tags': 'pattern, instruction',
        'Description': 'Start of round or row'
    },
    {
        'ID': 'CONT',
        'Name_US': 'Continue',
        'Name_UK': 'Continue',
        'Symbol': '...',
        'Category': 'Pattern',
        'Tags': 'pattern, instruction',
        'Description': 'Continue in pattern as established'
    },
    {
        'ID': 'RND',
        'Name_US': 'Round',
        'Name_UK': 'Round',
        'Symbol': '○',
        'Category': 'Pattern',
        'Tags': 'pattern, rounds',
        'Description': 'Complete circle of stitches'
    },
    {
        'ID': 'ROW',
        'Name_US': 'Row',
        'Name_UK': 'Row',
        'Symbol': '—',
        'Category': 'Pattern',
        'Tags': 'pattern, rows',
        'Description': 'Horizontal line of stitches worked back and forth'
    }
]

# PRIORITY 3: Essential Missing Techniques (10 terms)
techniques = [
    {
        'ID': 'GAUGE',
        'Name_US': 'Gauge',
        'Name_UK': 'Tension',
        'Symbol': '□',
        'Category': 'Technique',
        'Tags': 'technique, measuring, sizing',
        'Description': 'Number of stitches and rows per inch/cm'
    },
    {
        'ID': 'BLOCKING',
        'Name_US': 'Blocking',
        'Name_UK': 'Blocking',
        'Symbol': '▭',
        'Category': 'Finishing',
        'Tags': 'finishing, technique',
        'Description': 'Wetting and shaping finished pieces to measurements'
    },
    {
        'ID': 'WEAVE',
        'Name_US': 'Weave in Ends',
        'Name_UK': 'Sew in Ends',
        'Symbol': '~',
        'Category': 'Finishing',
        'Tags': 'finishing, technique',
        'Description': 'Hide yarn tails by weaving through stitches'
    },
    {
        'ID': 'SEAM',
        'Name_US': 'Seam',
        'Name_UK': 'Seam',
        'Symbol': '||',
        'Category': 'Construction',
        'Tags': 'construction, joining, finishing',
        'Description': 'Join pieces together with needle and yarn'
    },
    {
        'ID': 'RS',
        'Name_US': 'Right Side',
        'Name_UK': 'Right Side',
        'Symbol': 'RS',
        'Category': 'Pattern',
        'Tags': 'pattern, sides',
        'Description': 'The front/public side of the work'
    },
    {
        'ID': 'WS',
        'Name_US': 'Wrong Side',
        'Name_UK': 'Wrong Side',
        'Symbol': 'WS',
        'Category': 'Pattern',
        'Tags': 'pattern, sides',
        'Description': 'The back/private side of the work'
    },
    {
        'ID': 'PM',
        'Name_US': 'Place Marker',
        'Name_UK': 'Place Marker',
        'Symbol': 'M',
        'Category': 'Technique',
        'Tags': 'technique, marking',
        'Description': 'Place stitch marker in stitch or between stitches'
    },
    {
        'ID': 'SM',
        'Name_US': 'Slip Marker',
        'Name_UK': 'Slip Marker',
        'Symbol': 'M→',
        'Category': 'Technique',
        'Tags': 'technique, marking',
        'Description': 'Move marker from one needle to the other'
    },
    {
        'ID': 'M1',
        'Name_US': 'Make 1',
        'Name_UK': 'Make 1',
        'Symbol': 'M1',
        'Category': 'Shaping',
        'Tags': 'increase, shaping',
        'Description': 'Invisible increase between stitches'
    },
    {
        'ID': 'BO',
        'Name_US': 'Bind Off',
        'Name_UK': 'Cast Off',
        'Symbol': 'BO',
        'Category': 'Finishing',
        'Tags': 'finishing, edges',
        'Description': 'Secure stitches at end of piece'
    }
]

# Get current row count
result = sheet.values().get(
    spreadsheetId=SPREADSHEET_ID,
    range='A:A'
).execute()
current_rows = len(result.get('values', []))
next_row = current_rows + 1

print(f"Current rows in sheet: {current_rows}")
print(f"Starting at row: {next_row}")

# Combine all new terms
all_new_terms = basic_stitches + pattern_terms + techniques

# Prepare rows
new_rows = []
for term in all_new_terms:
    row = [
        term['ID'],
        'New',  # Status
        term['Name_US'],
        term['Name_UK'],
        term.get('Symbol', ''),
        term.get('Category', ''),
        term.get('Tags', ''),
        term.get('Description', ''),
        'High'  # Priority
    ]
    new_rows.append(row)

# Add to sheet
if new_rows:
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f'A{next_row}:I{next_row + len(new_rows) - 1}',
        valueInputOption='RAW',
        body={'values': new_rows}
    ).execute()
    
    print(f"✅ Added {len(new_rows)} new terms!")
    print(f"📊 Total terms now: {current_rows - 1 + len(new_rows)}")
    
    # Color new rows
    requests = [{
        'repeatCell': {
            'range': {
                'sheetId': 0,
                'startRowIndex': next_row - 1,
                'endRowIndex': next_row + len(new_rows) - 1,
                'startColumnIndex': 1,
                'endColumnIndex': 2
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': {'red': 1, 'green': 0.42, 'blue': 0.48}
                }
            },
            'fields': 'userEnteredFormat.backgroundColor'
        }
    }]
    
    sheet.batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={'requests': requests}
    ).execute()

print("\n📈 Progress toward 150 terms:")
total = current_rows - 1 + len(new_rows)
print(f"   {total}/150 ({int(total/150*100)}%)")
print(f"   {150 - total} terms remaining")
print(f"\n🔗 Sheet: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")