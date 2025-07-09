#!/usr/bin/env python3
"""
Fix duplicate names in glossary by identifying and removing duplicates
"""
import sys
sys.path.append('..')

from google.oauth2 import service_account
from googleapiclient.discovery import build
from collections import defaultdict

SPREADSHEET_ID = '1WXt17J7Bn7nuRG3SV1HvvoWX4mvgZmY7dAeLRIlIh3A'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def get_sheets_service():
    """Initialize Google Sheets API service"""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()

def find_and_show_duplicates():
    """Find duplicate names and show details for decision making"""
    sheets = get_sheets_service()
    
    # Get all data
    result = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:Z'
    ).execute()
    
    values = result.get('values', [])
    headers = values[0]
    data = values[1:]
    
    # Get column indices
    id_idx = headers.index('ID')
    name_us_idx = headers.index('Name_US')
    desc_idx = headers.index('Description')
    tags_idx = headers.index('Tags') if 'Tags' in headers else -1
    
    # Find duplicates
    name_to_rows = defaultdict(list)
    
    for i, row in enumerate(data):
        row_num = i + 2  # Account for header and 0-index
        name_us = row[name_us_idx] if len(row) > name_us_idx else ''
        
        if name_us:
            name_to_rows[name_us.lower()].append({
                'row_num': row_num,
                'id': row[id_idx] if len(row) > id_idx else '',
                'name': name_us,
                'desc': row[desc_idx] if len(row) > desc_idx else '',
                'tags': row[tags_idx] if tags_idx >= 0 and len(row) > tags_idx else ''
            })
    
    # Show duplicates
    duplicates_found = False
    duplicate_names = [
        'slip knot', 'fasten off', 'crab stitch', 'weave in ends',
        'spike stitch', 'bavarian crochet', 'bead crochet', 
        'filet crochet', 'hyperbolic crochet', 'overlay crochet'
    ]
    
    print("=== DUPLICATE NAME ANALYSIS ===\n")
    
    for name in duplicate_names:
        if name in name_to_rows and len(name_to_rows[name]) > 1:
            duplicates_found = True
            print(f"\n'{name.upper()}' found {len(name_to_rows[name])} times:")
            print("-" * 60)
            
            for entry in name_to_rows[name]:
                print(f"Row {entry['row_num']}:")
                print(f"  ID: {entry['id']}")
                print(f"  Description: {entry['desc'][:100]}{'...' if len(entry['desc']) > 100 else ''}")
                print(f"  Tags: {entry['tags']}")
                print()
    
    if not duplicates_found:
        print("No duplicates found!")
        return
    
    # Also check for missing essential terms
    print("\n=== MISSING ESSENTIAL TERMS ===")
    print("\nThese fundamental stitches appear to be missing:")
    essential_missing = ['sc', 'dc', 'hdc', 'tr', 'ch', 'slst']
    
    existing_ids = [row[id_idx].lower() for row in data if len(row) > id_idx]
    
    for term_id in essential_missing:
        if term_id not in existing_ids:
            print(f"  • {term_id}")
    
    print("\nNote: Some of these might exist with different IDs.")
    print("Check if 'sc' exists as 'single-crochet' or similar variants.")

def remove_duplicate_rows(rows_to_delete):
    """Remove specific rows from the sheet"""
    sheets = get_sheets_service()
    
    # Sort rows in descending order to delete from bottom up
    rows_to_delete.sort(reverse=True)
    
    # Get sheet ID
    sheet_metadata = sheets.get(spreadsheetId=SPREADSHEET_ID).execute()
    sheet_id = sheet_metadata['sheets'][0]['properties']['sheetId']
    
    # Create delete requests
    requests = []
    for row_num in rows_to_delete:
        requests.append({
            'deleteDimension': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'ROWS',
                    'startIndex': row_num - 1,  # 0-indexed
                    'endIndex': row_num
                }
            }
        })
    
    # Execute batch update
    if requests:
        body = {'requests': requests}
        sheets.batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()
        
        print(f"\n✅ Deleted {len(rows_to_delete)} duplicate rows")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--delete':
        if len(sys.argv) > 2:
            rows_to_delete = [int(r) for r in sys.argv[2].split(',')]
            print(f"Deleting rows: {rows_to_delete}")
            remove_duplicate_rows(rows_to_delete)
        else:
            print("Error: Please specify rows to delete")
            print("Usage: python fix_duplicate_names.py --delete 123,456,789")
    else:
        print("Duplicate Name Analysis")
        print("=" * 60)
        
        find_and_show_duplicates()
        
        print("\n" + "=" * 60)
        print("\nTo remove duplicates:")
        print("1. Review the duplicate entries above")
        print("2. Note the row numbers to delete")
        print("3. Run: python fix_duplicate_names.py --delete 123,456,789")
        print("\nNote: Check if missing terms exist with different IDs.")