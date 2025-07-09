#!/usr/bin/env python3
"""
Validate glossary data for duplicates and errors
"""
import sys
sys.path.append('..')

from google.oauth2 import service_account
from googleapiclient.discovery import build
from collections import Counter
import re

SPREADSHEET_ID = '1WXt17J7Bn7nuRG3SV1HvvoWX4mvgZmY7dAeLRIlIh3A'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def get_sheets_service():
    """Initialize Google Sheets API service"""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()

def check_glossary_quality():
    """Comprehensive quality check for glossary data"""
    sheets = get_sheets_service()
    
    # Get all data
    result = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:Z'
    ).execute()
    
    values = result.get('values', [])
    if not values:
        print("❌ No data found in sheet!")
        return
        
    headers = values[0]
    data = values[1:]
    
    print("=== GLOSSARY QUALITY CHECK ===\n")
    print(f"Total rows: {len(data)}")
    print(f"Headers: {', '.join(headers)}\n")
    
    # Find column indices
    try:
        id_idx = headers.index('ID')
        name_us_idx = headers.index('Name_US')
        name_uk_idx = headers.index('Name_UK')
        desc_idx = headers.index('Description')
        symbol_idx = headers.index('Symbol') if 'Symbol' in headers else -1
        tags_idx = headers.index('Tags') if 'Tags' in headers else -1
    except ValueError as e:
        print(f"❌ Missing required column: {e}")
        return
    
    # Track duplicates and errors
    id_counts = Counter()
    name_counts = Counter()
    duplicate_rows = {}
    errors = []
    empty_descriptions = []
    
    # Check each row
    for i, row in enumerate(data):
        row_num = i + 2  # Account for header and 0-index
        
        # Get values safely
        term_id = row[id_idx] if len(row) > id_idx else ''
        name_us = row[name_us_idx] if len(row) > name_us_idx else ''
        name_uk = row[name_uk_idx] if len(row) > name_uk_idx else ''
        desc = row[desc_idx] if len(row) > desc_idx else ''
        
        # Skip empty rows
        if not term_id and not name_us:
            continue
            
        # Count occurrences
        if term_id:
            id_counts[term_id] += 1
            if term_id in duplicate_rows:
                duplicate_rows[term_id].append(row_num)
            else:
                duplicate_rows[term_id] = [row_num]
                
        if name_us:
            name_counts[name_us.lower()] += 1
        
        # Quality checks
        if name_us:
            # Check for double spaces
            if '  ' in name_us or (desc and '  ' in desc):
                errors.append(f"Row {row_num}: Double spaces in '{name_us}'")
            
            # Check for leading/trailing spaces
            if name_us != name_us.strip():
                errors.append(f"Row {row_num}: Extra spaces in '{name_us}'")
            
            # Check for empty descriptions
            if not desc or desc.strip() == '':
                empty_descriptions.append(f"Row {row_num}: '{name_us}' has no description")
            
            # Check US/UK terminology alignment
            if term_id in ['sc', 'dc', 'hdc', 'tr']:
                # Basic stitches should have different UK names
                if name_us.lower() == name_uk.lower():
                    errors.append(f"Row {row_num}: US/UK should differ for '{name_us}'")
    
    # Report findings
    print("🔍 DUPLICATE CHECK:\n")
    
    # Report duplicate IDs
    duplicate_ids = [(term_id, count) for term_id, count in id_counts.items() if count > 1]
    if duplicate_ids:
        print("❌ DUPLICATE IDs FOUND:")
        for term_id, count in sorted(duplicate_ids):
            rows = duplicate_rows[term_id]
            print(f"  • '{term_id}' appears {count} times in rows: {', '.join(map(str, rows))}")
    else:
        print("✅ No duplicate IDs found")
    
    # Report duplicate names
    print("\n🔍 DUPLICATE NAMES CHECK:\n")
    duplicate_names = [(name, count) for name, count in name_counts.items() if count > 1]
    if duplicate_names:
        print("❌ DUPLICATE NAMES FOUND:")
        for name, count in sorted(duplicate_names):
            print(f"  • '{name}' appears {count} times")
    else:
        print("✅ No duplicate names found")
    
    # Report data quality issues
    if errors:
        print("\n❌ DATA QUALITY ISSUES:")
        for error in errors[:20]:  # Show first 20
            print(f"  • {error}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more issues")
    
    if empty_descriptions:
        print(f"\n⚠️  MISSING DESCRIPTIONS: {len(empty_descriptions)} terms have no description")
        for item in empty_descriptions[:10]:
            print(f"  • {item}")
        if len(empty_descriptions) > 10:
            print(f"  ... and {len(empty_descriptions) - 10} more")
    
    # Summary statistics
    print("\n📊 SUMMARY:")
    print(f"  Total terms: {len(data)}")
    print(f"  Unique IDs: {len(id_counts)}")
    print(f"  Unique names: {len(name_counts)}")
    print(f"  Duplicate IDs: {len(duplicate_ids)}")
    print(f"  Data quality issues: {len(errors)}")
    print(f"  Missing descriptions: {len(empty_descriptions)}")
    
    # Final verdict
    print("\n🎯 VERDICT:")
    if len(duplicate_ids) == 0 and len(errors) == 0 and len(empty_descriptions) == 0:
        print("✅ Glossary data is clean and ready!")
    else:
        print("❌ Issues found. Review and fix before launch.")
        
def check_authority_alignment():
    """Check alignment with standard crochet terminology"""
    print("\n\n=== AUTHORITY STANDARDS CHECK ===\n")
    
    # Craft Yarn Council standard terms
    AUTHORITY_TERMS = {
        'sc': {'us': 'single crochet', 'uk': 'double crochet'},
        'dc': {'us': 'double crochet', 'uk': 'treble crochet'},
        'hdc': {'us': 'half double crochet', 'uk': 'half treble crochet'},
        'tr': {'us': 'treble crochet', 'uk': 'double treble crochet'},
        'dtr': {'us': 'double treble crochet', 'uk': 'triple treble crochet'},
        'sl st': {'us': 'slip stitch', 'uk': 'slip stitch'},
        'slst': {'us': 'slip stitch', 'uk': 'slip stitch'},
        'ch': {'us': 'chain', 'uk': 'chain'},
        'yo': {'us': 'yarn over', 'uk': 'yarn over hook'},
        'sk': {'us': 'skip', 'uk': 'miss'},
        'sp': {'us': 'space', 'uk': 'space'},
        'tog': {'us': 'together', 'uk': 'together'},
    }
    
    sheets = get_sheets_service()
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
    
    # Check alignment
    misalignments = []
    
    for row in data:
        term_id = row[id_idx] if len(row) > id_idx else ''
        name_us = row[name_us_idx] if len(row) > name_us_idx else ''
        name_uk = row[name_uk_idx] if len(row) > name_uk_idx else ''
        
        if term_id in AUTHORITY_TERMS:
            expected = AUTHORITY_TERMS[term_id]
            if name_us.lower() != expected['us'].lower():
                misalignments.append(f"ID '{term_id}': US name is '{name_us}', expected '{expected['us']}'")
            if name_uk.lower() != expected['uk'].lower():
                misalignments.append(f"ID '{term_id}': UK name is '{name_uk}', expected '{expected['uk']}'")
    
    if misalignments:
        print("❌ TERMINOLOGY MISALIGNMENTS WITH CRAFT YARN COUNCIL:")
        for issue in misalignments:
            print(f"  • {issue}")
    else:
        print("✅ All checked terms align with Craft Yarn Council standards!")
    
    # Check for essential missing terms
    glossary_ids = [row[id_idx] for row in data if len(row) > id_idx]
    missing_essential = []
    
    for auth_id in AUTHORITY_TERMS:
        if auth_id not in glossary_ids and auth_id.replace(' ', '') not in glossary_ids:
            missing_essential.append(f"{auth_id} ({AUTHORITY_TERMS[auth_id]['us']})")
    
    if missing_essential:
        print("\n⚠️  MISSING ESSENTIAL TERMS:")
        for term in missing_essential:
            print(f"  • {term}")

if __name__ == "__main__":
    print("Glossary Data Validator")
    print("=" * 50)
    
    check_glossary_quality()
    check_authority_alignment()
    
    print("\n" + "=" * 50)
    print("Validation complete.")