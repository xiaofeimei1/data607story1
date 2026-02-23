import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load the data
file_path = "IIJA FUNDING AS OF MARCH 2023.xlsx" # I saved a copy of file in the same github repository with the py file.
df = pd.read_excel(file_path)

print(f"Shape: {df.shape}")
print("\nFirst few rows:")
print(df.head())
print("\nColumn names:", df.columns.tolist())

df.columns = ['State_Territory_Tribal_Nation', 'Total_Billions']
df_sorted = df.sort_values('Total_Billions', ascending=False)

# figure for basic funding analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('IIJA Funding Allocation Analysis', fontsize=16, fontweight='bold')

# Top 10 States by Total Funding
top_10 = df_sorted.head(10)
bars1 = axes[0,0].barh(top_10['State_Territory_Tribal_Nation'], 
                       top_10['Total_Billions'], color='steelblue')
axes[0,0].set_xlabel('Total Funding (Billions USD)')
axes[0,0].set_title('Top 10 States: Highest Total Funding')
axes[0,0].invert_yaxis()

for bar in bars1:
    width = bar.get_width()
    axes[0,0].text(width, bar.get_y() + bar.get_height()/2, 
                   f'${width:,.2f}B', ha='left', va='center')

# Bottom 10 States by Total Funding
bottom_10 = df_sorted.tail(10)
bars2 = axes[0,1].barh(bottom_10['State_Territory_Tribal_Nation'], 
                       bottom_10['Total_Billions'], color='lightcoral')
axes[0,1].set_xlabel('Total Funding (Billions USD)')
axes[0,1].set_title('Bottom 10 States: Lowest Total Funding')
axes[0,1].invert_yaxis()

for bar in bars2:
    width = bar.get_width()
    axes[0,1].text(width, bar.get_y() + bar.get_height()/2, 
                   f'${width:,.2f}B', ha='left', va='center')

# Add population data (2022 estimates in millions from US Census Bureau)
population_data = {
    'ALABAMA': 5.07, 'ALASKA': 0.73, 'ARIZONA': 7.36, 'ARKANSAS': 3.04,
    'CALIFORNIA': 39.24, 'COLORADO': 5.84, 'CONNECTICUT': 3.61,
    'DELAWARE': 1.02, 'FLORIDA': 22.24, 'GEORGIA': 10.91,
    'HAWAII': 1.46, 'IDAHO': 1.94, 'ILLINOIS': 12.67, 'INDIANA': 6.83,
    'IOWA': 3.20, 'KANSAS': 2.94, 'KENTUCKY': 4.51, 'LOUISIANA': 4.59,
    'MAINE': 1.39, 'MARYLAND': 6.16, 'MASSACHUSETTS': 7.03,
    'MICHIGAN': 10.05, 'MINNESOTA': 5.71, 'MISSISSIPPI': 2.94,
    'MISSOURI': 6.16, 'MONTANA': 1.12, 'NEBRASKA': 1.97,
    'NEVADA': 3.18, 'NEW HAMPSHIRE': 1.40, 'NEW JERSEY': 9.26,
    'NEW MEXICO': 2.12, 'NEW YORK': 19.84, 'NORTH CAROLINA': 10.70,
    'NORTH DAKOTA': 0.78, 'OHIO': 11.76, 'OKLAHOMA': 4.02,
    'OREGON': 4.24, 'PENNSYLVANIA': 12.96, 'RHODE ISLAND': 1.10,
    'SOUTH CAROLINA': 5.28, 'SOUTH DAKOTA': 0.91, 'TENNESSEE': 7.05,
    'TEXAS': 30.03, 'UTAH': 3.38, 'VERMONT': 0.65, 'VIRGINIA': 8.68,
    'WASHINGTON': 7.79, 'WEST VIRGINIA': 1.77, 'WISCONSIN': 5.90,
    'WYOMING': 0.58, 'DISTRICT OF COLUMBIA': 0.67,
    # Territories (approximate populations)
    'PUERTO RICO': 3.26, 'GUAM': 0.17, 'VIRGIN ISLANDS': 0.10,
    'NORTHERN MARIANA ISLANDS': 0.05, 'AMERICAN SAMOA': 0.05
}

# Add to dataframe
df['Population_Millions'] = df['State_Territory_Tribal_Nation'].map(
    lambda x: population_data.get(str(x).strip().upper(), np.nan)
)

# Calculate per capita funding
df['Per_Capita'] = (df['Total_Billions'] * 1_000_000_000) / (df['Population_Millions'] * 1_000_000)  # Convert to dollars per person
df['Per_Capita_Thousands'] = df['Per_Capita'] / 1000  # For display in thousands

print(f"\nStates with population data: {df['Population_Millions'].notna().sum()}")
print(f"States missing population data: {df['Population_Millions'].isna().sum()}")

# Political leaning data based on 2020 presidential election
political_leaning = {
    'ALABAMA': 'Republican', 'ALASKA': 'Republican', 'ARIZONA': 'Swing', 
    'ARKANSAS': 'Republican', 'CALIFORNIA': 'Democratic', 'COLORADO': 'Democratic',
    'CONNECTICUT': 'Democratic', 'DELAWARE': 'Democratic', 'FLORIDA': 'Swing',
    'GEORGIA': 'Swing', 'HAWAII': 'Democratic', 'IDAHO': 'Republican',
    'ILLINOIS': 'Democratic', 'INDIANA': 'Republican', 'IOWA': 'Republican',
    'KANSAS': 'Republican', 'KENTUCKY': 'Republican', 'LOUISIANA': 'Republican',
    'MAINE': 'Democratic', 'MARYLAND': 'Democratic', 'MASSACHUSETTS': 'Democratic',
    'MICHIGAN': 'Swing', 'MINNESOTA': 'Swing', 'MISSISSIPPI': 'Republican',
    'MISSOURI': 'Republican', 'MONTANA': 'Republican', 'NEBRASKA': 'Republican',
    'NEVADA': 'Swing', 'NEW HAMPSHIRE': 'Swing', 'NEW JERSEY': 'Democratic',
    'NEW MEXICO': 'Democratic', 'NEW YORK': 'Democratic', 'NORTH CAROLINA': 'Swing',
    'NORTH DAKOTA': 'Republican', 'OHIO': 'Swing', 'OKLAHOMA': 'Republican',
    'OREGON': 'Democratic', 'PENNSYLVANIA': 'Swing', 'RHODE ISLAND': 'Democratic',
    'SOUTH CAROLINA': 'Republican', 'SOUTH DAKOTA': 'Republican', 'TENNESSEE': 'Republican',
    'TEXAS': 'Republican', 'UTAH': 'Republican', 'VERMONT': 'Democratic',
    'VIRGINIA': 'Swing', 'WASHINGTON': 'Democratic', 'WEST VIRGINIA': 'Republican',
    'WISCONSIN': 'Swing', 'WYOMING': 'Republican', 'DISTRICT OF COLUMBIA': 'Democratic',
    'PUERTO RICO': 'Democratic', 'GUAM': 'Democratic', 'VIRGIN ISLANDS': 'Democratic',
    'NORTHERN MARIANA ISLANDS': 'Democratic', 'AMERICAN SAMOA': 'Democratic'
}

# Add political leaning to dataframe
df['Political_Leaning'] = df['State_Territory_Tribal_Nation'].map(
    lambda x: political_leaning.get(str(x).strip().upper(), 'Unknown')
)

print(f"\nPolitical distribution:")
print(df['Political_Leaning'].value_counts())

# Filter only states with both funding and population data
df_per_capita = df.dropna(subset=['Population_Millions', 'Total_Billions'])

# Create political analysis for per capita funding (just the box plot)
fig, ax = plt.subplots(figsize=(10, 6))

political_order = ['Republican', 'Swing', 'Democratic']
political_colors = {'Republican': 'red', 'Swing': 'gold', 'Democratic': 'blue'}

political_data = []
for leaning in political_order:
    data = df_per_capita[df_per_capita['Political_Leaning'] == leaning]['Per_Capita_Thousands'].dropna()
    political_data.append(data)

bp = ax.boxplot(political_data, labels=political_order, patch_artist=True)
ax.set_ylabel('Per Capita Funding (Thousands USD)')
ax.set_title('Per Capita Funding by Political Leaning')
ax.grid(True, alpha=0.3)

# Color the boxes
for patch, leaning in zip(bp['boxes'], political_order):
    patch.set_facecolor(political_colors[leaning])
    patch.set_alpha(0.6)

# mean markers
for i, (leaning, data) in enumerate(zip(political_order, political_data), 1):
    if len(data) > 0:
        mean_val = data.mean()
        ax.plot(i, mean_val, 'k_', markersize=12, markeredgewidth=2)
        ax.text(i, mean_val, f'${mean_val:.1f}k', 
                ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()

# political analysis visualization for total funding
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Box plot by political leaning (total funding)
political_data_total = []
for leaning in political_order:
    data = df[df['Political_Leaning'] == leaning]['Total_Billions'].dropna()
    political_data_total.append(data)

bp = axes[0].boxplot(political_data_total, labels=political_order, patch_artist=True)
axes[0].set_ylabel('Total Funding (Billions USD)')
axes[0].set_title('Funding Distribution by Political Leaning')
axes[0].grid(True, alpha=0.3)

# Color the boxes
for patch, leaning in zip(bp['boxes'], political_order):
    patch.set_facecolor(political_colors[leaning])
    patch.set_alpha(0.6)

# Add mean markers
for i, (leaning, data) in enumerate(zip(political_order, political_data_total), 1):
    if len(data) > 0:
        mean_val = data.mean()
        axes[0].plot(i, mean_val, 'k_', markersize=12, markeredgewidth=2)
        axes[0].text(i, mean_val, f' ${mean_val:.2f}B', 
                    ha='center', va='bottom', fontweight='bold')

# Pie chart of total funding by political leaning
funding_by_party = df.groupby('Political_Leaning')['Total_Billions'].sum()
funding_by_party = funding_by_party.reindex(political_order)

wedges, texts, autotexts = axes[1].pie(funding_by_party, labels=funding_by_party.index, 
                                       autopct='%1.1f%%', 
                                       colors=[political_colors[p] for p in funding_by_party.index],
                                       startangle=90, explode=(0.05, 0.05, 0.05))
axes[1].set_title('Total Funding Distribution by Political Leaning')

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

# Bar chart of average funding by political leaning
avg_funding_by_party = df.groupby('Political_Leaning')['Total_Billions'].mean()
avg_funding_by_party = avg_funding_by_party.reindex(political_order)

bars = axes[2].bar(avg_funding_by_party.index, avg_funding_by_party.values,
                  color=[political_colors[p] for p in avg_funding_by_party.index],
                  alpha=0.7, edgecolor='black')
axes[2].set_ylabel('Average Funding (Billions USD)')
axes[2].set_title('Average Funding per State by Political Leaning')
axes[2].grid(True, alpha=0.3, axis='y')

#value labels on bars
for bar in bars:
    height = bar.get_height()
    axes[2].text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.2f}B', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()

# statistics
total_funding = df['Total_Billions'].sum()
mean_funding = df['Total_Billions'].mean()
median_funding = df['Total_Billions'].median()
std_funding = df['Total_Billions'].std()
cv_funding = (std_funding / mean_funding) * 100

# Gini coefficient
def gini_coefficient(x):
    x = np.array(x)
    x = x[np.logical_not(np.isnan(x))]
    x = np.sort(x)
    n = len(x)
    index = np.arange(1, n + 1)
    return (np.sum((2 * index - n - 1) * x)) / (n * np.sum(x))

gini = gini_coefficient(df['Total_Billions'])

# Calculate political statistics
if 'Political_Leaning' in df.columns:
    dem_funding = df[df['Political_Leaning'] == 'Democratic']['Total_Billions']
    rep_funding = df[df['Political_Leaning'] == 'Republican']['Total_Billions']
    swing_funding = df[df['Political_Leaning'] == 'Swing']['Total_Billions']
    
    dem_total = dem_funding.sum()
    rep_total = rep_funding.sum()
    swing_total = swing_funding.sum()
    
    dem_avg = dem_funding.mean()
    rep_avg = rep_funding.mean()
    swing_avg = swing_funding.mean()
    
    political_ratio = dem_total / rep_total if rep_total > 0 else np.nan
