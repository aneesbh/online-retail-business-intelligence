# Online Retail Business Intelligence & Customer Analytics

## Overview

An end-to-end Business Intelligence and Customer Analytics project that transforms online retail transaction data into actionable business insights using Python, PostgreSQL, SQL, RFM analysis, and Power BI.

## Business Objectives

- Analyze sales and order trends
- Identify top-performing products
- Analyze country-level sales performance
- Segment customers using RFM analysis
- Analyze product returns and return trends
- Build interactive dashboards for business decision-making

## Technology Stack

- Python
- Pandas
- NumPy
- PostgreSQL
- SQL
- Power BI
- DAX
- Scikit-learn
- RFM Analysis
- Git

## Project Architecture

Raw Retail Data
        ↓
Python / Pandas
        ↓
Data Cleaning & Feature Engineering
        ↓
PostgreSQL
        ↓
SQL Analytical Layer
        ↓
RFM Customer Segmentation
        ↓
Power BI
        ↓
Interactive Business Dashboard

## Data Processing

Python was used for:

- Data cleaning and validation
- Duplicate handling
- Feature engineering
- Sales calculations
- Date/time feature creation
- Exploratory data analysis
- RFM dataset preparation
- Customer segmentation

## Customer Analytics

RFM analysis was performed using:

- Recency — how recently a customer purchased
- Frequency — how frequently a customer purchased
- Monetary — how much a customer spent

Customer segments include groups such as:

- At Risk
- Potential Loyal

## PostgreSQL Analytics

PostgreSQL was used as the analytical database for structured business analysis across:

- Sales
- Products
- Customers
- Countries
- Returns

## Power BI Dashboard

The Power BI solution contains:

1. Executive Overview
2. Sales Analysis
3. Product Performance
4. Customer Segmentation
5. Monthly Trends
6. Country & Returns
7. Business Insights

### Power BI Features

- KPI dashboards
- DAX measures
- Interactive slicers
- Page navigation
- Drill-through analysis
- Report-page tooltips
- Trend analysis
- Customer segmentation
- Product and country analysis

## Project Structure

```text
online-retail-business-intelligence/
│
├── data/
│   └── powerbi/
│
├── src/
│   ├── clean_data.py
│   ├── combine_data.py
│   ├── customer_segmentation.py
│   └── sales_forecasting.py
│
├── api/
├── dashboard/
├── models/
├── notebooks/
├── tests/
├── .gitignore
└── README.md
