import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io

st.set_page_config(page_title="Flipkart Analyzer", page_icon="🛒", layout="wide")
st.title("🛒 Flipkart Product Analyzer")
st.divider()

uploaded = st.file_uploader("Upload Flipkart CSV file", type=["csv"])

if not uploaded:
    st.info("Please upload your Flipkart CSV file to begin.")
    st.stop()

df = pd.read_csv(uploaded, encoding='utf-8')

df['retail_price'] = pd.to_numeric(df['retail_price'], errors='coerce')
df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')
df['product_rating'] = pd.to_numeric(df['product_rating'], errors='coerce')
df['discount_percent'] = ((df['retail_price'] - df['discounted_price']) / df['retail_price']) * 100
df.loc[df['discount_percent'] < 0, 'discount_percent'] = 0

def get_last_category(cat_str):
    if pd.isna(cat_str): return None
    parts = cat_str.strip('[]').replace('"','').replace("'",'').split('>>')
    return parts[-1].strip() if parts else None

df['simple_category'] = df['product_category_tree'].apply(get_last_category)
df['brand'] = df['brand'].astype(str).str.strip().str.title()
df.loc[df['brand'] == 'Nan', 'brand'] = None
df.dropna(subset=['product_name'], inplace=True)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Products", f"{len(df):,}")
k2.metric("Avg Discount", f"{df['discount_percent'].mean():.1f}%")
k3.metric("Max Discount", f"{df['discount_percent'].max():.1f}%")
k4.metric("Avg Rating", f"{df['product_rating'].mean():.2f} ★")

st.divider()

c1, c2 = st.columns(2)

with c1:
    fig, ax = plt.subplots(figsize=(7, 4))
    df['brand'].value_counts().head(10).plot(kind='barh', ax=ax, color='#2874f0')
    ax.set_title('Top 10 Brands')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with c2:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(df['discount_percent'].dropna(), bins=30, color='#fb641b', edgecolor='white')
    ax.set_title('Discount % Distribution')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.divider()
st.subheader("🔍 Explore Products")

cats = ['All'] + sorted(df['simple_category'].dropna().unique().tolist())
sel_cat = st.selectbox("Filter by Category", cats)
min_disc = st.slider("Minimum Discount %", 0, 100, 0)

filtered = df.copy()
if sel_cat != 'All':
    filtered = filtered[filtered['simple_category'] == sel_cat]
filtered = filtered[filtered['discount_percent'] >= min_disc]

st.dataframe(filtered[['product_name','brand','simple_category',
    'retail_price','discounted_price','discount_percent','product_rating']].head(200),
    use_container_width=True)

csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download CSV", csv, "filtered.csv", "text/csv")
