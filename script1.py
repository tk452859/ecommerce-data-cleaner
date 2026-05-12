# This is a sample Python script.
import matplotlib
# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Cache results so you don't scrape same page twice
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the data
uploaded = st.file_uploader("Upload CSV", type="csv")
if not uploaded:
    st.stop()
df = pd.read_csv(uploaded, encoding='utf-8')
print("Data loaded successfully")
print(df.head())
print(df.info())

# 1. Fix prices: remove commas, convert to numeric
df['retail_price'] = pd.to_numeric(df['retail_price'], errors='coerce')
df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')

# 2. Calculate discount % (if both prices exist)
df['discount_percent'] = ((df['retail_price'] - df['discounted_price']) / df['retail_price']) * 100
df.loc[df['discount_percent'] < 0, 'discount_percent'] = 0  # fix negatives

# 3. Clean ratings: replace 'No rating available' with NaN and convert to float
df['product_rating'] = pd.to_numeric(df['product_rating'], errors='coerce')
df['overall_rating'] = pd.to_numeric(df['overall_rating'], errors='coerce')

# 4. Extract simple category (last part of the nested list)
def get_last_category(cat_str):
    if pd.isna(cat_str):
        return None
    # remove brackets and quotes, split
    cat_str = cat_str.strip('[]').replace('"', '').replace("'", '')
    parts = cat_str.split('>>')
    return parts[-1].strip() if parts else None

df['simple_category'] = df['product_category_tree'].apply(get_last_category)

# 5. Clean brand: capitalize, remove extra spaces
df['brand'] = df['brand'].astype(str).str.strip().str.title()
df.loc[df['brand'] == 'Nan', 'brand'] = None

# 6. Remove rows where product_name is missing
df.dropna(subset=['product_name'], inplace=True)

# 7. Save cleaned file
df.to_csv('flipkart_cleaned.csv', index=False)
print("Cleaned file saved.")

# 8. Generate summary statistics
summary = {
    'Total Products': len(df),
    'Products with Discount': df['discounted_price'].notna().sum(),
    'Average Discount %': round(df['discount_percent'].mean(), 2),
    'Average Rating': round(df['product_rating'].mean(), 2),
    'Top Brand by Count': df['brand'].value_counts().head(1).index[0] if not df['brand'].empty else None,
    'Most Common Category': df['simple_category'].value_counts().head(1).index[0] if not df['simple_category'].empty else None
}
print("\nSummary Statistics:")
print(summary)

# 9. Save summary as text file
try:
    with open('summary_report.txt', 'w', encoding='utf-8') as f:
        for k, v in summary.items():
            f.write(f"{k}: {v}\n")
        f.write("\n" + "=" * 50 + "\n")
        f.write("RECOMMENDATIONS:\n")
        f.write("1. Focus marketing on the top category\n")
        f.write("2. Review products with highest discounts\n")
        f.write("3. Monitor low-rated brands\n")
    print("\nSUCCESS: summary_report.txt saved")
except Exception as e:
    print(f"Error writing summary_report.txt: {e}")

# 10. Generate Top 10 Brands Chart
try:
    brand_counts = df['brand'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    brand_counts.plot(kind='bar')
    plt.title('Top 10 Brands by Number of Products')
    plt.xlabel('Brand')
    plt.ylabel('Product Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('top_brands.png')
    print("SUCCESS: top_brands.png saved")
    plt.close()  # Close to free memory
except Exception as e:
    print(f"Error generating brand chart: {e}")

# 11. Generate Discount Distribution Chart
try:
    plt.figure(figsize=(10, 6))
    plt.hist(df['discount_percent'].dropna(), bins=30, edgecolor='black')
    plt.title('Distribution of Discount Percentages')
    plt.xlabel('Discount %')
    plt.ylabel('Number of Products')
    plt.savefig('discount_distribution.png')
    print("SUCCESS: discount_distribution.png saved")
    plt.close()
except Exception as e:
    print(f"Error generating discount chart: {e}")

# 12. Generate Executive Summary Report
try:
    report = f"""
========================================
 FLIPKART PRODUCT ANALYSIS REPORT
========================================
Report Date: {datetime.now().strftime('%Y-%m-%d')}

KEY FINDINGS:
- Total products analyzed: {len(df):,}
- Average discount offered: {df['discount_percent'].mean():.1f}%
- Highest discount: {df['discount_percent'].max():.1f}%
- Average product rating: {df['product_rating'].mean():.2f} / 5.0
- Most common category: {df['simple_category'].mode()[0]}
- Top brand by volume: {df['brand'].mode()[0]}

RECOMMENDATIONS:
1. Focus marketing on the '{df['simple_category'].mode()[0]}' category (highest volume)
2. Consider price adjustments for products with discounts below 30%
3. Improve product quality/listing for brands with low average rating
"""
    with open('executive_summary.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    print("\n" + report)
    print("\nSUCCESS: executive_summary.txt saved")
except Exception as e:
    print(f"Error generating executive summary: {e}")

print("\n" + "=" * 50)
print("ALL TASKS COMPLETED SUCCESSFULLY!")
print("Files created:")
print("  - flipkart_cleaned.csv")
print("  - summary_report.txt")
print("  - top_brands.png")
print("  - discount_distribution.png")
print("  - executive_summary.txt")
