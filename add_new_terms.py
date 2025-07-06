#!/usr/bin/env python3
"""
Add FINAL batch of crochet terms to Google Sheets - Batch 3
For DANI'S Crochet Glossary - Push to 250+ terms!
Focusing on unique, often-missed terms
"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Your spreadsheet ID
SPREADSHEET_ID = '1WXt17J7Bn7nuRG3SV1HvvoWX4mvgZmY7dAeLRIlIh3A'

# Service account credentials
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheets_service():
    """Initialize Google Sheets service"""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service

def add_terms_batch(service, terms_data):
    """Add multiple terms to the sheet"""
    sheet = service.spreadsheets()
    
    # First, get the current last row
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!A:A'
    ).execute()
    
    current_rows = len(result.get('values', []))
    next_row = current_rows + 1
    
    # Prepare the data for batch update
    values = []
    for term in terms_data:
        row = [
            term['id'],
            'New',  # Status
            term['name_us'],
            term['name_uk'],
            term['symbol'],
            term['category'],
            term['tags'],
            term['description'],
            term.get('priority', 'Medium')
        ]
        values.append(row)
    
    # Update the sheet
    body = {
        'values': values
    }
    
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f'Sheet1!A{next_row}',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    print(f"Added {result.get('updatedRows', 0)} new terms!")
    return result

# Define batch 3 - Unique and often-missed terms
batch_3_terms = [
    # REGIONAL & CULTURAL VARIATIONS (8 terms)
    {
        'id': 'AMISH-KNOT',
        'name_us': 'Amish Knot',
        'name_uk': 'Amish Knot',
        'symbol': 'amish',
        'category': 'regional',
        'tags': 'regional, traditional, joining',
        'description': 'Traditional invisible joining method',
        'priority': 'Low'
    },
    {
        'id': 'RUSSIAN-JOIN',
        'name_us': 'Russian Join',
        'name_uk': 'Russian Join',
        'symbol': 'rjoin',
        'category': 'regional',
        'tags': 'regional, joining, invisible',
        'description': 'Splicing yarn ends by weaving',
        'priority': 'Medium'
    },
    {
        'id': 'CELTIC-WEAVE',
        'name_us': 'Celtic Weave',
        'name_uk': 'Celtic Weave',
        'symbol': 'celtic',
        'category': 'regional',
        'tags': 'regional, cables, traditional',
        'description': 'Complex cable patterns from Celtic tradition',
        'priority': 'Low'
    },
    {
        'id': 'JAPANESE-FLOWER',
        'name_us': 'Japanese Flower',
        'name_uk': 'Japanese Flower',
        'symbol': 'jflower',
        'category': 'regional',
        'tags': 'regional, motif, decorative',
        'description': 'Delicate flower motifs from Japanese patterns',
        'priority': 'Low'
    },
    {
        'id': 'NORDIC-STAR',
        'name_us': 'Nordic Star',
        'name_uk': 'Nordic Star',
        'symbol': 'nstar',
        'category': 'regional',
        'tags': 'regional, colorwork, traditional',
        'description': 'Star patterns from Scandinavian tradition',
        'priority': 'Low'
    },
    {
        'id': 'PERUVIAN-BRAID',
        'name_us': 'Peruvian Braid',
        'name_uk': 'Peruvian Braid',
        'symbol': 'pbraid',
        'category': 'regional',
        'tags': 'regional, edging, decorative',
        'description': 'Decorative braided edge from Peru',
        'priority': 'Low'
    },
    {
        'id': 'AFRICAN-FLOWER',
        'name_us': 'African Flower',
        'name_uk': 'African Flower',
        'symbol': 'aflower',
        'category': 'regional',
        'tags': 'regional, hexagon, motif',
        'description': 'Hexagonal motif popular in African crafts',
        'priority': 'Medium'
    },
    {
        'id': 'TURKISH-CAST-ON',
        'name_us': 'Turkish Cast On',
        'name_uk': 'Turkish Cast On',
        'symbol': 'tcast',
        'category': 'regional',
        'tags': 'regional, provisional, technique',
        'description': 'Provisional cast on from Turkish tradition',
        'priority': 'Low'
    },
    
    # MATHEMATICAL & GEOMETRIC TERMS (7 terms)
    {
        'id': 'FIBONACCI',
        'name_us': 'Fibonacci Sequence',
        'name_uk': 'Fibonacci Sequence',
        'symbol': 'fib',
        'category': 'mathematical',
        'tags': 'mathematical, sequence, striping',
        'description': 'Using Fibonacci numbers for stripe sequences',
        'priority': 'Low'
    },
    {
        'id': 'FRACTAL',
        'name_us': 'Fractal Crochet',
        'name_uk': 'Fractal Crochet',
        'symbol': 'fract',
        'category': 'mathematical',
        'tags': 'mathematical, geometric, art',
        'description': 'Mathematical patterns creating fractals',
        'priority': 'Low'
    },
    {
        'id': 'HYPERBOLIC',
        'name_us': 'Hyperbolic Crochet',
        'name_uk': 'Hyperbolic Crochet',
        'symbol': 'hyper',
        'category': 'mathematical',
        'tags': 'mathematical, coral-reef, sculptural',
        'description': 'Exponential increases creating ruffled forms',
        'priority': 'Low'
    },
    {
        'id': 'TESSELLATION',
        'name_us': 'Tessellation',
        'name_uk': 'Tessellation',
        'symbol': 'tess',
        'category': 'mathematical',
        'tags': 'mathematical, repeating, pattern',
        'description': 'Repeating shapes with no gaps',
        'priority': 'Medium'
    },
    {
        'id': 'GOLDEN-RATIO',
        'name_us': 'Golden Ratio',
        'name_uk': 'Golden Ratio',
        'symbol': 'golden',
        'category': 'mathematical',
        'tags': 'mathematical, proportion, design',
        'description': 'Using 1.618 ratio in design proportions',
        'priority': 'Low'
    },
    {
        'id': 'MODULAR',
        'name_us': 'Modular Construction',
        'name_uk': 'Modular Construction',
        'symbol': 'mod',
        'category': 'mathematical',
        'tags': 'mathematical, construction, units',
        'description': 'Building with repeated geometric units',
        'priority': 'Medium'
    },
    {
        'id': 'MITERED',
        'name_us': 'Mitered Square',
        'name_uk': 'Mitred Square',
        'symbol': 'miter',
        'category': 'mathematical',
        'tags': 'mathematical, square, diagonal',
        'description': 'Square worked from corner to corner',
        'priority': 'Medium'
    },
    
    # EMBELLISHMENT & SURFACE TECHNIQUES (8 terms)
    {
        'id': 'SURFACE-SLIP',
        'name_us': 'Surface Slip Stitch',
        'name_uk': 'Surface Slip Stitch',
        'symbol': 'sslip',
        'category': 'embellishment',
        'tags': 'embellishment, surface, decorative',
        'description': 'Slip stitch worked on fabric surface',
        'priority': 'High'
    },
    {
        'id': 'SURFACE-CHAIN',
        'name_us': 'Surface Chain',
        'name_uk': 'Surface Chain',
        'symbol': 'schain',
        'category': 'embellishment',
        'tags': 'embellishment, surface, decorative',
        'description': 'Chain stitch embroidery on crochet',
        'priority': 'Medium'
    },
    {
        'id': 'APPLIQUE',
        'name_us': 'Applique',
        'name_uk': 'Applique',
        'symbol': 'app',
        'category': 'embellishment',
        'tags': 'embellishment, motif, sewing',
        'description': 'Attaching separate motifs to base',
        'priority': 'High'
    },
    {
        'id': 'FRINGE',
        'name_us': 'Fringe',
        'name_uk': 'Fringe',
        'symbol': 'fringe',
        'category': 'embellishment',
        'tags': 'embellishment, edge, decorative',
        'description': 'Cut yarn strands attached to edge',
        'priority': 'High'
    },
    {
        'id': 'TASSEL',
        'name_us': 'Tassel',
        'name_uk': 'Tassel',
        'symbol': 'tassel',
        'category': 'embellishment',
        'tags': 'embellishment, decorative, accent',
        'description': 'Bundled yarn decoration',
        'priority': 'High'
    },
    {
        'id': 'POM-POM',
        'name_us': 'Pom Pom',
        'name_uk': 'Pom Pom',
        'symbol': 'pom',
        'category': 'embellishment',
        'tags': 'embellishment, decorative, accent',
        'description': 'Fluffy ball decoration',
        'priority': 'Medium'
    },
    {
        'id': 'BEAD-CROCHET',
        'name_us': 'Bead Crochet',
        'name_uk': 'Bead Crochet',
        'symbol': 'bead',
        'category': 'embellishment',
        'tags': 'embellishment, beads, jewelry',
        'description': 'Incorporating beads into crochet',
        'priority': 'Medium'
    },
    {
        'id': 'SEQUIN',
        'name_us': 'Sequin Application',
        'name_uk': 'Sequin Application',
        'symbol': 'seq',
        'category': 'embellishment',
        'tags': 'embellishment, sparkle, decorative',
        'description': 'Adding sequins to crochet work',
        'priority': 'Low'
    },
    
    # FINISHING TECHNIQUES (7 terms)
    {
        'id': 'WET-BLOCK',
        'name_us': 'Wet Blocking',
        'name_uk': 'Wet Blocking',
        'symbol': 'wetb',
        'category': 'finishing',
        'tags': 'finishing, blocking, shaping',
        'description': 'Soaking and pinning to shape',
        'priority': 'High'
    },
    {
        'id': 'STEAM-BLOCK',
        'name_us': 'Steam Blocking',
        'name_uk': 'Steam Blocking',
        'symbol': 'steam',
        'category': 'finishing',
        'tags': 'finishing, blocking, shaping',
        'description': 'Using steam to set shape',
        'priority': 'High'
    },
    {
        'id': 'SPRAY-BLOCK',
        'name_us': 'Spray Blocking',
        'name_uk': 'Spray Blocking',
        'symbol': 'spray',
        'category': 'finishing',
        'tags': 'finishing, blocking, gentle',
        'description': 'Light misting for delicate fibers',
        'priority': 'Medium'
    },
    {
        'id': 'WEAVE-ENDS',
        'name_us': 'Weave in Ends',
        'name_uk': 'Weave in Ends',
        'symbol': 'weave',
        'category': 'finishing',
        'tags': 'finishing, ends, neatening',
        'description': 'Securing loose yarn ends',
        'priority': 'High'
    },
    {
        'id': 'FELTING',
        'name_us': 'Felting',
        'name_uk': 'Felting',
        'symbol': 'felt',
        'category': 'finishing',
        'tags': 'finishing, shrinking, wool',
        'description': 'Intentionally shrinking wool fabric',
        'priority': 'Medium'
    },
    {
        'id': 'FULLING',
        'name_us': 'Fulling',
        'name_uk': 'Fulling',
        'symbol': 'full',
        'category': 'finishing',
        'tags': 'finishing, controlled-felting, wool',
        'description': 'Controlled felting process',
        'priority': 'Low'
    },
    {
        'id': 'STARCH',
        'name_us': 'Starching',
        'name_uk': 'Starching',
        'symbol': 'starch',
        'category': 'finishing',
        'tags': 'finishing, stiffening, doilies',
        'description': 'Stiffening with starch solution',
        'priority': 'Medium'
    },
    
    # MODERN HYBRID TECHNIQUES (5 terms)
    {
        'id': 'KNOOKING',
        'name_us': 'Knooking',
        'name_uk': 'Knooking',
        'symbol': 'knook',
        'category': 'hybrid',
        'tags': 'hybrid, knit-look, modern',
        'description': 'Knitting with a crochet hook',
        'priority': 'Low'
    },
    {
        'id': 'CROCHET-KNIT',
        'name_us': 'Crochet-Knit Combo',
        'name_uk': 'Crochet-Knit Combo',
        'symbol': 'combo',
        'category': 'hybrid',
        'tags': 'hybrid, mixed-media, modern',
        'description': 'Combining crochet and knitting',
        'priority': 'Low'
    },
    {
        'id': 'BROOMSTICK',
        'name_us': 'Broomstick Lace',
        'name_uk': 'Broomstick Lace',
        'symbol': 'broom',
        'category': 'hybrid',
        'tags': 'hybrid, lace, vintage',
        'description': 'Using large needle with crochet hook',
        'priority': 'Medium'
    },
    {
        'id': 'HAIRPIN',
        'name_us': 'Hairpin Lace',
        'name_uk': 'Hairpin Lace',
        'symbol': 'hair',
        'category': 'hybrid',
        'tags': 'hybrid, lace, strips',
        'description': 'Lace strips made on hairpin loom',
        'priority': 'Medium'
    },
    {
        'id': 'LOOP-YARN',
        'name_us': 'Loop Yarn Crochet',
        'name_uk': 'Loop Yarn Crochet',
        'symbol': 'loopy',
        'category': 'hybrid',
        'tags': 'hybrid, specialty-yarn, modern',
        'description': 'Working with pre-looped yarn',
        'priority': 'Low'
    },
    
    # TROUBLESHOOTING TERMS (5 terms)
    {
        'id': 'TENSION-RING',
        'name_us': 'Tension Ring',
        'name_uk': 'Yarn Guide',
        'symbol': 'tring',
        'category': 'troubleshooting',
        'tags': 'troubleshooting, tool, tension',
        'description': 'Ring to maintain consistent tension',
        'priority': 'Low'
    },
    {
        'id': 'SPLIT-YARN',
        'name_us': 'Split Yarn',
        'name_uk': 'Split Yarn',
        'symbol': 'split',
        'category': 'troubleshooting',
        'tags': 'troubleshooting, problem, yarn',
        'description': 'When hook splits yarn strands',
        'priority': 'Medium'
    },
    {
        'id': 'TWISTED-CHAIN',
        'name_us': 'Twisted Chain',
        'name_uk': 'Twisted Chain',
        'symbol': 'twist',
        'category': 'troubleshooting',
        'tags': 'troubleshooting, problem, foundation',
        'description': 'Foundation chain that spirals',
        'priority': 'High'
    },
    {
        'id': 'CURLING-EDGE',
        'name_us': 'Curling Edge',
        'name_uk': 'Curling Edge',
        'symbol': 'curl',
        'category': 'troubleshooting',
        'tags': 'troubleshooting, problem, edge',
        'description': 'Edges that roll or curl',
        'priority': 'High'
    },
    {
        'id': 'YARN-CHICKEN',
        'name_us': 'Playing Yarn Chicken',
        'name_uk': 'Playing Yarn Chicken',
        'symbol': 'chicken',
        'category': 'troubleshooting',
        'tags': 'troubleshooting, yarn-shortage, gamble',
        'description': 'Hoping to finish before yarn runs out',
        'priority': 'Medium'
    }
]

def main():
    """Main function to run the import"""
    print("Adding FINAL batch of crochet terms to Google Sheets...")
    print(f"Total terms to add: {len(batch_3_terms)}")
    print("\nThis batch includes unique categories:")
    print("- Regional & Cultural Variations")
    print("- Mathematical & Geometric Terms")
    print("- Embellishment Techniques")
    print("- Finishing Methods")
    print("- Modern Hybrid Techniques")
    print("- Troubleshooting Terms")
    
    try:
        # Initialize service
        service = get_sheets_service()
        
        # Add all terms
        result = add_terms_batch(service, batch_3_terms)
        
        print("\n🎉 SUCCESS! Final batch added!")
        print(f"Sheet ID: {SPREADSHEET_ID}")
        print("\n📊 FINAL TALLY:")
        print("- Previous total: 213 terms")
        print(f"- Added in this batch: {len(batch_3_terms)} terms")
        print(f"- GRAND TOTAL: ~{213 + len(batch_3_terms)} TERMS!")
        print("\n🏆 DANI'S now has one of the most comprehensive crochet glossaries online!")
        print("\nYour glossary includes:")
        print("✓ Basic stitches")
        print("✓ Advanced techniques")
        print("✓ Regional variations")
        print("✓ Modern trends")
        print("✓ Mathematical concepts")
        print("✓ Troubleshooting help")
        print("✓ Community slang")
        print("✓ Professional construction")
        print("\n🎂 Perfect for your birthday launch!")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")

if __name__ == "__main__":
    main()