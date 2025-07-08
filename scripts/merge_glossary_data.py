#!/usr/bin/env python3
import json

# Load the extracted translations
with open('data/glossary/crochet-terms-v1.json', 'r') as f:
    translations_data = json.load(f)

# The existing glossary data with English names
existing_terms = {
    "ch": {"name_us": "Chain Stitch", "name_uk": "Chain Stitch", "symbol": "o"},
    "sl st": {"name_us": "Slip Stitch", "name_uk": "Slip Stitch", "symbol": "-"},
    "sc": {"name_us": "Single Crochet", "name_uk": "Double Crochet", "symbol": "x"},
    "hdc": {"name_us": "Half Double Crochet", "name_uk": "Half Treble Crochet", "symbol": "H"},
    "dc": {"name_us": "Double Crochet", "name_uk": "Treble Crochet", "symbol": "T"},
    "tr": {"name_us": "Treble Crochet", "name_uk": "Double Treble Crochet", "symbol": "TT"},
    "dtr": {"name_us": "Double Treble Crochet", "name_uk": "Triple Treble Crochet", "symbol": "TTT"},
    "trtr": {"name_us": "Triple Treble Crochet", "name_uk": "Quadruple Treble Crochet", "symbol": "TTTT"},
    "inc": {"name_us": "Increase", "name_uk": "Increase", "symbol": "+"},
    "dec": {"name_us": "Decrease", "name_uk": "Decrease", "symbol": "-"},
    "fpdc": {"name_us": "Front Post Double Crochet", "name_uk": "Front Post Treble Crochet", "symbol": "FP"},
    "bpdc": {"name_us": "Back Post Double Crochet", "name_uk": "Back Post Treble Crochet", "symbol": "BP"},
    "sc2tog": {"name_us": "Single Crochet 2 Together", "name_uk": "Double Crochet 2 Together", "symbol": "X2"},
    "dc2tog": {"name_us": "Double Crochet 2 Together", "name_uk": "Treble Crochet 2 Together", "symbol": "T2"},
    "popcorn": {"name_us": "Popcorn Stitch", "name_uk": "Popcorn Stitch", "symbol": "PC"},
    "bobble": {"name_us": "Bobble Stitch", "name_uk": "Bobble Stitch", "symbol": "BO"},
    "puff": {"name_us": "Puff Stitch", "name_uk": "Puff Stitch", "symbol": "PF"},
    "shell": {"name_us": "Shell Stitch", "name_uk": "Shell Stitch", "symbol": "SH"},
    "v-stitch": {"name_us": "V-Stitch", "name_uk": "V-Stitch", "symbol": "V"},
    "cluster": {"name_us": "Cluster Stitch", "name_uk": "Cluster Stitch", "symbol": "CL"},
    "x-stitch": {"name_us": "Cross Stitch", "name_uk": "Cross Stitch", "symbol": "X"},
    "crossed dc": {"name_us": "Crossed Double Crochet", "name_uk": "Crossed Treble Crochet", "symbol": "XDC"},
    "mesh": {"name_us": "Mesh Stitch", "name_uk": "Mesh Stitch", "symbol": "MS"},
    "spike sc": {"name_us": "Spike Single Crochet", "name_uk": "Spike Double Crochet", "symbol": "SP"},
    "granny square": {"name_us": "Granny Square", "name_uk": "Granny Square", "symbol": "GS"}
}

# Create merged data
merged_glossary = {
    "metadata": {
        "version": "1.0.0",
        "last_updated": "2025-01-05",
        "total_terms": 0,
        "languages": ["en_us", "en_uk", "ru"]
    },
    "terms": []
}

# Process each translation entry
for term in translations_data['terms']:
    term_id = term['id'].lower()
    
    # Add English names if we have them
    if term_id in existing_terms:
        term['names']['en_us']['full'] = existing_terms[term_id]['name_us']
        term['names']['en_uk']['full'] = existing_terms[term_id]['name_uk']
        term['symbol']['chart'] = existing_terms[term_id].get('symbol', '')
    
    merged_glossary['terms'].append(term)

merged_glossary['metadata']['total_terms'] = len(merged_glossary['terms'])

# Save the merged file
with open('data/glossary/crochet-terms-merged.json', 'w') as f:
    json.dump(merged_glossary, f, indent=2, ensure_ascii=False)

print(f"Merged {len(merged_glossary['terms'])} terms")
print("Saved to: data/glossary/crochet-terms-merged.json")