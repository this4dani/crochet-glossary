#!/usr/bin/env python3
"""
Check if basic stitches exist with different IDs
"""
import sys
sys.path.append('..')

from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = '1WXt17J7Bn7nuRG3SV1HvvoWX4mvgZmY7dAeLRIlIh3A'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def get_sheets_service():
    """Initialize Google Sheets API service"""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()

def find_essential_stitches():
    """Search for basic stitches that might have different IDs"""
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
    name_uk_idx = headers.index('Name_UK')
    
    # Standard stitch abbreviations from Craft Yarn Council
    essential_stitches = {
        'single crochet': 'sc',
        'double crochet': 'dc',
        'half double crochet': 'hdc',
        'treble crochet': 'tr',
        'chain': 'ch',
        'slip stitch': 'slst',
        'yarn over': 'yo',
        'skip': 'sk',
        'space': 'sp',
        'together': 'tog'
    }
    
    print("=== SEARCHING FOR BASIC STITCHES ===\n")
    
    found_stitches = {}
    all_ids = []
    
    # Check each row
    for row in data:
        term_id = row[id_idx] if len(row) > id_idx else ''
        name_us = row[name_us_idx] if len(row) > name_us_idx else ''
        
        all_ids.append(term_id)
        
        # Check if this is a basic stitch
        for stitch_name, expected_id in essential_stitches.items():
            if stitch_name in name_us.lower():
                if stitch_name not in found_stitches:
                    found_stitches[stitch_name] = []
                found_stitches[stitch_name].append({
                    'id': term_id,
                    'name': name_us,
                    'expected_id': expected_id
                })
    
    # Report findings
    print("Basic stitches found:\n")
    for stitch_name, entries in found_stitches.items():
        print(f"'{stitch_name}':")
        for entry in entries:
            status = "✅" if entry['id'] == entry['expected_id'] else "⚠️"
            print(f"  {status} ID: '{entry['id']}' - {entry['name']}")
            if entry['id'] != entry['expected_id']:
                print(f"     (Standard ID: '{entry['expected_id']}')")
        print()
    
    # Check what's missing
    print("\nBasic stitches NOT found:")
    for stitch_name, expected_id in essential_stitches.items():
        if stitch_name not in found_stitches:
            print(f"  ❌ {stitch_name} (standard ID: {expected_id})")
    
    # Show existing IDs with common prefixes
    print("\n\nExisting IDs with common abbreviations:")
    common_prefixes = ['sc', 'dc', 'hdc', 'tr', 'ch', 'sl', 'yo', 'sk', 'sp', 'tog']
    
    for prefix in common_prefixes:
        matching_ids = [id for id in all_ids if id.startswith(prefix)]
        if matching_ids:
            print(f"\n'{prefix}*': {', '.join(matching_ids)}")

if __name__ == "__main__":
    find_essential_stitches()