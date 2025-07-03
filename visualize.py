import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import ssl

# --- SSL Bypass (if needed on your network) ---
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# --- Data Loading and Preparation ---
url = 'https://data.cdc.gov/api/views/km4m-vcsb/rows.csv?accessType=DOWNLOAD'

try:
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
    df = df[df['Date'] <= '2021-07-31'].copy()

    df['Series_Complete_Pop_Pct_US'] = pd.to_numeric(df['Series_Complete_Pop_Pct_US'], errors='coerce').fillna(0)
    
    df['Simple_Category'] = df['Demographic_category'].str.replace('Race_eth_', '', regex=False).str.replace('_', ' ').str.title().str.strip()

    # --- AUTOMATICALLY FIND THE CORRECT CATEGORY NAMES ---
    all_categories = df['Simple_Category'].unique()
    
    groups_to_find = {'White': 'White', 'Hispanic': 'Hispanic', 'Black': 'Black', 'Aapi': 'AAPI'}
    groups_to_plot = []
    colors_map = {}
    key_map = {} 

    print("Automatically identifying plot categories...")
    for keyword, desired_name in groups_to_find.items():
        for cat in all_categories:
            if keyword.lower() in cat.lower():
                groups_to_plot.append(cat)
                key_map[desired_name] = cat
                colors_map[cat] = {'White': 'silver', 'Hispanic': '#1f77b4', 'Black': '#ff7f0e', 'AAPI': '#2ca02c'}[desired_name]
                print(f"  Found '{cat}' for '{desired_name}'")
                break
    
    if not groups_to_plot:
        raise ValueError("Could not find any of the required demographic categories in the data.")
    
    # --- Create the Visualization ---
    pivot_df = df[df['Simple_Category'].isin(groups_to_plot)].pivot_table(
        index='Date',
        columns='Simple_Category',
        values='Series_Complete_Pop_Pct_US'
    ).fillna(0)

    # --- Plotting ---
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(14, 8))

    for group in groups_to_plot:
        ax.plot(pivot_df.index, pivot_df[group], label=group, color=colors_map.get(group, 'gray'), linewidth=3.5)

    # --- Enhancing the Storytelling ---
    
    # --- FURTHER ADJUSTED TITLE POSITIONING ---
    ax.set_title('Beyond Hesitancy: The Story of Vaccine Access and Uptake', fontsize=22, weight='bold', loc='left', pad=60) # Increased padding more
    plt.figtext(0.09, 0.95, 'While some groups had an early lead, rates for Black and Hispanic communities showed strong, sustained growth, indicating high demand.', # Increased Y-position more
                fontsize=14, ha='left', style='italic', color='gray')

    ax.set_xlabel('Month (2021)', fontsize=12, weight='bold')
    ax.set_ylabel('Share of Population Fully Vaccinated', fontsize=12, weight='bold')
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100.0))
    ax.set_ylim(0)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.legend(title='Racial/Ethnic Group', fontsize='large', frameon=True, shadow=True)
    
    # --- DYNAMIC ANNOTATION PLACEMENT ---
    if 'White' in key_map:
        white_key = key_map['White']
        idx_25_percent = int(len(pivot_df.index) * 0.25)
        annotation_date_1 = pivot_df.index[idx_25_percent]
        annotation_y_1 = pivot_df.loc[annotation_date_1, white_key]
        ax.annotate('Early lead suggests\nbetter initial access',
                    xy=(annotation_date_1, annotation_y_1),
                    xytext=(annotation_date_1, annotation_y_1 + 15), 
                    arrowprops=dict(facecolor='black', arrowstyle='->', connectionstyle='arc3,rad=0.1'),
                    fontsize=12, ha='center', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=0.5))

    if 'Hispanic' in key_map:
        hispanic_key = key_map['Hispanic']
        idx_75_percent = int(len(pivot_df.index) * 0.75)
        annotation_date_2 = pivot_df.index[idx_75_percent]
        annotation_y_2 = pivot_df.loc[annotation_date_2, hispanic_key]
        ax.annotate('Strong uptake shows\ndemand, not just hesitancy',
                    xy=(annotation_date_2, annotation_y_2),
                    xytext=(annotation_date_2, annotation_y_2 - 15),
                    arrowprops=dict(facecolor='black', arrowstyle='->', connectionstyle='arc3,rad=0.1'),
                    fontsize=12, ha='center', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=0.5))

    plt.figtext(0.9, 0.01, "Source: data.cdc.gov", ha="right", fontsize=10, color="gray")
    
    # --- FURTHER ADJUSTED LAYOUT TO GIVE MORE SPACE AT THE TOP ---
    plt.tight_layout(rect=[0, 0.03, 1, 0.84]) 
    plt.show()

except Exception as e:
    print(f"An error occurred: {e}")