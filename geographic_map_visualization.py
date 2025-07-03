import json
import folium
from collections import defaultdict
import random

# Enhanced coordinate lookup - Focused on US locations
COORDS = {
    # Major US States
    'New York': [40.7128, -74.0060],
    'New York City': [40.7128, -74.0060],
    'California': [36.7783, -119.4179],
    'Oregon': [44.0582, -121.3153],
    'Indiana': [39.7684, -86.1581],
    'Illinois': [40.6331, -89.3985],
    'Texas': [31.9686, -99.9018],
    'Washington': [47.6062, -122.3321],
    'Connecticut': [41.6032, -73.0877],
    'Michigan': [44.3148, -85.6024],
    'Maine': [44.6939, -69.3819],
    'Delaware': [39.3185, -75.5071],
    'Kentucky': [37.6681, -84.6701],
    'Massachusetts': [42.2304, -71.5301],
    'Arkansas': [35.2010, -91.8318],
    'Virginia': [37.4316, -78.6569],
    'Florida': [27.6648, -81.5158],
    'Ohio': [40.4173, -82.9071],
    'Pennsylvania': [40.5908, -77.2098],
    'Georgia': [32.1656, -82.9001],
    'North Carolina': [35.7596, -79.0193],
    'South Carolina': [33.8569, -80.9450],
    'Tennessee': [35.7478, -86.6923],
    'Alabama': [32.3182, -86.9023],
    'Mississippi': [32.7416, -89.6787],
    'Louisiana': [31.1695, -91.8678],
    'Missouri': [38.4561, -92.2884],
    'Iowa': [41.8780, -93.0977],
    'Minnesota': [46.7296, -94.6859],
    'Wisconsin': [43.7844, -88.7879],
    'Kansas': [38.5111, -96.8005],
    'Nebraska': [41.4925, -99.9018],
    'South Dakota': [44.2998, -99.4388],
    'North Dakota': [47.5515, -101.0020],
    'Montana': [46.8797, -110.3626],
    'Idaho': [44.0682, -114.7420],
    'Wyoming': [42.7475, -107.2085],
    'Colorado': [39.5501, -105.7821],
    'Utah': [39.3209, -111.0937],
    'Arizona': [33.7298, -111.4312],
    'New Mexico': [34.5199, -105.8701],
    'Nevada': [38.8026, -116.4194],
    'Alaska': [64.2008, -149.4937],
    'Hawaii': [19.8968, -155.5828],
    
    # Major US Cities
    'San Francisco': [37.7749, -122.4194],
    'Kirkland': [47.6815, -122.2087],
    'Manhattan': [40.7831, -73.9712],
    'Davis': [38.5449, -121.7405],
    'New Haven': [41.3083, -72.9279],
    'New Orleans': [29.9511, -90.0715],
    'Washington DC': [38.9072, -77.0369],
    'Washington, D.C.': [38.9072, -77.0369],
    'Los Angeles': [34.0522, -118.2437],
    'Chicago': [41.8781, -87.6298],
    'Houston': [29.7604, -95.3698],
    'Phoenix': [33.4484, -112.0740],
    'Philadelphia': [39.9526, -75.1652],
    'San Antonio': [29.4241, -98.4936],
    'San Diego': [32.7157, -117.1611],
    'Dallas': [32.7767, -96.7970],
    'San Jose': [37.3382, -121.8863],
    'Austin': [30.2672, -97.7431],
    'Jacksonville': [30.3322, -81.6557],
    'Fort Worth': [32.7555, -97.3308],
    'Columbus': [39.9612, -82.9988],
    'Charlotte': [35.2271, -80.8431],
    'San Francisco Bay Area': [37.7749, -122.4194],
    'The Bay Area': [37.7749, -122.4194],
    'Northern California': [37.7749, -122.4194],
    
    # US Abbreviations and Variations
    'Calif.': [36.7783, -119.4179],
    'Conn.': [41.6032, -73.0877],
    'Wash.': [47.6062, -122.3321],
    'The United States': [37.0902, -95.7129],
    'The United States Of America': [37.0902, -95.7129],
    'Us': [37.0902, -95.7129],
    'America': [37.0902, -95.7129],
    'New York City\'S': [40.7128, -74.0060],
    'New York City Region': [40.7128, -74.0060],
    'Virginia County': [37.4316, -78.6569],
    'The San Francisco Bay Area': [37.7749, -122.4194],
    'History United': [37.0902, -95.7129],
    'I.C.U': [37.0902, -95.7129],
    'Atlantic': [29.9511, -90.0715],
    
    # Specific US Locations
    'Jonesboro': [35.8423, -90.7043],
    
    # Keep some international locations for reference but they won't be shown on US-focused map
    'Italy': [41.8719, 12.5674],
    'China': [35.8617, 104.1954],
    'France': [46.6034, 1.8883],
    'Spain': [40.4637, -3.7492],
    'Germany': [51.1657, 10.4515],
    'Japan': [36.2048, 138.2529],
    'South Korea': [35.9078, 127.7669],
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
    'Europe': [54.5260, 15.2551],
    'Africa': [8.7832, 34.5085],
    'Asia': [34.0479, 100.6197],
    'West Africa': [8.7832, -11.2090],
    'Ebola': [8.7832, -11.2090],
    'Wuhan': [30.5928, 114.3055],
    'Beijing': [39.9042, 116.4074],
    'Nairobi': [-1.2921, 36.8219],
    'Atalanta': [45.6983, 9.6773],
    'Valencia': [39.4699, -0.3763],
    'Champions League': [45.6983, 9.6773],
}

# US location identifiers for filtering
US_LOCATIONS = {
    'New York', 'New York City', 'California', 'Oregon', 'Indiana', 'Illinois', 'Texas', 
    'Washington', 'Connecticut', 'Michigan', 'Maine', 'Delaware', 'Kentucky', 'Massachusetts', 
    'Arkansas', 'Virginia', 'Florida', 'Ohio', 'Pennsylvania', 'Georgia', 'North Carolina', 
    'South Carolina', 'Tennessee', 'Alabama', 'Mississippi', 'Louisiana', 'Missouri', 'Iowa', 
    'Minnesota', 'Wisconsin', 'Kansas', 'Nebraska', 'South Dakota', 'North Dakota', 'Montana', 
    'Idaho', 'Wyoming', 'Colorado', 'Utah', 'Arizona', 'New Mexico', 'Nevada', 'Alaska', 'Hawaii',
    'San Francisco', 'Kirkland', 'Manhattan', 'Davis', 'New Haven', 'New Orleans', 'Washington DC', 
    'Washington, D.C.', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 
    'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte',
    'San Francisco Bay Area', 'The Bay Area', 'Northern California', 'Calif.', 'Conn.', 'Wash.',
    'The United States', 'The United States Of America', 'Us', 'America', 'New York City\'S', 
    'New York City Region', 'Virginia County', 'The San Francisco Bay Area', 'History United', 
    'I.C.U', 'Atlantic', 'Jonesboro'
}

def extract_first_location(loc_list):
    """Extract the first location from a list of locations"""
    if not loc_list or not isinstance(loc_list, list):
        return None
    return loc_list[0].strip() if loc_list[0].strip() else None

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
    <div style="width: 400px; font-family: Arial, sans-serif;">
        <h3 style="margin: 0 0 15px 0; color: #2c3e50; font-size: 16px; border-bottom: 2px solid #3498db; padding-bottom: 5px;">{headline}</h3>
        <p style="margin: 8px 0; font-size: 14px;"><strong style="color: #34495e;">Source:</strong> {source}</p>
        <p style="margin: 8px 0; font-size: 14px;"><strong style="color: #34495e;">Tone:</strong> <span style="color: #e74c3c; font-weight: bold;">{tone}</span></p>
        <p style="margin: 8px 0; font-size: 14px;"><strong style="color: #34495e;">Framing:</strong> <span style="color: #3498db; font-weight: bold;">{framing}</span></p>
        <p style="margin: 8px 0; font-size: 14px;"><strong style="color: #34495e;">Groups:</strong> {groups_str}</p>
        <p style="margin: 8px 0; font-size: 14px;"><strong style="color: #34495e;">Metaphors:</strong> {metaphors_str}</p>
    </div>
    """
    return popup_html

def add_random_offset(lat, lon, max_offset=0.3):
    """Add small random offset to prevent exact overlapping"""
    lat_offset = random.uniform(-max_offset, max_offset)
    lon_offset = random.uniform(-max_offset, max_offset)
    return lat + lat_offset, lon + lon_offset

def main():
    # Read the JSONL file
    articles = []
    with open('covid_media_serp_results_with_locations.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            try:
                articles.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    
    # Create map centered on the US
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles='OpenStreetMap')
    
    # Track locations to avoid duplicates and count articles
    location_counts = defaultdict(int)
    location_articles = defaultdict(list)
    
    # Process each article - filter for US locations only
    for article in articles:
        locations = article.get('location', [])
        if not locations:
            continue
            
        first_loc = extract_first_location(locations)
        if not first_loc or first_loc not in COORDS:
            continue
            
        # Only include US locations
        if first_loc not in US_LOCATIONS:
            continue
            
        location_counts[first_loc] += 1
        location_articles[first_loc].append(article)
    
    # Add markers for each location
    for location, count in location_counts.items():
        if location in COORDS:
            lat, lon = COORDS[location]
            
            # Add small random offset to prevent exact overlapping
            lat, lon = add_random_offset(lat, lon, 0.2)
            
            # Create popup with all articles for this location
            popup_content = f"<h2 style='color: #2c3e50; margin-bottom: 15px;'>{location}</h2>"
            popup_content += f"<p style='font-size: 16px; color: #7f8c8d; margin-bottom: 20px;'><strong>{count} articles</strong></p>"
            
            # Show up to 3 articles in the popup
            for i, article in enumerate(location_articles[location][:3]):
                popup_content += create_popup_content(article)
                if i < 2:  # Add separator between articles
                    popup_content += "<hr style='margin: 20px 0; border: 1px solid #ecf0f1;'>"
            
            if len(location_articles[location]) > 3:
                popup_content += f"<p style='text-align: center; color: #7f8c8d; font-style: italic; margin-top: 15px;'>... and {len(location_articles[location]) - 3} more articles</p>"
            
            # Color code by article count
            if count >= 10:
                icon_color = 'red'
                icon = 'info-sign'
            elif count >= 5:
                icon_color = 'orange'
                icon = 'info-sign'
            elif count >= 2:
                icon_color = 'lightblue'
                icon = 'info-sign'
            else:
                icon_color = 'green'
                icon = 'info-sign'
            
            # Create marker with detailed popup
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_content, max_width=450),
                icon=folium.Icon(color=icon_color, icon=icon),
                tooltip=f"<b>{location}</b><br>{count} articles - Click for details!"
            ).add_to(m)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 320px; height: auto; 
                background-color: white; border:3px solid #34495e; z-index:9999; 
                font-size:16px; padding: 22px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.3);">
    <h4 style="margin: 0 0 14px 0; color: #2c3e50;">US COVID-19 Media Coverage Map</h4>
    <p><span style="color:red;">●</span> 10+ articles (Major coverage)</p>
    <p><span style="color:orange;">●</span> 5-9 articles (Significant coverage)</p>
    <p><span style="color:lightblue;">●</span> 2-4 articles (Moderate coverage)</p>
    <p><span style="color:green;">●</span> 1 article (Mentioned)</p>
    <p style="margin-top: 12px; font-size: 13px; color: #7f8c8d;"><em>Click markers for detailed analysis</em></p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save the map
    m.save('map.html')
    print(f"US-focused map created with {len(location_counts)} locations and {sum(location_counts.values())} articles!")
    print("Open map.html in your browser to view the interactive map.")
    print("Click on any marker to see detailed article analysis!")

if __name__ == "__main__":
    main() 