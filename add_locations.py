import json
import spacy
from typing import List, Set

# Load spaCy model for named entity recognition
nlp = spacy.load("en_core_web_sm")

# Common location abbreviations and variations
LOCATION_MAPPINGS = {
    'NYC': 'New York City',
    'NY': 'New York',
    'U.S.': 'United States',
    'USA': 'United States',
    'UK': 'United Kingdom',
    'U.K.': 'United Kingdom',
    'DC': 'Washington DC',
    'D.C.': 'Washington DC',
    'SF': 'San Francisco',
    'LA': 'Los Angeles',
    'CA': 'California',
    'TX': 'Texas',
    'FL': 'Florida',
    'IL': 'Illinois',
    'MI': 'Michigan',
    'PA': 'Pennsylvania',
    'WA': 'Washington',
    'OR': 'Oregon',
    'GA': 'Georgia',
    'MA': 'Massachusetts',
    'NJ': 'New Jersey',
    'CT': 'Connecticut',
    'MD': 'Maryland',
    'VA': 'Virginia',
    'NC': 'North Carolina',
    'SC': 'South Carolina',
    'TN': 'Tennessee',
    'KY': 'Kentucky',
    'OH': 'Ohio',
    'IN': 'Indiana',
    'WI': 'Wisconsin',
    'MN': 'Minnesota',
    'IA': 'Iowa',
    'MO': 'Missouri',
    'AR': 'Arkansas',
    'LA': 'Louisiana',
    'MS': 'Mississippi',
    'AL': 'Alabama',
    'AK': 'Alaska',
    'HI': 'Hawaii',
    'AZ': 'Arizona',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'UT': 'Utah',
    'CO': 'Colorado',
    'WY': 'Wyoming',
    'MT': 'Montana',
    'ID': 'Idaho',
    'ND': 'North Dakota',
    'SD': 'South Dakota',
    'NE': 'Nebraska',
    'KS': 'Kansas',
    'OK': 'Oklahoma',
    'ME': 'Maine',
    'NH': 'New Hampshire',
    'VT': 'Vermont',
    'RI': 'Rhode Island',
    'DE': 'Delaware',
}

def normalize_location(loc: str) -> str:
    """
    Normalize location names using common abbreviations and variations.
    """
    # Convert to title case for consistency
    loc = loc.title()
    
    # Check if the location is in our mappings
    if loc in LOCATION_MAPPINGS:
        return LOCATION_MAPPINGS[loc]
    
    return loc

def extract_locations(text: str) -> Set[str]:
    """
    Extract location names from text using spaCy's named entity recognition
    and common location patterns.
    """
    doc = nlp(text)
    locations = set()
    
    # Extract locations from named entities
    for ent in doc.ents:
        if ent.label_ in ['GPE', 'LOC']:  # GPE = Geo-Political Entity, LOC = Location
            locations.add(normalize_location(ent.text))
    
    # Look for common location patterns
    words = text.split()
    for i, word in enumerate(words):
        # Check for state abbreviations
        if word.upper() in LOCATION_MAPPINGS:
            locations.add(LOCATION_MAPPINGS[word.upper()])
        
        # Check for "in [Location]" pattern
        if word.lower() == 'in' and i + 1 < len(words):
            next_word = words[i + 1]
            if next_word.upper() in LOCATION_MAPPINGS:
                locations.add(LOCATION_MAPPINGS[next_word.upper()])
    
    return locations

def process_jsonl_file(input_file: str, output_file: str):
    """
    Process the JSONL file to add location information from both headlines and article text.
    """
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            try:
                data = json.loads(line.strip())
                
                # Extract locations from both headline and article text
                headline = data.get('headline', '')
                article_text = data.get('article_text', '')
                
                # Combine locations from both sources
                locations = list(extract_locations(headline) | extract_locations(article_text))
                
                # Add locations to the data
                data['location'] = locations
                
                # Write the updated data
                f_out.write(json.dumps(data) + '\n')
                
            except json.JSONDecodeError:
                print(f"Error decoding JSON line: {line}")
                continue

if __name__ == "__main__":
    input_file = "covid_media_serp_results.jsonl"
    output_file = "covid_media_serp_results_with_locations.jsonl"
    process_jsonl_file(input_file, output_file) 