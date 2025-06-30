import os
import json
import time
import requests
from dotenv import load_dotenv
from newspaper import Article
import trafilatura
from typing import List, Dict, Optional
import logging
import random
import re
import spacy

# --- PROJECT ESSENCE ---
"""
Essence of the Project:
This agent surfaces how the true human cost of the COVID-19 pandemic has been sanitized, fragmented, and rendered invisible through patterns of media framing — and whose deaths have been allowed to disappear from public memory.

It uses AI-driven deep media analysis to surface:
- What is said about COVID deaths
- What is not said — the invisible, the absent, the ungrieved
- How the framing of death reflects underlying systems of inequality, ableism, racism, and capitalist logic
- The evolving narrative gap between real deaths and media memory of death
"""

# --- CONFIGURATION ---
SEARCH_QUERY = 'covid deaths site:nytimes.com after:2020-03-01 before:2020-03-31'
OUTPUT_FILE = 'covid_media_serp_results.jsonl'
MAX_RESULTS = 1000  # Fetch up to 1000 articles
DEBUG = True  # Toggle debug mode
SLEEP_BETWEEN_REQUESTS = 0.2  # Lowered for speed, but not zero to avoid bans
SERPAPI_PAGE_SIZE = 100  # SerpAPI max per page

# --- SETUP LOGGING ---
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- LOAD API KEYS ---
load_dotenv()
SERPAPI_API_KEY = os.getenv('SERP_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not SERPAPI_API_KEY or not OPENAI_API_KEY:
    raise ValueError("API keys not found in .env file.")

# --- SERPAPI SEARCH WITH PAGINATION ---
def search_serpapi(query: str, max_results: int = 1000) -> List[Dict]:
    url = 'https://serpapi.com/search'
    articles = []
    start = 0
    while len(articles) < max_results:
        params = {
            'engine': 'google',
            'q': query,
            'api_key': SERPAPI_API_KEY,
            'num': SERPAPI_PAGE_SIZE,
            'start': start
        }
        logger.debug(f"Querying SerpAPI with params: {params}")
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        results = resp.json()
        organic = results.get('organic_results', [])
        logger.debug(f"SerpAPI returned {len(organic)} results on this page.")
        for res in organic:
            articles.append({
                'url': res.get('link'),
                'headline': res.get('title'),
                'source': res.get('source', ''),
                'publish_date': res.get('date', '')
            })
        if len(organic) < SERPAPI_PAGE_SIZE:
            break  # No more results
        start += SERPAPI_PAGE_SIZE
        if len(articles) >= max_results:
            break
        logger.info(f"Fetched {len(articles)} articles so far...")
        time.sleep(SLEEP_BETWEEN_REQUESTS)
    # Shuffle to avoid only top results
    random.shuffle(articles)
    logger.info(f"Total articles fetched (shuffled): {len(articles)}")
    return articles[:max_results]

# --- ARTICLE SCRAPING ---
def scrape_article(url: str) -> Optional[str]:
    logger.debug(f"Attempting to scrape article with newspaper3k: {url}")
    try:
        art = Article(url)
        art.download()
        art.parse()
        if art.text and len(art.text) > 200:
            logger.debug(f"Successfully scraped with newspaper3k: {url}")
            return art.text
        else:
            logger.debug(f"newspaper3k returned insufficient text for: {url}")
    except Exception as e:
        logger.debug(f"newspaper3k failed for {url}: {e}")
    # Fallback to trafilatura
    logger.debug(f"Falling back to trafilatura for: {url}")
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded)
            if text and len(text) > 200:
                logger.debug(f"Successfully scraped with trafilatura: {url}")
                return text
            else:
                logger.debug(f"trafilatura returned insufficient text for: {url}")
    except Exception as e:
        logger.debug(f"trafilatura failed for {url}: {e}")
    logger.warning(f"Failed to scrape article: {url}")
    return None

# --- GPT-4o ANALYSIS ---
def analyze_article_with_gpt(headline: str, article_text: str) -> Optional[Dict]:
    prompt = f"""
You are an expert media analyst specializing in Digital Humanities and critical discourse analysis.

You will analyze articles about COVID-19 deaths. Your goal is to extract not only the surface-level framing, but also the deeper cultural signals, silences, and omissions in the text.

For each article, perform the following analysis and return a single structured JSON object with these fields:

{{
"tone": "hopeful / neutral / tragic / indifferent / other",
"framing": "preventable / inevitable / personal tragedy / political failure / systemic injustice / other",
"group_mentions": [list of social groups mentioned in relation to COVID deaths — e.g. elderly, racial minorities, working-class, disabled, children, incarcerated people, undocumented immigrants, etc.],
"metaphors": [list of metaphors used — e.g. war, fight, disaster, natural process, cleansing, sacrifice, other],
"euphemisms": [list of euphemistic phrases used to avoid mentioning death directly, if any],
"absences": [list of notable groups, causes, or systemic factors that are NOT mentioned but are likely relevant — e.g. poverty, racism, elder neglect, long COVID, workplace safety, healthcare access],
"grief_handling": "Does the article frame grief as private, public, communal, absent, or other?",
"blame_or_agency": "Does the article assign responsibility for COVID deaths? If so, to whom or what? If not, does it suggest the deaths were unavoidable?",
"commodification_of_death": "Does the article implicitly or explicitly treat death as a statistic, cost of doing business, political talking point, or something else?"
}}

Guidelines:

Do NOT simply summarize the article.
Pay special attention to who is visible and who is invisible in the narrative.
Pay attention to subtle language choices that downplay or depoliticize death.
Identify when grief is absent or individualized rather than collectivized.
Treat omissions as analytically meaningful — absences matter as much as presences.
Return only the JSON object. No extra text or explanation.

Headline: {headline}
Text: {article_text}
"""
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    try:
        logger.debug(f"Sending article to GPT-4o for analysis. Headline: {headline[:60]}")
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=60)
        resp.raise_for_status()
        content = resp.json()['choices'][0]['message']['content']
        logger.debug(f"GPT-4o raw response: {content[:500]}...")
        # Remove code block markers if present
        content = re.sub(r'^```json\s*|^```|```$', '', content.strip(), flags=re.MULTILINE)
        content = content.strip()
        return json.loads(content)
    except Exception as e:
        logger.warning(f"GPT analysis failed: {e}")
        return None

# --- MAIN AGENT LOGIC ---
def main():
    logger.info(f"Querying SerpAPI: {SEARCH_QUERY}")
    articles = search_serpapi(SEARCH_QUERY, max_results=MAX_RESULTS)
    logger.info(f"Found {len(articles)} articles.")

    success_count = 0
    scrape_fail_count = 0
    gpt_fail_count = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for idx, art in enumerate(articles, 1):
            url = art['url']
            logger.info(f"[{idx}/{len(articles)}] Scraping: {url}")
            text = scrape_article(url)
            if not text:
                logger.warning(f"Could not scrape article: {url}")
                scrape_fail_count += 1
                continue
            logger.info(f"Running GPT-4o analysis for: {art['headline']}")
            gpt_result = analyze_article_with_gpt(art['headline'], text)
            if not gpt_result:
                logger.warning(f"GPT analysis failed for: {url}")
                gpt_fail_count += 1
                continue
            result = {
                "publish_date": art.get("publish_date", ""),
                "source": art.get("source", ""),
                "headline": art.get("headline", ""),
                "url": url,
                "article_text": text,
                "gpt_analysis": gpt_result
            }
            logger.info(f"Writing result for: {url}")
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
            f.flush()
            success_count += 1
            logger.debug(f"Sleeping for {SLEEP_BETWEEN_REQUESTS} seconds to avoid rate limits.")
            time.sleep(SLEEP_BETWEEN_REQUESTS)

    logger.info(f"Done! Results saved to {OUTPUT_FILE}")
    logger.info(f"Summary: {success_count} successful, {scrape_fail_count} scrape failures, {gpt_fail_count} GPT failures out of {len(articles)} articles.")

# Load spaCy model for named entity recognition
nlp = spacy.load("en_core_web_sm")

def extract_locations(text: str) -> List[str]:
    """
    Extract location names from text using spaCy's named entity recognition.
    """
    doc = nlp(text)
    locations = []
    for ent in doc.ents:
        if ent.label_ in ['GPE', 'LOC']:  # GPE = Geo-Political Entity, LOC = Location
            locations.append(ent.text)
    return locations

def process_jsonl_file(input_file: str, output_file: str):
    """
    Process the JSONL file to add location information from headlines.
    """
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            try:
                data = json.loads(line.strip())
                
                # Extract locations from headline
                headline = data.get('headline', '')
                locations = extract_locations(headline)
                
                # Add locations to the data
                data['locations'] = locations
                
                # Write the updated data
                f_out.write(json.dumps(data) + '\n')
                
            except json.JSONDecodeError:
                print(f"Error decoding JSON line: {line}")
                continue

if __name__ == "__main__":
    main()
    input_file = "covid_media_serp_results.jsonl"
    output_file = "covid_media_serp_results_with_locations.jsonl"
    process_jsonl_file(input_file, output_file)