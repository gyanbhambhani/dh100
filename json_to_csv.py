import json
import csv
from datetime import datetime

def convert_json_to_csv():
    # Read the JSON file
    with open('dh.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    # Define the CSV headers (without article_text)
    headers = [
        'publish_date',
        'source',
        'headline',
        'url',
        'location',
        'tone',
        'framing',
        'group_mentions',
        'metaphors',
        'euphemisms',
        'absences',
        'grief_handling',
        'blame_or_agency',
        'commodification_of_death'
    ]
    
    # Create and write to CSV file
    with open('dh.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        
        for article in data:
            # Create a row dictionary with the main fields (without article_text)
            row = {
                'publish_date': article.get('publish_date', ''),
                'source': article.get('source', ''),
                'headline': article.get('headline', ''),
                'url': article.get('url', ''),
                'location': '; '.join(article.get('location', [])),
            }
            
            # Add GPT analysis fields
            gpt_analysis = article.get('gpt_analysis', {})
            row.update({
                'tone': gpt_analysis.get('tone', ''),
                'framing': gpt_analysis.get('framing', ''),
                'group_mentions': '; '.join(gpt_analysis.get('group_mentions', [])),
                'metaphors': '; '.join(gpt_analysis.get('metaphors', [])),
                'euphemisms': '; '.join(gpt_analysis.get('euphemisms', [])),
                'absences': '; '.join(gpt_analysis.get('absences', [])),
                'grief_handling': gpt_analysis.get('grief_handling', ''),
                'blame_or_agency': gpt_analysis.get('blame_or_agency', ''),
                'commodification_of_death': gpt_analysis.get('commodification_of_death', '')
            })
            
            writer.writerow(row)

if __name__ == '__main__':
    convert_json_to_csv()
    print("Conversion completed. Output saved to dh.csv") 