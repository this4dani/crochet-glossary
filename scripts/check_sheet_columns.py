#!/usr/bin/env python3
"""
Check the actual column structure in Google Sheets
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

def check_columns():
    """Display column structure and sample data"""
    sheets = get_sheets_service()
    
    # Get headers and first few rows
    result = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A1:Z5'
    ).execute()
    
    values = result.get('values', [])
    if not values:
        print("No data found!")
        return
        
    headers = values[0]
    
    print("=== COLUMN STRUCTURE ===\n")
    print("Index | Column Name")
    print("-" * 30)
    for i, header in enumerate(headers):
        print(f"{i:5} | {header}")
    
    print("\n=== SAMPLE DATA (First Row) ===\n")
    if len(values) > 1:
        first_row = values[1]
        for i, header in enumerate(headers):
            if i < len(first_row):
                value = first_row[i][:50] + "..." if len(first_row[i]) > 50 else first_row[i]
                print(f"{header}: {value}")
    
    print("\n=== EXPORT SCRIPT MAPPING ===")
    print("The export script currently uses:")
    print("  row[0] -> id")
    print("  row[2] -> name_us")
    print("  row[3] -> name_uk")
    print("  row[4] -> symbol")
    print("  row[6] -> tags")
    print("  row[7] -> notes (Description)")

if __name__ == "__main__":
    check_columns()