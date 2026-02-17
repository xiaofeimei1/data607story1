import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load the data
file_path = r"C:\Users\xmei\Downloads\IIJA FUNDING AS OF MARCH 2023.xlsx"
df = pd.read_excel(file_path)

print("Data loaded successfully!")
print(f"Shape: {df.shape}")
print("\nFirst few rows:")
print(df.head())
print("\nColumn names:", df.columns.tolist())

# Clean column names
df.columns = ['State_Territory_Tribal_Nation', 'Total_Billions']

print(f"\nNumber of states/territories with funding data: {len(df)}")
print(f"Total funding across all states: ${df['Total_Billions'].sum():,.2f} billion")

# Sort by funding amount
df_sorted = df.sort_values('Total_Billions', ascending=False)

# Create figure for basic funding analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('IIJA Funding Allocation Analysis', fontsize=16, fontweight='bold')

# 1. Top 10 States by Total Funding
top_10 = df_sorted.head(10)
bars1 = axes[0,0].barh(top_10['State_Territory_Tribal_Nation'], 
                       top_10['Total_Billions'], color='steelblue')
axes[0,0].set_xlabel('Total Funding (Billions USD)')
axes[0,0].set_title('Top 10 States: Highest Total Funding')
axes[0,0].invert_yaxis()

# Add value labels
for bar in bars1:
    width = bar.get_width()
    axes[0,0].text(width, bar.get_y() + bar.get_height()/2, 
                   f'${width:,.2f}B', ha='left', va='center')

# 2. Bottom 10 States by Total Funding
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

# 3. Funding Distribution Histogram
axes[1,0].hist(df['Total_Billions'], bins=20, edgecolor='black', alpha=0.7, color='skyblue')
axes[1,0].axvline(df['Total_Billions'].mean(), color='red', 
                  linestyle='--', linewidth=2, label=f'Mean: ${df["Total_Billions"].mean():.2f}B')
axes[1,0].axvline(df['Total_Billions'].median(), color='green', 
                  linestyle='--', linewidth=2, label=f'Median: ${df["Total_Billions"].median():.2f}B')
axes[1,0].set_xlabel('Total Funding (Billions USD)')
axes[1,0].set_ylabel('Number of States')
axes[1,0].set_title('Distribution of Total Funding')
axes[1,0].legend()

# 4. Cumulative Funding Distribution
sorted_funding = np.sort(df['Total_Billions'])
cumulative = np.cumsum(sorted_funding)
cumulative_percent = cumulative / cumulative[-1] * 100

axes[1,1].plot(range(1, len(cumulative) + 1), cumulative_percent, 
               'b-', linewidth=2, marker='o', markersize=4)
axes[1,1].axhline(80, color='red', linestyle='--', alpha=0.7, label='80% Threshold')
axes[1,1].fill_between(range(1, len(cumulative) + 1), 0, cumulative_percent, alpha=0.3)
axes[1,1].set_xlabel('Number of States (sorted by funding)')
axes[1,1].set_ylabel('Cumulative Percentage of Total Funding (%)')
axes[1,1].set_title('Cumulative Funding Distribution')
axes[1,1].legend()
axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

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

# Create political analysis visualization
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# 1. Box plot by political leaning (with correct colors)
political_order = ['Republican', 'Swing', 'Democratic']
political_colors = {'Republican': 'red', 'Swing': 'gold', 'Democratic': 'blue'}

political_data = []
for leaning in political_order:
    data = df[df['Political_Leaning'] == leaning]['Total_Billions'].dropna()
    political_data.append(data)

bp = axes[0].boxplot(political_data, labels=political_order, patch_artist=True)
axes[0].set_ylabel('Total Funding (Billions USD)')
axes[0].set_title('Funding Distribution by Political Leaning')
axes[0].grid(True, alpha=0.3)

# Color the boxes with correct colors
for patch, leaning in zip(bp['boxes'], political_order):
    patch.set_facecolor(political_colors[leaning])
    patch.set_alpha(0.6)

# Add mean markers
for i, (leaning, data) in enumerate(zip(political_order, political_data), 1):
    if len(data) > 0:
        mean_val = data.mean()
        axes[0].plot(i, mean_val, 'k_', markersize=12, markeredgewidth=2)
        axes[0].text(i, mean_val, f' ${mean_val:.2f}B', 
                    ha='center', va='bottom', fontweight='bold')

# 2. Pie chart of total funding by political leaning
funding_by_party = df.groupby('Political_Leaning')['Total_Billions'].sum()
funding_by_party = funding_by_party.reindex(political_order)

wedges, texts, autotexts = axes[1].pie(funding_by_party, labels=funding_by_party.index, 
                                       autopct='%1.1f%%', 
                                       colors=[political_colors[p] for p in funding_by_party.index],
                                       startangle=90, explode=(0.05, 0.05, 0.05))
axes[1].set_title('Total Funding Distribution by Political Leaning')

# Make percentages bold
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

# 3. Bar chart of average funding by political leaning
avg_funding_by_party = df.groupby('Political_Leaning')['Total_Billions'].mean()
avg_funding_by_party = avg_funding_by_party.reindex(political_order)

bars = axes[2].bar(avg_funding_by_party.index, avg_funding_by_party.values,
                  color=[political_colors[p] for p in avg_funding_by_party.index],
                  alpha=0.7, edgecolor='black')
axes[2].set_ylabel('Average Funding (Billions USD)')
axes[2].set_title('Average Funding per State by Political Leaning')
axes[2].grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    axes[2].text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.2f}B', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()

# Calculate key statistics
total_funding = df['Total_Billions'].sum()
mean_funding = df['Total_Billions'].mean()
median_funding = df['Total_Billions'].median()
std_funding = df['Total_Billions'].std()
cv_funding = (std_funding / mean_funding) * 100

# Calculate Gini coefficient
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

# Create summary figure
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Left side: Summary statistics
ax_left = axes[0]
ax_left.axis('off')

summary_text = f"""
IIJA FUNDING ANALYSIS SUMMARY
{'='*40}
Dataset Information:
- Total states/territories: {len(df)}
- Total funding amount: ${total_funding:,.2f}B

Distribution Statistics:
- Mean funding: ${mean_funding:,.2f}B
- Median funding: ${median_funding:,.2f}B
- Standard deviation: ${std_funding:,.2f}B
- Coefficient of Variation: {cv_funding:.1f}%

Equity Assessment:
- Gini Coefficient: {gini:.3f}
- Interpretation: {'High inequality' if gini > 0.4 else 'Moderate inequality' if gini > 0.3 else 'Acceptable equality'}
"""

if 'Political_Leaning' in df.columns:
    # Perform t-test
    if len(dem_funding) > 1 and len(rep_funding) > 1:
        t_stat, p_value = stats.ttest_ind(dem_funding, rep_funding, equal_var=False)
    
    summary_text += f"""
Political Analysis:
{'='*40}
Democratic States ({len(dem_funding)}):
- Total: ${dem_total:,.2f}B ({dem_total/total_funding*100:.1f}%)
- Average: ${dem_avg:,.2f}B

Republican States ({len(rep_funding)}):
- Total: ${rep_total:,.2f}B ({rep_total/total_funding*100:.1f}%)
- Average: ${rep_avg:,.2f}B

Swing States ({len(swing_funding)}):
- Total: ${swing_total:,.2f}B ({swing_total/total_funding*100:.1f}%)
- Average: ${swing_avg:,.2f}B

Political Bias Metrics:
- Dem/Rep Total Funding Ratio: {political_ratio:.2f}
- Dem/Rep Average Funding Ratio: {dem_avg/rep_avg:.2f}
"""

    if 't_stat' in locals():
        summary_text += f"""
Statistical Test (Welch's t-test):
- t-statistic: {t_stat:.3f}
- p-value: {p_value:.4f}
- {'SIGNIFICANT difference' if p_value < 0.05 else 'NO significant difference'}
"""

summary_text += f"""
Key Findings:
{'='*40}
1. Equity Assessment: {'The distribution appears UNEQUITABLE' if cv_funding > 30 or gini > 0.4 else 'The distribution appears RELATIVELY EQUITABLE'}

2. Political Bias: """
if 'Political_Leaning' in df.columns:
    if political_ratio > 1.2:
        summary_text += "Favors Democratic states"
    elif political_ratio < 0.8:
        summary_text += "Favors Republican states"
    else:
        summary_text += "Minimal political bias detected"
else:
    summary_text += "Cannot assess without political data"

summary_text += f"""

3. Recommendations:
- {'Consider population data for more accurate equity assessment' if cv_funding > 30 else 'Distribution appears reasonable based on funding alone'}
- {'Investigate potential political factors in allocation' if 'political_ratio' in locals() and abs(political_ratio - 1) > 0.2 else 'Political factors appear balanced'}
- Analyze funding by program category for deeper insights
"""

ax_left.text(0.1, 0.95, summary_text, fontfamily='monospace', 
            fontsize=10, verticalalignment='top', linespacing=1.5)

# Right side: Key visualizations
ax_right = axes[1]

# Create subplots within the right axis
gs = ax_right.inset_axes([0, 0.5, 1, 0.5])  # Top half for scatter plot
gs2 = ax_right.inset_axes([0, 0, 1, 0.5])   # Bottom half for ranking

# Scatter plot: Funding vs Rank
df['Rank'] = df['Total_Billions'].rank(ascending=False)
scatter = gs.scatter(df['Rank'], df['Total_Billions'], 
                    c=df['Total_Billions'], cmap='viridis',
                    s=100, alpha=0.6, edgecolor='black')
gs.set_xlabel('Rank (1 = Highest Funding)')
gs.set_ylabel('Total Funding (Billions USD)')
gs.set_title('Funding vs Rank Distribution')
gs.grid(True, alpha=0.3)

# Add top 5 labels
top_5 = df.nlargest(5, 'Total_Billions')
for _, row in top_5.iterrows():
    gs.text(row['Rank'] + 0.5, row['Total_Billions'], 
            row['State_Territory_Tribal_Nation'], 
            fontsize=8, ha='left', va='center')

# Bar chart of top 10 states
top_10_for_chart = df.nlargest(10, 'Total_Billions')
bars = gs2.barh(range(len(top_10_for_chart)), top_10_for_chart['Total_Billions'][::-1],
               color=plt.cm.viridis(top_10_for_chart['Total_Billions'][::-1]/top_10_for_chart['Total_Billions'].max()))
gs2.set_yticks(range(len(top_10_for_chart)))
gs2.set_yticklabels(top_10_for_chart['State_Territory_Tribal_Nation'][::-1])
gs2.set_xlabel('Funding (Billions USD)')
gs2.set_title('Top 10 States by Funding')
gs2.invert_yaxis()

# Add funding values
for i, (bar, val) in enumerate(zip(bars, top_10_for_chart['Total_Billions'][::-1])):
    gs2.text(val, i, f'${val:.2f}B', va='center', ha='left', fontsize=8)

plt.suptitle('COMPREHENSIVE IIJA FUNDING ANALYSIS', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# Print final conclusions
print("\n" + "="*60)
print("FINAL CONCLUSIONS")
print("="*60)

print(f"\n1. EQUITY ASSESSMENT (based on funding distribution):")
print(f"   - Coefficient of Variation: {cv_funding:.1f}%")
if cv_funding > 30:
    print("   - WARNING: High inequality in funding distribution (CV > 30%)")
else:
    print("   - Funding distribution shows moderate equality")

print(f"   - Gini Coefficient: {gini:.3f}")
if gini > 0.4:
    print("   - WARNING: High inequality (Gini > 0.4)")
elif gini > 0.3:
    print("   - Moderate inequality (Gini 0.3-0.4)")
else:
    print("   - Acceptable equality (Gini < 0.3)")

if 'Political_Leaning' in df.columns:
    print(f"\n2. POLITICAL BIAS ASSESSMENT:")
    print(f"   - Democratic/Republican Total Funding Ratio: {political_ratio:.2f}")
    if political_ratio > 1.2:
        print("   - EVIDENCE OF BIAS: Funding favors Democratic states")
    elif political_ratio < 0.8:
        print("   - EVIDENCE OF BIAS: Funding favors Republican states")
    else:
        print("   - NO SIGNIFICANT BIAS: Funding appears politically balanced")
    
    print(f"   - Democratic/Republican Average Funding Ratio: {dem_avg/rep_avg:.2f}")
    
    if 't_stat' in locals():
        print(f"\n3. STATISTICAL SIGNIFICANCE:")
        print(f"   - p-value: {p_value:.4f}")
        if p_value < 0.05:
            print("   - STATISTICALLY SIGNIFICANT: Political difference is real")
            if dem_avg > rep_avg:
                print("   - Democratic states receive significantly MORE funding")
            else:
                print("   - Republican states receive significantly MORE funding")
        else:
            print("   - NOT STATISTICALLY SIGNIFICANT: No real political difference")

print(f"\n4. TOP RECIPIENTS:")
top_3 = df.nlargest(3, 'Total_Billions')
for i, (_, row) in enumerate(top_3.iterrows(), 1):
    print(f"   {i}. {row['State_Territory_Tribal_Nation']}: ${row['Total_Billions']:.2f}B")

print(f"\n5. BOTTOM RECIPIENTS:")
bottom_3 = df.nsmallest(3, 'Total_Billions')
for i, (_, row) in enumerate(bottom_3.iterrows(), 1):
    print(f"   {i}. {row['State_Territory_Tribal_Nation']}: ${row['Total_Billions']:.2f}B")

print("\n" + "="*60)
print("RECOMMENDATIONS FOR FURTHER ANALYSIS:")
print("="*60)
print("1. Merge with population data for per-capita analysis")
print("2. Analyze funding by specific program categories")
print("3. Compare with historical infrastructure funding patterns")
print("4. Consider regional economic factors and needs")
print("5. Examine funding formulas and allocation methodologies")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load the funding data
file_path = r"C:\Users\xmei\Downloads\IIJA FUNDING AS OF MARCH 2023.xlsx"
df = pd.read_excel(file_path)
df.columns = ['State_Territory_Tribal_Nation', 'Total_Billions']

print("Funding data loaded successfully!")
print(f"Number of states/territories: {len(df)}")
print(f"Total funding: ${df['Total_Billions'].sum():,.2f} billion")

# Add population data (2022 estimates in millions from US Census Bureau)
# Note: You can update this with actual Census data
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

# Add population to dataframe
df['Population_Millions'] = df['State_Territory_Tribal_Nation'].map(
    lambda x: population_data.get(str(x).strip().upper(), np.nan)
)

# Calculate per capita funding
df['Per_Capita'] = (df['Total_Billions'] * 1_000_000_000) / (df['Population_Millions'] * 1_000_000)  # Convert to dollars per person
df['Per_Capita_Thousands'] = df['Per_Capita'] / 1000  # For display in thousands

print(f"\nStates with population data: {df['Population_Millions'].notna().sum()}")
print(f"States missing population data: {df['Population_Millions'].isna().sum()}")

# Create comprehensive per capita analysis
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('IIJA Funding Per Capita Analysis: Is Funding Equitable by Population?', 
             fontsize=16, fontweight='bold')

# Filter only states with both funding and population data
df_per_capita = df.dropna(subset=['Population_Millions', 'Total_Billions'])
df_per_capita = df_per_capita.sort_values('Per_Capita', ascending=False)

print(f"\nAnalyzing {len(df_per_capita)} states with complete data")

# 1. Top 10 States by Per Capita Funding
top_10 = df_per_capita.head(10)
bars1 = axes[0,0].barh(top_10['State_Territory_Tribal_Nation'], 
                       top_10['Per_Capita_Thousands'], color='darkgreen')
axes[0,0].set_xlabel('Funding per Person (Thousands USD)')
axes[0,0].set_title('Top 10: Highest Per Capita Funding')
axes[0,0].invert_yaxis()

for bar in bars1:
    width = bar.get_width()
    axes[0,0].text(width, bar.get_y() + bar.get_height()/2, 
                   f'${width:,.1f}k', ha='left', va='center')

# 2. Bottom 10 States by Per Capita Funding
bottom_10 = df_per_capita.tail(10)
bars2 = axes[0,1].barh(bottom_10['State_Territory_Tribal_Nation'], 
                       bottom_10['Per_Capita_Thousands'], color='darkred')
axes[0,1].set_xlabel('Funding per Person (Thousands USD)')
axes[0,1].set_title('Bottom 10: Lowest Per Capita Funding')
axes[0,1].invert_yaxis()

for bar in bars2:
    width = bar.get_width()
    axes[0,1].text(width, bar.get_y() + bar.get_height()/2, 
                   f'${width:,.1f}k', ha='left', va='center')

# 3. Per Capita Distribution Histogram
axes[0,2].hist(df_per_capita['Per_Capita_Thousands'], bins=20, 
               edgecolor='black', alpha=0.7, color='purple')
axes[0,2].axvline(df_per_capita['Per_Capita_Thousands'].mean(), color='red', 
                  linestyle='--', linewidth=2, 
                  label=f'Mean: ${df_per_capita["Per_Capita_Thousands"].mean():.1f}k')
axes[0,2].axvline(df_per_capita['Per_Capita_Thousands'].median(), color='green', 
                  linestyle='--', linewidth=2, 
                  label=f'Median: ${df_per_capita["Per_Capita_Thousands"].median():.1f}k')
axes[0,2].set_xlabel('Funding per Person (Thousands USD)')
axes[0,2].set_ylabel('Number of States')
axes[0,2].set_title('Distribution of Per Capita Funding')
axes[0,2].legend()

# 4. Scatter Plot: Total Funding vs Population
scatter = axes[1,0].scatter(df_per_capita['Population_Millions'], 
                           df_per_capita['Total_Billions'],
                           c=df_per_capita['Per_Capita_Thousands'], 
                           cmap='viridis', s=100, alpha=0.7, edgecolor='black')
axes[1,0].set_xlabel('Population (Millions)')
axes[1,0].set_ylabel('Total Funding (Billions USD)')
axes[1,0].set_title('Funding vs Population (Color = Per Capita)')
cbar = plt.colorbar(scatter, ax=axes[1,0])
cbar.set_label('Per Capita (Thousands USD)')

# Add state labels for outliers
for _, row in df_per_capita.nlargest(5, 'Per_Capita_Thousands').iterrows():
    axes[1,0].annotate(row['State_Territory_Tribal_Nation'], 
                      (row['Population_Millions'], row['Total_Billions']),
                      fontsize=8, alpha=0.8)

# 5. Per Capita vs Population
axes[1,1].scatter(df_per_capita['Population_Millions'], 
                 df_per_capita['Per_Capita_Thousands'],
                 s=50, alpha=0.6, color='blue')
axes[1,1].set_xlabel('Population (Millions)')
axes[1,1].set_ylabel('Per Capita Funding (Thousands USD)')
axes[1,1].set_title('Per Capita Funding vs Population')
axes[1,1].grid(True, alpha=0.3)

# Add trend line
if len(df_per_capita) > 2:
    z = np.polyfit(df_per_capita['Population_Millions'], 
                  df_per_capita['Per_Capita_Thousands'], 1)
    p = np.poly1d(z)
    x_range = np.linspace(df_per_capita['Population_Millions'].min(), 
                         df_per_capita['Population_Millions'].max(), 100)
    axes[1,1].plot(x_range, p(x_range), 'r--', alpha=0.8, 
                  label=f'Trend: y={z[0]:.3f}x+{z[1]:.2f}')
    axes[1,1].legend()

# 6. Equity Ratio Analysis
# Calculate what funding would be if distributed purely by population
total_funding = df_per_capita['Total_Billions'].sum()
total_population = df_per_capita['Population_Millions'].sum()

df_per_capita['Expected_Equitable'] = (df_per_capita['Population_Millions'] / total_population) * total_funding
df_per_capita['Equity_Ratio'] = df_per_capita['Total_Billions'] / df_per_capita['Expected_Equitable']

# Sort by equity ratio
df_equity = df_per_capita.sort_values('Equity_Ratio', ascending=False)

# Create horizontal bar chart
y_pos = np.arange(len(df_equity))
bars = axes[1,2].barh(y_pos, df_equity['Equity_Ratio'])
axes[1,2].set_yticks(y_pos)
axes[1,2].set_yticklabels(df_equity['State_Territory_Tribal_Nation'])
axes[1,2].invert_yaxis()
axes[1,2].set_xlabel('Equity Ratio (Actual / Expected by Population)')
axes[1,2].set_title('Funding Equity Relative to Population')
axes[1,2].axvline(1.0, color='black', linestyle='--', alpha=0.5, label='Perfect Equity')

# Color bars: red for underfunded, green for overfunded
for i, bar in enumerate(bars):
    ratio = df_equity['Equity_Ratio'].iloc[i]
    if ratio < 0.8:
        bar.set_color('red')  # Underfunded (<80% of expected)
    elif ratio > 1.2:
        bar.set_color('green')  # Overfunded (>120% of expected)
    else:
        bar.set_color('gray')  # Fairly funded

axes[1,2].legend()

plt.tight_layout()
plt.show()
# Add political leaning data for per capita analysis
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

df_per_capita['Political_Leaning'] = df_per_capita['State_Territory_Tribal_Nation'].map(
    lambda x: political_leaning.get(str(x).strip().upper(), 'Unknown')
)

# Create political analysis for per capita funding
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# 1. Box plot by political leaning
political_order = ['Republican', 'Swing', 'Democratic']
political_colors = {'Republican': 'red', 'Swing': 'gold', 'Democratic': 'blue'}

political_data = []
for leaning in political_order:
    data = df_per_capita[df_per_capita['Political_Leaning'] == leaning]['Per_Capita_Thousands'].dropna()
    political_data.append(data)

bp = axes[0].boxplot(political_data, labels=political_order, patch_artist=True)
axes[0].set_ylabel('Per Capita Funding (Thousands USD)')
axes[0].set_title('Per Capita Funding by Political Leaning')
axes[0].grid(True, alpha=0.3)

# Color the boxes
for patch, leaning in zip(bp['boxes'], political_order):
    patch.set_facecolor(political_colors[leaning])
    patch.set_alpha(0.6)

# Add mean markers
for i, (leaning, data) in enumerate(zip(political_order, political_data), 1):
    if len(data) > 0:
        mean_val = data.mean()
        axes[0].plot(i, mean_val, 'k_', markersize=12, markeredgewidth=2)
        axes[0].text(i, mean_val, f'${mean_val:.1f}k', 
                    ha='center', va='bottom', fontweight='bold')

# 2. Scatter: Equity Ratio vs Political Leaning
# Convert political leaning to numeric for plotting
leaning_numeric = {'Republican': 0, 'Swing': 0.5, 'Democratic': 1}
df_per_capita['Political_Numeric'] = df_per_capita['Political_Leaning'].map(leaning_numeric)

scatter = axes[1].scatter(df_per_capita['Political_Numeric'], 
                         df_per_capita['Equity_Ratio'],
                         c=df_per_capita['Per_Capita_Thousands'], 
                         cmap='coolwarm', s=100, alpha=0.7, edgecolor='black')
axes[1].set_xlabel('Political Leaning (0=Rep, 0.5=Swing, 1=Dem)')
axes[1].set_ylabel('Equity Ratio (Actual/Expected)')
axes[1].set_title('Equity vs Political Leaning')
axes[1].set_xticks([0, 0.5, 1])
axes[1].set_xticklabels(['Republican', 'Swing', 'Democratic'])
cbar = plt.colorbar(scatter, ax=axes[1])
cbar.set_label('Per Capita (Thousands USD)')

# Add horizontal line at equity = 1
axes[1].axhline(1.0, color='black', linestyle='--', alpha=0.5)

# 3. Bar chart: Average Equity Ratio by Political Leaning
avg_equity_by_party = df_per_capita.groupby('Political_Leaning')['Equity_Ratio'].mean()
avg_equity_by_party = avg_equity_by_party.reindex(political_order)

bars = axes[2].bar(avg_equity_by_party.index, avg_equity_by_party.values,
                  color=[political_colors[p] for p in avg_equity_by_party.index],
                  alpha=0.7, edgecolor='black')
axes[2].set_ylabel('Average Equity Ratio')
axes[2].set_title('Average Equity by Political Leaning')
axes[2].axhline(1.0, color='black', linestyle='--', alpha=0.5, label='Perfect Equity')
axes[2].grid(True, alpha=0.3, axis='y')

# Add value labels
for bar in bars:
    height = bar.get_height()
    axes[2].text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontweight='bold')

axes[2].legend()

plt.suptitle('POLITICAL ANALYSIS: Per Capita Funding Equity', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# Calculate political statistics for per capita funding
dem_per_capita = df_per_capita[df_per_capita['Political_Leaning'] == 'Democratic']['Per_Capita_Thousands']
rep_per_capita = df_per_capita[df_per_capita['Political_Leaning'] == 'Republican']['Per_Capita_Thousands']
swing_per_capita = df_per_capita[df_per_capita['Political_Leaning'] == 'Swing']['Per_Capita_Thousands']

dem_avg_per_capita = dem_per_capita.mean()
rep_avg_per_capita = rep_per_capita.mean()
swing_avg_per_capita = swing_per_capita.mean()

political_ratio_per_capita = dem_avg_per_capita / rep_avg_per_capita

# Statistical test
if len(dem_per_capita) > 1 and len(rep_per_capita) > 1:
    t_stat_per_capita, p_value_per_capita = stats.ttest_ind(dem_per_capita, rep_per_capita, equal_var=False)

print("\n" + "="*70)
print("COMPREHENSIVE PER CAPITA EQUITY ANALYSIS - FINAL CONCLUSIONS")
print("="*70)

print(f"\n1. OVERALL EQUITY ASSESSMENT (Based on Population):")
print(f"   - Coefficient of Variation: {cv_per_capita:.1f}%")
if cv_per_capita > 30:
    print("   - ⚠️  WARNING: HIGH INEQUALITY - Funding is NOT equitable by population")
elif cv_per_capita > 20:
    print("   - ⚠️  CAUTION: MODERATE INEQUALITY - Some inequity in distribution")
else:
    print("   - ✅ ACCEPTABLE: Funding shows reasonable equity by population")

print(f"   - Gini Coefficient: {gini_per_capita:.3f}")
if gini_per_capita > 0.4:
    print("   - ⚠️  WARNING: HIGH INEQUALITY (Gini > 0.4)")
elif gini_per_capita > 0.3:
    print("   - ⚠️  CAUTION: MODERATE INEQUALITY (Gini 0.3-0.4)")
else:
    print("   - ✅ ACCEPTABLE: Reasonable equality (Gini < 0.3)")

print(f"   - Equity Range: {percent_equitable:.1f}% of states within 80-120% of expected")
if percent_equitable < 50:
    print("   - ⚠️  WARNING: Less than half of states are equitably funded")
elif percent_equitable < 70:
    print("   - ⚠️  CAUTION: Majority of states funded, but significant outliers")
else:
    print("   - ✅ GOOD: Majority of states are within equitable range")

print(f"\n2. INEQUALITY EXTREMES:")
print(f"   - Top 10% vs Bottom 10% Ratio: {inequality_ratio:.1f}:1")
if inequality_ratio > 5:
    print("   - ⚠️  SEVERE INEQUALITY: Top recipients get 5x+ more per person")
elif inequality_ratio > 3:
    print("   - ⚠️  SIGNIFICANT INEQUALITY: Top recipients get 3x+ more per person")
else:
    print("   - ✅ ACCEPTABLE: Reasonable range between top and bottom")

print(f"\n3. MOST OVERFUNDED (Relative to Population):")
for i in range(min(3, len(df_equity))):
    state = df_equity.iloc[i]
    print(f"   {i+1}. {state['State_Territory_Tribal_Nation']}: {state['Equity_Ratio']:.2f}x expected (${state['Per_Capita_Thousands']:.1f}k/person)")

print(f"\n4. MOST UNDERFUNDED (Relative to Population):")
for i in range(min(3, len(df_equity))):
    idx = -1 - i
    state = df_equity.iloc[idx]
    print(f"   {i+1}. {state['State_Territory_Tribal_Nation']}: {state['Equity_Ratio']:.2f}x expected (${state['Per_Capita_Thousands']:.1f}k/person)")

if 'Political_Leaning' in df_per_capita.columns:
    print(f"\n5. POLITICAL BIAS ANALYSIS (Per Capita):")
    print(f"   - Democratic states average: ${dem_avg_per_capita:.1f}k per person")
    print(f"   - Republican states average: ${rep_avg_per_capita:.1f}k per person")
    print(f"   - Swing states average: ${swing_avg_per_capita:.1f}k per person")
    print(f"   - Democratic/Republican ratio: {political_ratio_per_capita:.2f}")
    
    if political_ratio_per_capita > 1.2:
        print("   - ⚠️  EVIDENCE OF BIAS: Favors Democratic states")
    elif political_ratio_per_capita < 0.8:
        print("   - ⚠️  EVIDENCE OF BIAS: Favors Republican states")
    else:
        print("   - ✅ MINIMAL POLITICAL BIAS: Funding appears balanced")
    
    if 't_stat_per_capita' in locals():
        print(f"   - Statistical significance (p-value): {p_value_per_capita:.4f}")
        if p_value_per_capita < 0.05:
            print("   - ⚠️  STATISTICALLY SIGNIFICANT: Political difference is real")
        else:
            print("   - ✅ NOT STATISTICALLY SIGNIFICANT: No real political difference")

print(f"\n6. KEY TAKEAWAYS:")
if cv_per_capita > 30 or gini_per_capita > 0.4:
    print("   - ❌ IIJA funding is NOT equitable by population")
    print("   - Some states receive significantly more/less than their population share")
else:
    print("   - ✅ IIJA funding shows reasonable equity by population")
    print("   - Most states receive funding roughly proportional to population")

if 'political_ratio_per_capita' in locals() and abs(political_ratio_per_capita - 1) > 0.2:
    print("   - ⚠️  Evidence of political bias in per capita allocation")
else:
    print("   - ✅ Minimal evidence of political bias in per capita allocation")

print("\n" + "="*70)
print("RECOMMENDATIONS FOR MORE ACCURATE ANALYSIS:")
print("="*70)
print("1. Use exact Census population data (not estimates)")
print("2. Consider cost-of-living differences between states")
print("3. Analyze funding by specific infrastructure needs")
print("4. Compare with historical infrastructure investment patterns")
print("5. Consider urban vs rural population distribution")
print("6. Analyze funding formulas used in IIJA legislation")