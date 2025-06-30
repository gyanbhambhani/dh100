import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

categories = [
    'tone', 'framing', 'group_mentions', 'metaphors', 
    'euphemisms', 'absences', 'grief_handling', 
    'blame_or_agency', 'commodification_of_death'
]

# Optional: different orientation preference per category
orientation_prefs = {
    'tone': 0.9,
    'framing': 0.7,
    'group_mentions': 0.5,
    'metaphors': 0.3,
    'euphemisms': 0.6,
    'absences': 0.8,
    'grief_handling': 0.9,
    'blame_or_agency': 0.4,
    'commodification_of_death': 0.5
}

def create_wordcloud(text, ax, prefer_horizontal):
    wordcloud = WordCloud(
        width=400, 
        height=400,
        background_color='white',
        max_words=50,
        contour_width=0,
        prefer_horizontal=prefer_horizontal
    ).generate(text)
    
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

def main():
    df = pd.read_csv('dh.csv')

    # Aggregate text per category
    sample_data = {}
    for category in categories:
        all_text = df[category].dropna().astype(str).str.cat(sep=' ')
        sample_data[category] = all_text
    
    # Grid layout
    n_categories = len(categories)
    n_cols = 3
    n_rows = (n_categories + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    axes = axes.flatten()
    
    # Wordclouds without titles
    for idx, category in enumerate(categories):
        create_wordcloud(
            sample_data[category], 
            axes[idx], 
            orientation_prefs.get(category, 0.75)
        )
    
    # Hide unused plots
    for idx in range(len(categories), len(axes)):
        axes[idx].axis('off')
    
    # Save output
    plt.tight_layout()
    plt.savefig('combined_wordclouds.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Created combined wordcloud visualization")

if __name__ == "__main__":
    main()
