import json

# Read the JSONL file and check locations
articles = []
with open('covid_media_serp_results_with_locations.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            articles.append(json.loads(line.strip()))
        except json.JSONDecodeError:
            continue

print(f"Total articles loaded: {len(articles)}")

# Check locations
all_locations = set()
matched_locations = set()
unmatched_locations = set()

# Enhanced coordinate lookup (same as in the map script)
COORDS = {
    'New York': [40.7128, -74.0060],
    'New York City': [40.7128, -74.0060],
    'California': [36.7783, -119.4179],
    'Oregon': [44.0582, -121.3153],
    'Indiana': [39.7684, -86.1581],
    'Illinois': [40.6331, -89.3985],
    'Texas': [31.9686, -99.9018],
    'Washington': [47.6062, -122.3321],
    'Italy': [41.8719, 12.5674],
    'China': [35.8617, 104.1954],
    'France': [46.6034, 1.8883],
    'Spain': [40.4637, -3.7492],
    'Germany': [51.1657, 10.4515],
    'Japan': [36.2048, 138.2529],
    'South Korea': [35.9078, 127.7669],
    'United States': [37.0902, -95.7129],
    'Connecticut': [41.6032, -73.0877],
    'Michigan': [44.3148, -85.6024],
    'Maine': [44.6939, -69.3819],
    'Delaware': [39.3185, -75.5071],
    'Kentucky': [37.6681, -84.6701],
    'Massachusetts': [42.2304, -71.5301],
    'Arkansas': [35.2010, -91.8318],
    'Jonesboro': [35.8423, -90.7043],
    'Virginia': [37.4316, -78.6569],
    'Hong Kong': [22.3193, 114.1694],
    'Tokyo': [35.6762, 139.6503],
    'Yokohama': [35.4437, 139.6380],
    'Milan': [45.4642, 9.1900],
    'Bergamo': [45.6983, 9.6773],
    'Lombardy': [45.6983, 9.6773],
    'Iran': [32.4279, 53.6880],
    'Canada': [56.1304, -106.3468],
    'Lebanon': [33.8547, 35.8623],
    'Afghanistan': [33.9391, 67.7100],
    'Iraq': [33.2232, 43.6793],
    'San Francisco': [37.7749, -122.4194],
    'Kirkland': [47.6815, -122.2087],
    'Wash.': [47.6062, -122.3321],
    'Manhattan': [40.7831, -73.9712],
    'Northern California': [37.7749, -122.4194],
    'The Bay Area': [37.7749, -122.4194],
    'Davis': [38.5449, -121.7405],
    'Hawaii': [19.8968, -155.5828],
    'Calif.': [36.7783, -119.4179],
    'Conn.': [41.6032, -73.0877],
    'New Haven': [41.3083, -72.9279],
    'New Orleans': [29.9511, -90.0715],
    'The United States': [37.0902, -95.7129],
    'The United States Of America': [37.0902, -95.7129],
    'Us': [37.0902, -95.7129],
    'America': [37.0902, -95.7129],
    'Europe': [54.5260, 15.2551],
    'Africa': [8.7832, 34.5085],
    'Asia': [34.0479, 100.6197],
    'West Africa': [8.7832, -11.2090],
    'Ebola': [8.7832, -11.2090],
    'Wuhan': [30.5928, 114.3055],
    'Beijing': [39.9042, 116.4074],
    'Nairobi': [-1.2921, 36.8219],
    'Washington DC': [38.9072, -77.0369],
    'Washington, D.C.': [38.9072, -77.0369],
    'Atlantic': [29.9511, -90.0715],
    'Virginia County': [37.4316, -78.6569],
    'The San Francisco Bay Area': [37.7749, -122.4194],
    'History United': [37.0902, -95.7129],
    'I.C.U': [37.0902, -95.7129],
    'Atalanta': [45.6983, 9.6773],
    'Valencia': [39.4699, -0.3763],
    'Champions League': [45.6983, 9.6773],
    'New York City\'S': [40.7128, -74.0060],
    'New York City Region': [40.7128, -74.0060],
    'The United States Of America': [37.0902, -95.7129]
}

for article in articles:
    locations = article.get('location', [])
    if locations:
        for loc in locations:
            all_locations.add(loc.strip())
            if loc.strip() in COORDS:
                matched_locations.add(loc.strip())
            else:
                unmatched_locations.add(loc.strip())

print(f"Total unique locations found: {len(all_locations)}")
print(f"Locations with coordinates: {len(matched_locations)}")
print(f"Locations without coordinates: {len(unmatched_locations)}")

print("\nMatched locations:")
for loc in sorted(matched_locations):
    print(f"  ✓ {loc}")

print("\nUnmatched locations:")
for loc in sorted(unmatched_locations):
    print(f"  ✗ {loc}")

# Count articles per matched location
location_counts = {}
for article in articles:
    locations = article.get('location', [])
    if locations:
        first_loc = locations[0].strip()
        if first_loc in COORDS:
            location_counts[first_loc] = location_counts.get(first_loc, 0) + 1

print(f"\nArticles per matched location:")
for loc, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {loc}: {count} articles") 