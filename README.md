# Uncounted Lives: COVID-19 Data Gaps and Systemic Erasure

## Project Overview

Uncounted Lives investigates how the COVID-19 pandemic didn't just take lives—it erased them from the record. Our project reveals the disturbing gaps in vaccine and mortality data that disproportionately affect marginalized communities in the U.S., including Native Americans, undocumented immigrants, the unhoused, and essential workers of color.

Using CDC vaccination datasets and metadata from The COVID Tracking Project, we show how "Unknown" isn't just a missing label—it's a systemic failure. These gaps reflect political decisions, institutional neglect, and historical patterns of exclusion that silence the very people most harmed by the pandemic.

Our mission is simple: make the invisible visible. By critiquing the architecture of public health data through a lens of equity and data feminism, we demand a future where every life counts—and is counted.

## Research Questions

- How do data collection practices systematically exclude marginalized communities?
- What patterns emerge when we analyze the "Unknown" categories in public health datasets?
- How can we visualize and communicate the human cost of data gaps?
- What does the architecture of public health data reveal about institutional priorities?

## Methodology

This project employs a mixed-methods approach combining:

- **Quantitative Analysis**: Statistical examination of CDC vaccination and mortality datasets
- **Qualitative Content Analysis**: Discourse analysis of public health communications
- **Data Visualization**: Creation of wordclouds and other visual representations to reveal patterns
- **Critical Data Studies**: Application of data feminism and equity frameworks

## Repository Contents

### Data Processing Scripts
- `covid_media_serp_agent.py` - Automated data collection from public health sources
- `add_locations.py` - Geographic data enrichment
- `convert_to_json.py` - Data format conversion utilities
- `json_to_csv.py` - Export functionality for analysis

### Analysis Tools
- `create_wordcloud.py` - Generates wordcloud visualizations for thematic analysis
- `check_csv.py` - Data quality and completeness assessment

### Data Files
- `dh.csv` - Processed dataset for analysis
- `dh.json` - JSON format of the dataset
- `covid_media_serp_results.jsonl` - Raw collected data

## Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/gyanbhambhani/dh100.git
cd dh100
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (create a `.env` file):
```
# Add your API keys and configuration here
```

## Usage

### Generating Wordclouds
To create visualizations of thematic patterns in the data:

```bash
python create_wordcloud.py
```

This will generate:
- Individual wordclouds for each analysis category
- A combined visualization showing all categories together

### Data Analysis Categories
The wordcloud analysis examines these key themes:
- **Tone**: Emotional and rhetorical characteristics of public health communications
- **Framing**: How COVID-19 is conceptualized and presented
- **Group Mentions**: Which communities are included or excluded from narratives
- **Metaphors**: Figurative language used to describe the pandemic
- **Euphemisms**: Indirect language around death and illness
- **Absences**: What's missing from public health discourse
- **Grief Handling**: How loss and bereavement are addressed
- **Blame or Agency**: Attribution of responsibility and causality
- **Commodification of Death**: Economic framing of mortality

## Key Findings

*[This section will be populated as analysis progresses]*

## Contributing

This is a research project focused on data justice and public health equity. We welcome contributions that:

- Improve data collection and processing methods
- Enhance visualization techniques
- Strengthen the theoretical framework
- Expand the scope of analysis

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The COVID Tracking Project for their comprehensive data collection
- CDC for providing public health datasets
- The data feminism community for theoretical frameworks
- All communities affected by COVID-19 data gaps

## Contact

For questions about this research, please open an issue on GitHub or contact the research team.

---

*"The most important thing is to make sure that we're not just counting the dead, but counting the living who are being left behind."* - Dr. Camara Jones 