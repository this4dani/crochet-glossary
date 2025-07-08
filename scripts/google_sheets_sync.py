#!/usr/bin/env python3
"""
Google Sheets Integration for DANI'S Crochet Glossary
Syncs between Google Sheets and glossarydata.js
"""

import json
import os
import re
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd

# Configuration
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID_HERE'  # You'll get this after creating the sheet
RANGE_NAME = 'Terms!A:Z'  # Adjust based on your sheet structure
CREDENTIALS_FILE = 'credentials.json'  # Your Google service account key

# Set up credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GlossarySync:
    def __init__(self):
        self.creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES
        )
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = self.service.spreadsheets()
    
    def create_glossary_sheet(self):
        """Create a new Google Sheet with proper structure"""
        spreadsheet = {
            'properties': {
                'title': "DANI'S Crochet Glossary - Master Database"
            },
            'sheets': [
                {
                    'properties': {
                        'title': 'Terms',
                        'gridProperties': {
                            'rowCount': 500,
                            'columnCount': 30
                        }
                    }
                },
                {
                    'properties': {
                        'title': 'Categories',
                    }
                },
                {
                    'properties': {
                        'title': 'Progress',
                    }
                }
            ]
        }
        
        sheet = self.service.spreadsheets().create(
            body=spreadsheet,
            fields='spreadsheetId'
        ).execute()
        
        print(f"Created new spreadsheet with ID: {sheet.get('spreadsheetId')}")
        return sheet.get('spreadsheetId')
    
    def setup_headers(self):
        """Set up the header row with all necessary columns"""
        headers = [
            ['ID', 'Status', 'Priority', 'Category', 'Subcategory', 
             'Name_US', 'Name_UK', 'Abbrev_US', 'Abbrev_UK', 
             'Symbol', 'Unicode', 'SVG_Path',
             'Description_Brief', 'Description_Full', 
             'Instructions_1', 'Instructions_2', 'Instructions_3',
             'Tags', 'Common_Uses', 'Related_Terms',
             'Video_URL', 'Image_URL', 
             'Added_Date', 'Modified_Date', 'Verified',
             'Translation_FR', 'Translation_ES', 'Translation_DE',
             'Notes', 'Source']
        ]
        
        body = {
            'values': headers
        }
        
        self.sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='Terms!A1:AD1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        # Format headers
        requests = [{
            'repeatCell': {
                'range': {
                    'sheetId': 0,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.2, 'green': 0.2, 'blue': 0.5},
                        'textFormat': {
                            'foregroundColor': {'red': 1, 'green': 1, 'blue': 1},
                            'bold': True
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        }]
        
        self.sheet.batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={'requests': requests}
        ).execute()
    
    def import_from_glossarydata(self, filepath='glossarydata.js'):
        """Import existing terms from glossarydata.js"""
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Extract the array content
        match = re.search(r'export const stitchGlossary = \[(.*?)\];', content, re.DOTALL)
        if not match:
            print("Could not parse glossarydata.js")
            return
        
        # Parse JavaScript objects (simplified - you might need more robust parsing)
        terms = []
        js_objects = re.findall(r'\{([^}]+)\}', match.group(1))
        
        for obj in js_objects:
            term = {}
            # Extract fields
            id_match = re.search(r'id:\s*"([^"]+)"', obj)
            if id_match:
                term['ID'] = id_match.group(1)
            
            name_us_match = re.search(r'name_us:\s*"([^"]+)"', obj)
            if name_us_match:
                term['Name_US'] = name_us_match.group(1)
                
            name_uk_match = re.search(r'name_uk:\s*"([^"]+)"', obj)
            if name_uk_match:
                term['Name_UK'] = name_uk_match.group(1)
                
            symbol_match = re.search(r'symbol:\s*"([^"]+)"', obj)
            if symbol_match:
                term['Symbol'] = symbol_match.group(1)
                
            notes_match = re.search(r'notes:\s*"([^"]+)"', obj)
            if notes_match:
                term['Description_Brief'] = notes_match.group(1)
            
            # Extract tags
            tags_match = re.search(r'tags:\s*\[([^\]]+)\]', obj)
            if tags_match:
                tags = tags_match.group(1).replace('"', '').replace("'", '')
                term['Tags'] = tags
            
            if term:
                term['Status'] = 'Existing'
                term['Added_Date'] = '2024-01-01'
                terms.append(term)
        
        return terms
    
    def push_to_sheets(self, terms):
        """Push terms to Google Sheets"""
        # Convert to rows
        rows = []
        columns = ['ID', 'Status', 'Priority', 'Category', 'Subcategory', 
                   'Name_US', 'Name_UK', 'Abbrev_US', 'Abbrev_UK', 
                   'Symbol', 'Unicode', 'SVG_Path',
                   'Description_Brief', 'Description_Full', 
                   'Instructions_1', 'Instructions_2', 'Instructions_3',
                   'Tags', 'Common_Uses', 'Related_Terms',
                   'Video_URL', 'Image_URL', 
                   'Added_Date', 'Modified_Date', 'Verified',
                   'Translation_FR', 'Translation_ES', 'Translation_DE',
                   'Notes', 'Source']
        
        for term in terms:
            row = []
            for col in columns:
                row.append(term.get(col, ''))
            rows.append(row)
        
        body = {'values': rows}
        
        result = self.sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='Terms!A2:AD' + str(len(rows) + 1),
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"Updated {result.get('updatedRows')} rows")
    
    def pull_from_sheets(self):
        """Pull current data from Google Sheets"""
        result = self.sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()
        
        values = result.get('values', [])
        if not values:
            print('No data found.')
            return []
        
        # Convert to list of dictionaries
        headers = values[0]
        terms = []
        for row in values[1:]:
            term = {}
            for i, header in enumerate(headers):
                if i < len(row):
                    term[header] = row[i]
            if term.get('ID'):  # Only include if has ID
                terms.append(term)
        
        return terms
    
    def export_to_glossarydata(self, terms, filepath='glossarydata_new.js'):
        """Export terms back to glossarydata.js format"""
        output = 'export const stitchGlossary = [\n'
        
        # Group by category for organization
        categories = {}
        for term in terms:
            cat = term.get('Category', 'Other')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(term)
        
        for category, cat_terms in categories.items():
            output += f'  // === {category.upper()} ===\n'
            
            for term in cat_terms:
                output += '  {\n'
                output += f'    id: "{term.get("ID", "")}",\n'
                output += f'    name_us: "{term.get("Name_US", "")}",\n'
                output += f'    name_uk: "{term.get("Name_UK", "")}",\n'
                
                if term.get('Symbol'):
                    output += f'    symbol: "{term["Symbol"]}",\n'
                
                if term.get('Tags'):
                    tags = term['Tags'].split(',')
                    tags_formatted = ', '.join([f'"{tag.strip()}"' for tag in tags])
                    output += f'    tags: [{tags_formatted}],\n'
                
                if term.get('Description_Brief'):
                    output += f'    notes: "{term["Description_Brief"]}"\n'
                
                output += '  },\n'
        
        output += '];\n'
        
        with open(filepath, 'w') as f:
            f.write(output)
        
        print(f"Exported {len(terms)} terms to {filepath}")
    
    def add_missing_core_terms(self):
        """Add the core terms that are missing"""
        missing_terms = [
            {
                'ID': 'DTR',
                'Status': 'New',
                'Priority': 'High',
                'Category': 'Basic',
                'Name_US': 'Double Treble Crochet',
                'Name_UK': 'Triple Treble Crochet',
                'Abbrev_US': 'dtr',
                'Abbrev_UK': 'trtr',
                'Symbol': 'TTT',
                'Description_Brief': 'Very tall stitch with 2 yarn overs',
                'Tags': 'basic, tall, advanced',
                'Added_Date': '2024-07-06'
            },
            # Add more terms here
        ]
        
        return missing_terms

# Usage example
if __name__ == "__main__":
    sync = GlossarySync()
    
    # First time setup:
    # sheet_id = sync.create_glossary_sheet()
    # print(f"Update SPREADSHEET_ID to: {sheet_id}")
    # sync.setup_headers()
    
    # Import existing terms
    existing_terms = sync.import_from_glossarydata()
    print(f"Found {len(existing_terms)} existing terms")
    
    # Add missing terms
    missing_terms = sync.add_missing_core_terms()
    all_terms = existing_terms + missing_terms
    
    # Push to sheets
    sync.push_to_sheets(all_terms)
    
    # Later: Pull from sheets and export
    # updated_terms = sync.pull_from_sheets()
    # sync.export_to_glossarydata(updated_terms)