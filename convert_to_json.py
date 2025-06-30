import json

def convert_jsonl_to_json(input_file, output_file):
    # List to store all articles
    articles = []
    
    # Read the JSONL file
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                # Parse each line as JSON
                article = json.loads(line.strip())
                
                # Ensure all required fields are present
                required_fields = {
                    "publish_date": "",
                    "source": "",
                    "headline": "",
                    "url": "",
                    "article_text": "",
                    "location": [],
                    "gpt_analysis": {
                        "tone": "",
                        "framing": "",
                        "group_mentions": [],
                        "metaphors": [],
                        "euphemisms": [],
                        "absences": [],
                        "grief_handling": "",
                        "blame_or_agency": "",
                        "commodification_of_death": ""
                    }
                }
                
                # Update with actual values, keeping defaults for missing fields
                for key, value in article.items():
                    if key in required_fields:
                        required_fields[key] = value
                
                articles.append(required_fields)
                
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                continue
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    input_file = "covid_media_serp_results_with_locations.jsonl"
    output_file = "covid_media_serp_results.json"
    convert_jsonl_to_json(input_file, output_file)
    print(f"Conversion complete. Output written to {output_file}") 