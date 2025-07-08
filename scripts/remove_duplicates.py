#!/usr/bin/env python3
"""
Remove duplicate terms from Google Sheet
"""

import sys
sys.path.append('..')

from google.oauth2 import service_account
from googleapiclient.discovery import build

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

def find_and_show_duplicates(sheets):
    """Find duplicates and show details"""
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
    
    # Find column indices
    id_idx = headers.index('ID')
    name_us_idx = headers.index('Name_US')
    name_uk_idx = headers.index('Name_UK')
    status_idx = headers.index('Status') if 'Status' in headers else -1
    
    # Find duplicates
    seen = {}
    duplicates = []
    
    for i, row in enumerate(data):
        if len(row) > id_idx:
            term_id = row[id_idx].upper()  # Normalize to uppercase
            name_us = row[name_us_idx] if len(row) > name_us_idx else ''
            name_uk = row[name_uk_idx] if len(row) > name_uk_idx else ''
            status = row[status_idx] if status_idx >= 0 and len(row) > status_idx else ''
            
            if term_id in seen:
                # Found a duplicate
                duplicates.append({
                    'id': term_id,
                    'row1': seen[term_id]['row'] + 2,  # +2 for header and 0-index
                    'row2': i + 2,
                    'name1': seen[term_id]['name'],
                    'name2': name_us,
                    'status1': seen[term_id]['status'],
                    'status2': status
                })
            else:
                seen[term_id] = {
                    'row': i,
                    'name': name_us,
                    'status': status
                }
    
    print(f"\n=== DUPLICATE ANALYSIS ===")
    print(f"Found {len(duplicates)} duplicate IDs:\n")
    
    for dup in duplicates:
        print(f"ID: {dup['id']}")
        print(f"  Row {dup['row1']}: {dup['name1']} (Status: {dup['status1']})")
        print(f"  Row {dup['row2']}: {dup['name2']} (Status: {dup['status2']})")
        print()
    
    return duplicates, headers, data

def remove_duplicates(sheets, duplicates):
    """Remove duplicate rows, keeping the first occurrence"""
    if not duplicates:
        print("No duplicates to remove!")
        return
    
    response = input("\nDo you want to remove duplicate rows (keeping the first occurrence)? (y/n): ")
    if response.lower() != 'y':
        print("Skipping duplicate removal.")
        return
    
    # Get rows to delete (keeping the first, removing the second)
    rows_to_delete = sorted([dup['row2'] for dup in duplicates], reverse=True)
    
    print(f"\nRemoving {len(rows_to_delete)} duplicate rows...")
    
    # Delete rows one by one, starting from bottom
    for row_num in rows_to_delete:
        request = {
            'deleteDimension': {
                'range': {
                    'sheetId': 0,
                    'dimension': 'ROWS',
                    'startIndex': row_num - 1,  # 0-indexed
                    'endIndex': row_num
                }
            }
        }
        
        sheets.batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={'requests': [request]}
        ).execute()
        
        print(f"  Deleted row {row_num}")
    
    print("\n✅ Duplicates removed!")

def main():
    print("DANI'S Duplicate Removal Tool")
    print("=============================")
    
    # Initialize Sheets API
    sheets = get_sheets_service()
    
    # Find and show duplicates
    duplicates, headers, data = find_and_show_duplicates(sheets)
    
    if duplicates:
        # Offer to remove duplicates
        remove_duplicates(sheets, duplicates)
        
        print("\nNext steps:")
        print("1. Run export_to_glossarydata.py to update your website")
        print("2. Check your glossary page to verify duplicates are gone")
    else:
        print("\n✅ No duplicates found! Your glossary is clean.")

if __name__ == "__main__":
    main()