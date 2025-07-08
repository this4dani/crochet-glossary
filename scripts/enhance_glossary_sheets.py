#!/usr/bin/env python3
"""
Enhance glossary data directly in Google Sheets
"""

import sys
sys.path.append('..')  # To import from parent directory

from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
from collections import Counter

# Your spreadsheet ID
SPREADSHEET_ID = '1WXt17J7Bn7nuRG3SV1HvvoWX4mvgZmY7dAeLRIlIh3A'

# Credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def get_sheets_service():
    """Initialize Google Sheets API service"""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()

def analyze_glossary(sheets):
    """Analyze current glossary data"""
    # Read current data
    result = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:Z'
    ).execute()
    
    values = result.get('values', [])
    if not values:
        print("No data found!")
        return
    
    headers = values[0]
    data = values[1:]
    
    print(f"\n=== GLOSSARY ANALYSIS ===")
    print(f"Total terms: {len(data)}")
    
    # Find column indices
    id_idx = headers.index('ID') if 'ID' in headers else 0
    name_idx = headers.index('Name_US') if 'Name_US' in headers else 1
    status_idx = headers.index('Status') if 'Status' in headers else -1
    
    # Check for duplicates
    ids = [row[id_idx] if len(row) > id_idx else '' for row in data]
    id_counts = Counter(ids)
    duplicates = [id for id, count in id_counts.items() if count > 1]
    
    if duplicates:
        print(f"\n❌ DUPLICATE IDs FOUND: {duplicates}")
    else:
        print("\n✅ No duplicate IDs")
    
    # Check status breakdown
    if status_idx >= 0:
        statuses = [row[status_idx] if len(row) > status_idx else 'Unknown' for row in data]
        status_counts = Counter(statuses)
        print("\nStatus breakdown:")
        for status, count in status_counts.most_common():
            print(f"  {status}: {count}")
    
    return headers, data

def add_enhancement_columns(sheets, headers):
    """Add new columns for enhanced data if they don't exist"""
    new_columns = [
        'Difficulty',
        'Time_To_Learn', 
        'Common_Mistakes',
        'Pro_Tips',
        'Best_For',
        'Hook_Sizes',
        'Left_Handed_Note'
    ]
    
    # Check which columns are missing
    missing_columns = [col for col in new_columns if col not in headers]
    
    if missing_columns:
        print(f"\nAdding new columns: {missing_columns}")
        
        # Get current sheet dimensions
        sheet_metadata = sheets.get(spreadsheetId=SPREADSHEET_ID).execute()
        sheet_id = sheet_metadata['sheets'][0]['properties']['sheetId']
        current_cols = sheet_metadata['sheets'][0]['properties']['gridProperties']['columnCount']
        
        # Calculate new range
        start_col = len(headers)
        end_col = start_col + len(missing_columns)
        
        # Add column headers
        range_name = f'Sheet1!{chr(65 + start_col)}1:{chr(65 + end_col - 1)}1'
        body = {
            'values': [missing_columns]
        }
        
        sheets.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Added {len(missing_columns)} new columns")
        
        # Return updated headers
        return headers + missing_columns
    
    return headers

def enhance_terms(sheets, headers, data):
    """Add enhancement data to all terms"""
    print("\n=== ENHANCING TERMS ===")
    
    # Get column indices
    id_idx = headers.index('ID')
    tags_idx = headers.index('Tags') if 'Tags' in headers else -1
    diff_idx = headers.index('Difficulty') if 'Difficulty' in headers else -1
    time_idx = headers.index('Time_To_Learn') if 'Time_To_Learn' in headers else -1
    mistakes_idx = headers.index('Common_Mistakes') if 'Common_Mistakes' in headers else -1
    tips_idx = headers.index('Pro_Tips') if 'Pro_Tips' in headers else -1
    best_idx = headers.index('Best_For') if 'Best_For' in headers else -1
    
    updates = []
    
    for i, row in enumerate(data):
        # Ensure row has enough columns
        while len(row) < len(headers):
            row.append('')
        
        term_id = row[id_idx] if len(row) > id_idx else ''
        tags = row[tags_idx].split(', ') if tags_idx >= 0 and len(row) > tags_idx else []
        
        # Skip if already has difficulty
        if diff_idx >= 0 and len(row) > diff_idx and row[diff_idx]:
            continue
        
        # Assign difficulty and time based on tags
        difficulty = ''
        time_to_learn = ''
        
        if any(tag in ['basic', 'foundation', 'beginner'] for tag in tags):
            difficulty = '1'
            time_to_learn = '15-30 minutes'
        elif any(tag in ['intermediate', 'texture', 'shaping'] for tag in tags):
            difficulty = '3'
            time_to_learn = '30-60 minutes'
        elif any(tag in ['advanced', 'tunisian', 'lace'] for tag in tags):
            difficulty = '4'
            time_to_learn = '1-2 hours'
        elif any(tag in ['expert', 'specialty'] for tag in tags):
            difficulty = '5'
            time_to_learn = '2+ hours'
        else:
            difficulty = '2'
            time_to_learn = '30 minutes'
        
        # Add common mistakes for basic stitches
        mistakes = ''
        if term_id in ['sc', 'dc', 'hdc', 'tr', 'ch', 'slst']:
            mistakes = 'Working into wrong loop; Incorrect stitch count; Tension issues'
        
        # Add pro tips for beginner stitches
        tips = ''
        if difficulty in ['1', '2']:
            tips = 'Count stitches regularly; Use stitch markers; Keep consistent tension'
        
        # Add best for suggestions
        best_for = ''
        if 'amigurumi' in tags:
            best_for = 'Amigurumi, Toys, 3D projects'
        elif 'lace' in tags:
            best_for = 'Shawls, Doilies, Lightweight garments'
        elif 'texture' in tags:
            best_for = 'Blankets, Sweaters, Home decor'
        elif 'basic' in tags:
            best_for = 'Dishcloths, Scarves, Beginner projects'
        else:
            best_for = 'Various projects'
        
        # Update row
        if diff_idx >= 0:
            row[diff_idx] = difficulty
        if time_idx >= 0:
            row[time_idx] = time_to_learn
        if mistakes_idx >= 0:
            row[mistakes_idx] = mistakes
        if tips_idx >= 0:
            row[tips_idx] = tips
        if best_idx >= 0:
            row[best_idx] = best_for
        
        updates.append(row)
    
    # Batch update all rows
    if updates:
        range_name = f'Sheet1!A2:{chr(65 + len(headers) - 1)}{len(updates) + 1}'
        body = {
            'values': updates
        }
        
        sheets.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Enhanced {len(updates)} terms!")

def suggest_missing_terms():
    """Print suggestions for missing terms"""
    print("\n=== SUGGESTED TERMS TO ADD ===")
    
    suggestions = {
        "Modern Techniques": [
            "c2c - Corner to Corner crochet",
            "graphgan - Graph-based afghan technique",
            "overlay - Overlay crochet for 3D effects",
            "mosaic - Mosaic colorwork technique",
            "pooling - Planned color pooling"
        ],
        "Community Terms": [
            "frogging - Ripping out work (rip it, rip it)",
            "yarn chicken - Racing to finish before running out",
            "sable - Stash Acquisition Beyond Life Expectancy",
            "wip - Work In Progress",
            "cal - Crochet Along event",
            "kal - Knit Along (for mixed crafters)",
            "ufo - UnFinished Object"
        ],
        "Construction": [
            "russian join - Invisible yarn joining",
            "spit splice - Felted yarn join",
            "magic knot - Secure yarn joining",
            "jogless - Seamless color changes",
            "provisional - Temporary foundation"
        ]
    }
    
    for category, terms in suggestions.items():
        print(f"\n{category}:")
        for term in terms:
            print(f"  • {term}")

def main():
    print("DANI'S Glossary Enhancement Tool")
    print("================================")
    
    # Initialize Sheets API
    sheets = get_sheets_service()
    
    # Analyze current data
    headers, data = analyze_glossary(sheets)
    
    # Add enhancement columns if needed
    updated_headers = add_enhancement_columns(sheets, headers)
    
    # Enhance terms
    enhance_terms(sheets, updated_headers, data)
    
    # Suggest missing terms
    suggest_missing_terms()
    
    print("\n✅ Enhancement complete!")
    print("\nNext steps:")
    print("1. Review the enhanced data in your Google Sheet")
    print("2. Run export_to_glossarydata.py to update your website")
    print("3. Consider adding the suggested missing terms")

if __name__ == "__main__":
    main()