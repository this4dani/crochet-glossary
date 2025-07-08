#!/usr/bin/env python3
"""
Add PURE CROCHET terms to Google Sheets glossary - NO KNITTING!
Run this in your /scripts folder
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

# PURE CROCHET TERMS ONLY!
crochet_only_terms = [
    # === COMMUNITY SLANG (CROCHET SPECIFIC) ===
    {
        'ID': 'hoth',
        'Status': 'New',
        'Name_US': 'Hot Off The Hook',
        'Name_UK': 'Hot Off The Hook',
        'Symbol': 'HOTH',
        'Category': 'slang',
        'Tags': 'community, finished, pride',
        'Description': 'Just-finished crochet project you\'re excited to show off',
        'Difficulty': '1',
        'Time_To_Learn': 'Instant',
        'Best_For': 'Sharing accomplishments',
        'Common_Mistakes': 'N/A',
        'Pro_Tips': 'Take photos in good lighting before use'
    },
    {
        'ID': 'foth',
        'Status': 'New',
        'Name_US': 'Fresh Off The Hook',
        'Name_UK': 'Fresh Off The Hook',
        'Symbol': 'FOTH',
        'Category': 'slang',
        'Tags': 'community, finished, pride',
        'Description': 'Alternative to HOTH - newly completed crochet project',
        'Difficulty': '1',
        'Time_To_Learn': 'Instant',
        'Best_For': 'Social media posts'
    },
    {
        'ID': 'hooker',
        'Status': 'New',
        'Name_US': 'Hooker',
        'Name_UK': 'Hooker',
        'Symbol': 'Hooker',
        'Category': 'slang',
        'Tags': 'community, humor, crocheter',
        'Description': 'Playful term for someone who crochets (uses a hook)',
        'Difficulty': '1',
        'Time_To_Learn': 'Instant',
        'Best_For': 'Community identification',
        'Pro_Tips': 'Context matters - use with fellow crocheters'
    },
    {
        'ID': 'ocd',
        'Status': 'New',
        'Name_US': 'Obsessive Crocheting Disorder',
        'Name_UK': 'Obsessive Crocheting Disorder',
        'Symbol': 'OCD',
        'Category': 'slang',
        'Tags': 'community, humor, addiction',
        'Description': 'Humorous term for compulsive need to crochet',
        'Difficulty': '1',
        'Time_To_Learn': 'Instant',
        'Best_For': 'Explaining yarn purchases'
    },
    {
        'ID': 'cip',
        'Status': 'New',
        'Name_US': 'Crochet In Public',
        'Name_UK': 'Crochet In Public',
        'Symbol': 'CIP',
        'Category': 'slang',
        'Tags': 'community, social, portable',
        'Description': 'Taking your crochet project out in public spaces',
        'Difficulty': '1',
        'Time_To_Learn': 'Instant',
        'Best_For': 'Waiting rooms, commutes, cafes'
    },
    {
        'ID': 'talc',
        'Status': 'New',
        'Name_US': 'Take Along Crochet',
        'Name_UK': 'Take Along Crochet',
        'Symbol': 'TALC',
        'Category': 'slang',
        'Tags': 'community, portable, travel',
        'Description': 'Portable project perfect for travel',
        'Difficulty': '1',
        'Time_To_Learn': 'Instant',
        'Best_For': 'Travel, waiting, social events'
    },
    {
        'ID': 'pigs',
        'Status': 'New',
        'Name_US': 'Projects In Grocery Sacks',
        'Name_UK': 'Projects In Grocery Sacks',
        'Symbol': 'PIGS',
        'Category': 'slang',
        'Tags': 'community, storage, humor',
        'Description': 'Crochet projects stored in grocery bags',
        'Difficulty': '1',
        'Time_To_Learn': 'Instant',
        'Best_For': 'Emergency project storage'
    },
    {
        'ID': 'phd',
        'Status': 'New',
        'Name_US': 'Projects Half Done',
        'Name_UK': 'Projects Half Done',
        'Symbol': 'PHD',
        'Category': 'slang',
        'Tags': 'community, wip, incomplete',
        'Description': 'Multiple crochet projects at 50% completion',
        'Difficulty': '1',
        'Time_To_Learn': 'Instant',
        'Best_For': 'Describing your project pile'
    },
    {
        'ID': 'toad',
        'Status': 'New',
        'Name_US': 'Trashed Object Abandoned in Disgust',
        'Name_UK': 'Trashed Object Abandoned in Disgust',
        'Symbol': 'TOAD',
        'Category': 'slang',
        'Tags': 'community, abandoned, frustration',
        'Description': 'Project so frustrating you gave up completely',
        'Difficulty': '1',
        'Time_To_Learn': 'Instant',
        'Best_For': 'Venting frustration',
        'Common_Mistakes': 'Not frogging to reuse yarn'
    },
    {
        'ID': 'crojo',
        'Status': 'New',
        'Name_US': 'Crochet Mojo',
        'Name_UK': 'Crochet Mojo',
        'Symbol': 'Crojo',
        'Category': 'slang',
        'Tags': 'community, motivation, inspiration',
        'Description': 'Your crochet motivation and creative energy',
        'Difficulty': '1',
        'Time_To_Learn': 'Instant',
        'Best_For': 'Describing creative flow'
    },
    
    # === ADVANCED TECHNIQUES ===
    {
        'ID': 'bavarian',
        'Status': 'New',
        'Name_US': 'Bavarian Crochet',
        'Name_UK': 'Bavarian Crochet',
        'Symbol': 'bav',
        'Category': 'technique',
        'Tags': 'advanced, colorwork, squares',
        'Description': 'Creates colorful layered squares with unique diagonal construction',
        'Difficulty': '4',
        'Time_To_Learn': '2-3 hours',
        'Best_For': 'Blankets, Pillows, Afghans',
        'Common_Mistakes': 'Color placement confusion',
        'Pro_Tips': 'Use high contrast colors for best effect'
    },
    {
        'ID': 'entrelac',
        'Status': 'New',
        'Name_US': 'Entrelac Crochet',
        'Name_UK': 'Entrelac Crochet',
        'Symbol': 'entrelac',
        'Category': 'technique',
        'Tags': 'advanced, tunisian, basketweave',
        'Description': 'Creates interlocking diamond pattern using Tunisian crochet base',
        'Difficulty': '4',
        'Time_To_Learn': '2-3 hours',
        'Best_For': 'Blankets, Scarves, Vests',
        'Common_Mistakes': 'Losing track of block sequence',
        'Pro_Tips': 'Master Tunisian simple stitch first'
    },
    {
        'ID': 'intarsia',
        'Status': 'New',
        'Name_US': 'Intarsia Crochet',
        'Name_UK': 'Intarsia Crochet',
        'Symbol': 'intarsia',
        'Category': 'technique',
        'Tags': 'intermediate, colorwork, blocks',
        'Description': 'Large color blocks without carrying yarn across back',
        'Difficulty': '3',
        'Time_To_Learn': '1-2 hours',
        'Best_For': 'Picture blankets, Large motifs',
        'Common_Mistakes': 'Loose joins between colors',
        'Pro_Tips': 'Use bobbins for each color section'
    },
    {
        'ID': 'filet',
        'Status': 'New',
        'Name_US': 'Filet Crochet',
        'Name_UK': 'Filet Crochet',
        'Symbol': 'filet',
        'Category': 'technique',
        'Tags': 'intermediate, lace, mesh',
        'Description': 'Creates pictures using filled and open mesh squares',
        'Difficulty': '3',
        'Time_To_Learn': '1-2 hours',
        'Best_For': 'Curtains, Doilies, Table runners',
        'Common_Mistakes': 'Miscounting mesh spaces',
        'Pro_Tips': 'Use graph paper to plan designs'
    },
    {
        'ID': 'overlay',
        'Status': 'New',
        'Name_US': 'Overlay Crochet',
        'Name_UK': 'Overlay Crochet',
        'Symbol': 'overlay',
        'Category': 'technique',
        'Tags': 'advanced, layered, 3D',
        'Description': 'Working stitches on top of existing fabric for 3D effect',
        'Difficulty': '4',
        'Time_To_Learn': '2+ hours',
        'Best_For': 'Mandalas, Wall art, Decorative squares',
        'Common_Mistakes': 'Puckering from tight stitches',
        'Pro_Tips': 'Keep overlay stitches looser'
    },
    {
        'ID': 'hyperbolic',
        'Status': 'New',
        'Name_US': 'Hyperbolic Crochet',
        'Name_UK': 'Hyperbolic Crochet',
        'Symbol': 'hyperbolic',
        'Category': 'technique',
        'Tags': 'mathematical, ruffles, coral',
        'Description': 'Mathematical increasing creates natural ruffled forms',
        'Difficulty': '2',
        'Time_To_Learn': '30-60 minutes',
        'Best_For': 'Coral reef projects, Ruffled scarves',
        'Common_Mistakes': 'Inconsistent increase rate',
        'Pro_Tips': 'Increase in every stitch for maximum ruffle'
    },
    {
        'ID': 'wire-crochet',
        'Status': 'New',
        'Name_US': 'Wire Crochet',
        'Name_UK': 'Wire Crochet',
        'Symbol': 'wire',
        'Category': 'technique',
        'Tags': 'specialty, jewelry, sculpture',
        'Description': 'Using wire instead of yarn for sculptural pieces',
        'Difficulty': '3',
        'Time_To_Learn': '1-2 hours',
        'Best_For': 'Jewelry, Sculptures, Art pieces',
        'Common_Mistakes': 'Wire kinking or breaking',
        'Pro_Tips': 'Use jewelry pliers and wear gloves'
    },
    {
        'ID': 'bead-crochet',
        'Status': 'New',
        'Name_US': 'Bead Crochet',
        'Name_UK': 'Bead Crochet',
        'Symbol': 'bead',
        'Category': 'technique',
        'Tags': 'decorative, jewelry, embellishment',
        'Description': 'Incorporating beads into crochet stitches',
        'Difficulty': '3',
        'Time_To_Learn': '1 hour',
        'Best_For': 'Jewelry, Purses, Embellishments',
        'Common_Mistakes': 'Beads on wrong side',
        'Pro_Tips': 'Pre-string all beads before starting'
    },
    
    # === MISSING STITCH VARIATIONS ===
    {
        'ID': 'linked-dc',
        'Status': 'New',
        'Name_US': 'Linked Double Crochet',
        'Name_UK': 'Linked Treble Crochet',
        'Symbol': 'ldc',
        'Category': 'stitch',
        'Tags': 'intermediate, texture, dense',
        'Description': 'Double crochets linked through horizontal bars for denser fabric',
        'Difficulty': '3',
        'Time_To_Learn': '30-60 minutes',
        'Best_For': 'Garments, Bags, Structured items',
        'Common_Mistakes': 'Missing the horizontal bar',
        'Pro_Tips': 'Insert hook from top to bottom'
    },
    {
        'ID': 'fdc',
        'Status': 'New',
        'Name_US': 'Foundation Double Crochet',
        'Name_UK': 'Foundation Treble Crochet',
        'Symbol': 'fdc',
        'Category': 'foundation',
        'Tags': 'intermediate, foundation, stretchy',
        'Description': 'Creates foundation chain and first row of DC simultaneously',
        'Difficulty': '3',
        'Time_To_Learn': '45-60 minutes',
        'Best_For': 'Garment edges, Blanket starts',
        'Common_Mistakes': 'Too tight foundation',
        'Pro_Tips': 'Keep stitches loose and even'
    },
    {
        'ID': 'spike-st',
        'Status': 'New',
        'Name_US': 'Spike Stitch',
        'Name_UK': 'Spike Stitch',
        'Symbol': 'spike',
        'Category': 'stitch',
        'Tags': 'intermediate, decorative, colorwork',
        'Description': 'Working into rows below current row for vertical lines',
        'Difficulty': '2',
        'Time_To_Learn': '20-30 minutes',
        'Best_For': 'Textured patterns, Colorwork',
        'Common_Mistakes': 'Pulling too tight',
        'Pro_Tips': 'Keep spike stitches loose'
    },
    {
        'ID': 'loop-st',
        'Status': 'New',
        'Name_US': 'Loop Stitch',
        'Name_UK': 'Loop Stitch',
        'Symbol': 'loop',
        'Category': 'stitch',
        'Tags': 'intermediate, texture, fur',
        'Description': 'Creates loops on surface for fur or fringe effect',
        'Difficulty': '3',
        'Time_To_Learn': '30-45 minutes',
        'Best_For': 'Fur texture, Rugs, Hair on amigurumi',
        'Common_Mistakes': 'Inconsistent loop size',
        'Pro_Tips': 'Use finger or ruler for even loops'
    },
    {
        'ID': 'crab-st',
        'Status': 'New',
        'Name_US': 'Crab Stitch',
        'Name_UK': 'Crab Stitch',
        'Symbol': 'crab',
        'Category': 'stitch',
        'Tags': 'basic, edging, decorative',
        'Description': 'Reverse single crochet worked backwards for rope-like edge',
        'Difficulty': '2',
        'Time_To_Learn': '15-20 minutes',
        'Best_For': 'Borders, Edgings, Finishing',
        'Common_Mistakes': 'Working in wrong direction',
        'Pro_Tips': 'Work from left to right (opposite usual)'
    },
    {
        'ID': 'surface-crochet',
        'Status': 'New',
        'Name_US': 'Surface Crochet',
        'Name_UK': 'Surface Crochet',
        'Symbol': 'surface',
        'Category': 'technique',
        'Tags': 'decorative, embellishment, design',
        'Description': 'Working slip stitch on top of finished fabric',
        'Difficulty': '2',
        'Time_To_Learn': '20-30 minutes',
        'Best_For': 'Adding designs, Letters, Embellishment',
        'Common_Mistakes': 'Pulling too tight causing puckering',
        'Pro_Tips': 'Keep tension very loose'
    },
    {
        'ID': 'chainless-foundation',
        'Status': 'New',
        'Name_US': 'Chainless Foundation',
        'Name_UK': 'Chainless Foundation',
        'Symbol': 'chainless',
        'Category': 'foundation',
        'Tags': 'advanced, foundation, alternative',
        'Description': 'Starting projects without traditional chain foundation',
        'Difficulty': '4',
        'Time_To_Learn': '1-2 hours',
        'Best_For': 'Circular projects, Advanced patterns',
        'Common_Mistakes': 'Confusion with stitch placement',
        'Pro_Tips': 'Practice with scrap yarn first'
    }
]

def add_crochet_terms(sheets):
    """Add pure crochet terms to the sheet"""
    # Get current headers
    result = sheets.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!1:1'
    ).execute()
    
    headers = result.get('values', [[]])[0]
    
    # Prepare rows to add
    rows_to_add = []
    for term in crochet_only_terms:
        row = []
        for header in headers:
            # Map headers to our term dictionary
            if header == 'ID':
                row.append(term.get('ID', ''))
            elif header == 'Status':
                row.append(term.get('Status', 'New'))
            elif header == 'Name_US':
                row.append(term.get('Name_US', ''))
            elif header == 'Name_UK':
                row.append(term.get('Name_UK', ''))
            elif header == 'Symbol':
                row.append(term.get('Symbol', ''))
            elif header == 'Category':
                row.append(term.get('Category', ''))
            elif header == 'Tags':
                row.append(term.get('Tags', ''))
            elif header == 'Description':
                row.append(term.get('Description', ''))
            elif header == 'Difficulty':
                row.append(term.get('Difficulty', ''))
            elif header == 'Time_To_Learn':
                row.append(term.get('Time_To_Learn', ''))
            elif header == 'Best_For':
                row.append(term.get('Best_For', ''))
            elif header == 'Common_Mistakes':
                row.append(term.get('Common_Mistakes', ''))
            elif header == 'Pro_Tips':
                row.append(term.get('Pro_Tips', ''))
            elif header == 'Hook_Sizes':
                row.append(term.get('Hook_Sizes', ''))
            elif header == 'Left_Handed_Note':
                row.append(term.get('Left_Handed_Note', ''))
            else:
                row.append('')
        
        rows_to_add.append(row)
    
    # Append to sheet
    body = {
        'values': rows_to_add
    }
    
    sheets.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:Z',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    print(f"✅ Added {len(rows_to_add)} pure crochet terms!")
    print("\nTerms added:")
    for term in crochet_only_terms:
        print(f"  • {term['Name_US']} ({term['ID']})")

def main():
    print("Adding PURE CROCHET Terms to DANI'S Glossary")
    print("=" * 45)
    print("NO KNITTING TERMS! 🧶")
    print()
    
    sheets = get_sheets_service()
    add_crochet_terms(sheets)
    
    print("\n📊 Summary:")
    print(f"  Community Slang: 10 terms")
    print(f"  Advanced Techniques: 8 terms")
    print(f"  Missing Stitches: 7 terms")
    print(f"  TOTAL: 25 pure crochet terms")
    
    print("\nNext steps:")
    print("1. Run export_to_glossarydata.py")
    print("2. Test in your glossary")
    print("3. Push to GitHub")
    print("4. Celebrate having 275+ terms! 🎉")

if __name__ == "__main__":
    main()