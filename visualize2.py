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
    df = df[(df['Date'] >= '2021-01-01') & (df['Date'] <= '2021-07-31')].copy()

    df['Series_Complete_Yes'] = pd.to_numeric(df['Series_Complete_Yes'], errors='coerce').fillna(0)
    
    # Clean up demographic categories
    df['Simple_Category'] = df['Demographic_category'].str.replace('Race_eth_', '', regex=False).str.replace('_', ' ').str.title().str.strip()

    # --- Correctly identify the 'Unknown' category for Race/Ethnicity ---
    unknown_key = 'Unknown'
    if unknown_key not in df['Simple_Category'].unique():
         raise ValueError("Could not find the specific 'Unknown' category for race/ethnicity in the data.")
    else:
        print(f"Correctly identified 'Unknown' Race/Ethnicity category.")

    # --- Calculate the Share of Daily New Vaccinations with Unknown Race ---
    
    # Pivot to get cumulative vaccinations by category over time
    pivot_df = df.pivot_table(index='Date', columns='Simple_Category', values='Series_Complete_Yes').fillna(0)
    
    # Calculate the number of NEW vaccinations each day
    daily_new_vax = pivot_df.diff().fillna(0)
    daily_new_vax[daily_new_vax < 0] = 0 # Remove negative values from data corrections

    # Calculate the total new vaccinations each day
    total_daily_new = daily_new_vax.sum(axis=1)
    
    # Calculate the share of new daily vaccinations that are "Unknown"
    daily_pct_unknown = (daily_new_vax[unknown_key] / total_daily_new) * 100
    
    # Use a 14-day rolling average to smooth out daily noise
    daily_pct_unknown_smoothed = daily_pct_unknown.rolling(window=14).mean()

    # --- Plotting ---
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(14, 8))

    # Plot the smoothed percentage of unknowns
    ax.plot(daily_pct_unknown_smoothed.index, daily_pct_unknown_smoothed, color='#c51b8a', linewidth=3)
    
    # --- Enhancing the Storytelling ---
    ax.set_title('A Crisis of Clarity: The Early Vaccine Data Gap', fontsize=22, weight='bold', loc='left', pad=40)
    plt.figtext(0.09, 0.92, "In the critical early months, a significant percentage of daily vaccination records were missing race and ethnicity data.",
                fontsize=14, ha='left', style='italic', color='gray')
    
    ax.set_xlabel('Month (2021)', fontsize=12, weight='bold')
    ax.set_ylabel('Share of Daily Vaccinations with Unknown Race (14-Day Avg)', fontsize=12, weight='bold')
    
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100.0))
    ax.set_ylim(0)
    ax.tick_params(axis='both', which='major', labelsize=12)

    # --- ANNOTATION HAS BEEN REMOVED ---

    plt.figtext(0.9, 0.01, "Source: data.cdc.gov", ha="right", fontsize=10, color="gray")
    plt.tight_layout(rect=[0, 0.03, 1, 0.88])
    plt.show()

except Exception as e:
    print(f"An error occurred: {e}")