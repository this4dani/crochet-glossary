#!/usr/bin/env python3
"""
Validate DANI'S glossary data for accuracy and completeness
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
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

def validate_glossary():
    """Check glossary data quality"""
    sheets = get_sheets_service()
    
    # Get all data
    result = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:Z'
    ).execute()
    
    values = result.get('values', [])
    headers = values[0]
    data = values[1:]
    
    print(f"\n=== GLOSSARY VALIDATION REPORT ===")
    print(f"Total terms: {len(data)}")
    
    # Find column indices
    id_idx = headers.index('ID') if 'ID' in headers else 0
    us_idx = headers.index('Name_US') if 'Name_US' in headers else -1
    uk_idx = headers.index('Name_UK') if 'Name_UK' in headers else -1
    desc_idx = headers.index('Description') if 'Description' in headers else -1
    diff_idx = headers.index('Difficulty') if 'Difficulty' in headers else -1
    time_idx = headers.index('Time_To_Learn') if 'Time_To_Learn' in headers else -1
    
    # Track issues
    missing_desc = []
    missing_difficulty = []
    missing_time = []
    duplicate_ids = []
    
    # Check each term
    id_counts = Counter()
    
    for i, row in enumerate(data):
        term_id = row[id_idx] if len(row) > id_idx else ''
        id_counts[term_id] += 1
        
        # Check for missing descriptions
        if desc_idx >= 0 and (len(row) <= desc_idx or not row[desc_idx].strip()):
            missing_desc.append(f"{term_id} - {row[us_idx] if len(row) > us_idx else 'Unknown'}")
        
        # Check for missing difficulty
        if diff_idx >= 0 and (len(row) <= diff_idx or not row[diff_idx].strip()):
            missing_difficulty.append(f"{term_id} - {row[us_idx] if len(row) > us_idx else 'Unknown'}")
        
        # Check for missing time
        if time_idx >= 0 and (len(row) <= time_idx or not row[time_idx].strip()):
            missing_time.append(f"{term_id} - {row[us_idx] if len(row) > us_idx else 'Unknown'}")
    
    # Find duplicates
    duplicates = [id for id, count in id_counts.items() if count > 1]
    
    # Print report
    print(f"\n✅ GOOD DATA:")
    print(f"  • Terms with descriptions: {len(data) - len(missing_desc)}")
    print(f"  • Terms with difficulty: {len(data) - len(missing_difficulty)}")
    print(f"  • Terms with time estimates: {len(data) - len(missing_time)}")
    
    if duplicates:
        print(f"\n❌ DUPLICATE IDs ({len(duplicates)}):")
        for dup in duplicates[:5]:  # Show first 5
            print(f"  • {dup} appears {id_counts[dup]} times")
    
    if missing_desc:
        print(f"\n⚠️  MISSING DESCRIPTIONS ({len(missing_desc)}):")
        for term in missing_desc[:10]:  # Show first 10
            print(f"  • {term}")
        if len(missing_desc) > 10:
            print(f"  ... and {len(missing_desc) - 10} more")
    
    if missing_difficulty:
        print(f"\n⚠️  MISSING DIFFICULTY ({len(missing_difficulty)}):")
        for term in missing_difficulty[:10]:  # Show first 10
            print(f"  • {term}")
        if len(missing_difficulty) > 10:
            print(f"  ... and {len(missing_difficulty) - 10} more")
    
    # Summary
    print(f"\n=== SUMMARY ===")
    completeness = ((len(data) - len(missing_desc)) / len(data)) * 100
    print(f"Data completeness: {completeness:.1f}%")
    
    if completeness == 100:
        print("🎉 Your glossary data is PERFECT!")
    elif completeness > 90:
        print("✅ Your glossary is in great shape!")
    else:
        print("💡 Consider adding missing descriptions for better user experience")

if __name__ == "__main__":
    validate_glossary()
    