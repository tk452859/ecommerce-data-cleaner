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
