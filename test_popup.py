import json

def create_popup_content(article):
    """Create rich popup content for each article"""
    headline = article.get('headline', 'No headline')
    source = article.get('source', 'Unknown source')
    tone = article.get('gpt_analysis', {}).get('tone', 'Unknown')
    framing = article.get('gpt_analysis', {}).get('framing', 'Unknown')
    group_mentions = article.get('gpt_analysis', {}).get('group_mentions', [])
    metaphors = article.get('gpt_analysis', {}).get('metaphors', [])
    
    # Format group mentions and metaphors
    groups_str = ', '.join(group_mentions[:3]) if group_mentions else 'None mentioned'
    metaphors_str = ', '.join(metaphors[:2]) if metaphors else 'None'
    
    popup_html = f"""
    <div style="width: 300px;">
        <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{headline}</h4>
        <p><strong>Source:</strong> {source}</p>
        <p><strong>Tone:</strong> <span style="color: #e74c3c;">{tone}</span></p>
        <p><strong>Framing:</strong> <span style="color: #3498db;">{framing}</span></p>
        <p><strong>Groups:</strong> {groups_str}</p>
        <p><strong>Metaphors:</strong> {metaphors_str}</p>
    </div>
    """
    return popup_html

# Read a few articles and test popup content
articles = []
with open('covid_media_serp_results_with_locations.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i >= 5:  # Just read first 5 articles
            break
        try:
            articles.append(json.loads(line.strip()))
        except json.JSONDecodeError:
            continue

print("Testing popup content for first 5 articles:")
print("=" * 50)

for i, article in enumerate(articles):
    print(f"\nArticle {i+1}:")
    print(f"Headline: {article.get('headline', 'No headline')}")
    print(f"Source: {article.get('source', 'Unknown')}")
    print(f"Tone: {article.get('gpt_analysis', {}).get('tone', 'Unknown')}")
    print(f"Framing: {article.get('gpt_analysis', {}).get('framing', 'Unknown')}")
    print(f"Groups: {article.get('gpt_analysis', {}).get('group_mentions', [])}")
    print(f"Metaphors: {article.get('gpt_analysis', {}).get('metaphors', [])}")
    
    popup = create_popup_content(article)
    print(f"\nPopup HTML (first 200 chars): {popup[:200]}...")
    print("-" * 30) 