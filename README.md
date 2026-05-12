# Flipkart Product Data Cleaner & Analyzer

## Overview
Python script that automates cleaning and analysis of messy e-commerce product data (20,000+ records). Turns raw CSV into clean data + visualizations + actionable insights.

## Problem
Raw Flipkart data had:
- Missing/inconsistent prices
- Non-numeric ratings ("No rating available")
- Nested category strings that were unreadable
- Inconsistent brand names

## Solution
Automated pipeline that:
1. Cleans prices & calculates discount %
2. Converts ratings to numeric
3. Extracts simple categories
4. Standardizes brand names
5. Generates charts & reports

## Results
- **99.6%** of products are discounted
- **Average discount: 40.5%**
- **Highest discount found: 96.5%**
- **Most common category: Necklaces**

## Deliverables
- Cleaned CSV
- Summary statistics
- Brand analysis chart
- Discount distribution chart
- Executive summary with recommendations

## How to Run
```bash
python script1.py


<img width="1882" height="843" alt="Screenshot 2026-05-12 174307" src="https://github.com/user-attachments/assets/7048a228-da8b-4e65-8ae7-fb38e1033926" />

<img width="1876" height="791" alt="image" src="https://github.com/user-attachments/assets/a991a367-afca-4e1c-b449-a3c9687477aa" />
