#!/usr/bin/env python3
"""
Export Google Sheets data back to glossarydata.js
This will update your website with all 255 terms!
"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Your spreadsheet ID
SPREADSHEET_ID = '1WXt17J7Bn7nuRG3SV1HvvoWX4mvgZmY7dAeLRIlIh3A'

# Service account credentials
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_sheets_service():
    """Initialize Google Sheets service"""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service

def export_to_js():
    """Export sheet data to glossarydata.js format"""
    service = get_sheets_service()
    sheet = service.spreadsheets()
    
    # Get all data from the sheet
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:I'  # Columns A through I
    ).execute()
    
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
        return
    
    # Skip header row and process data
    terms = []
    for row in values[1:]:  # Skip first row (headers)
        if len(row) >= 8:  # Make sure we have enough columns
            term = {
                'id': row[0].lower(),  # ID in lowercase
                'name_us': row[2],
                'name_uk': row[3],
                'symbol': row[4] if len(row) > 4 and row[4] else row[0].lower(),
                'tags': [tag.strip() for tag in row[6].split(',')] if len(row) > 6 and row[6] else [],
                'notes': row[7] if len(row) > 7 and row[7] else ''
            }
            
            # Only add if we have the required fields
            if term['id'] and term['name_us'] and term['name_uk']:
                terms.append(term)
    
    # Create the JavaScript file content
    js_content = """export const stitchGlossary = [
"""
    
    for i, term in enumerate(terms):
        js_content += "  {\n"
        js_content += f'    id: "{term["id"]}",\n'
        js_content += f'    name_us: "{term["name_us"]}",\n'
        js_content += f'    name_uk: "{term["name_uk"]}",\n'
        js_content += f'    symbol: "{term["symbol"]}",\n'
        js_content += f'    tags: {json.dumps(term["tags"])},\n'
        js_content += f'    notes: "{term["notes"]}"\n'
        js_content += "  }"
        
        if i < len(terms) - 1:
            js_content += ","
        js_content += "\n"
    
    js_content += "];"
    
    # Write to file
    with open('glossarydata.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ Successfully exported {len(terms)} terms to glossarydata.js")
    print("\nNext steps:")
    print("1. Check glossarydata.js to verify the export")
    print("2. Commit and push to GitHub:")
    print("   git add glossarydata.js")
    print("   git commit -m 'Update glossary to 255 terms'")
    print("   git push")
    print("3. Your website should update automatically!")
    
    # Show sample of exported data
    print(f"\nFirst few terms exported:")
    for term in terms[:3]:
        print(f"  - {term['name_us']} ({term['id']})")
    print(f"  ... and {len(terms) - 3} more!")

def main():
    """Main function"""
    print("Exporting Google Sheets data to glossarydata.js...")
    print(f"Sheet ID: {SPREADSHEET_ID}")
    
    try:
        export_to_js()
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure credentials.json is in the same directory")
        print("2. Check that the sheet ID is correct")
        print("3. Verify the service account has read access to the sheet")

if __name__ == "__main__":
    main()
    