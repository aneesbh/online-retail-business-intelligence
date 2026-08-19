import pandas as pd

# 1. Load the combined dataset

df = pd.read_csv("data/online_retail_combined.csv")

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# 2. Convert InvoiceDate to datetime

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("InvoiceDate converted successfully!")
print(df["InvoiceDate"].dtype)


# 3. Remove exact duplicate rows

before = len(df)

df = df.drop_duplicates()

after = len(df)

print("Duplicate rows removed:", before - after)
print("Rows after removing duplicates:", after)


# 4. Check unusual prices

print("Zero-price rows:", (df["Price"] == 0).sum())
print("Negative-price rows:", (df["Price"] < 0).sum())

print("\nNegative-price examples:")

print(
    df[df["Price"] < 0][
        [
            "Invoice",
            "StockCode",
            "Description",
            "Quantity",
            "Price"
        ]
    ].to_string(index=False)
)


# 5. Remove invalid negative-price accounting adjustments

before = len(df)

df = df[df["Price"] >= 0]

after = len(df)

print("Negative-price rows removed:", before - after)
print("Rows after price validation:", after)


# 6. Inspect zero-price transactions

zero_price = df[df["Price"] == 0]

print("Zero-price rows:", len(zero_price))

print("\nMost common zero-price descriptions:")

print(
    zero_price["Description"]
    .value_counts()
    .head(20)
)


# 7. Remove zero-price transactions

before = len(df)

df = df[df["Price"] > 0]

after = len(df)

print("Zero-price rows removed:", before - after)
print(
    "Rows after removing zero-price transactions:",
    after
)


# 8. Check missing Customer IDs

missing_customer = df["Customer ID"].isna().sum()

print(
    "Missing Customer IDs:",
    missing_customer
)

print(
    "Customer ID available:",
    len(df) - missing_customer
)


# 9. Check missing product descriptions

missing_description = df["Description"].isna().sum()

print(
    "Missing Descriptions:",
    missing_description
)

print(
    "Descriptions available:",
    len(df) - missing_description
)


# 10. Calculate SalesAmount

df["SalesAmount"] = (
    df["Quantity"] * df["Price"]
)

print("SalesAmount created successfully!")

print(
    df[
        [
            "Quantity",
            "Price",
            "SalesAmount"
        ]
    ].head()
)


# 11. Classify transactions

df["TransactionType"] = df["Quantity"].apply(
    lambda x: "Return" if x < 0 else "Sale"
)

print("TransactionType created successfully!")

print(
    df["TransactionType"].value_counts()
)


# 12. Create time-based columns

df["Year"] = df["InvoiceDate"].dt.year

df["Month"] = df["InvoiceDate"].dt.month

df["MonthName"] = (
    df["InvoiceDate"].dt.month_name()
)

df["Quarter"] = (
    df["InvoiceDate"].dt.quarter
)

df["YearMonth"] = (
    df["InvoiceDate"]
    .dt.to_period("M")
    .astype(str)
)

print("Time columns created successfully!")

print(
    df[
        [
            "InvoiceDate",
            "Year",
            "Month",
            "MonthName",
            "Quarter",
            "YearMonth"
        ]
    ].head()
)


# 13. Create customer dataset

customer_df = (
    df.dropna(
        subset=["Customer ID"]
    ).copy()
)

# Convert Customer ID to integer
customer_df["Customer ID"] = (
    customer_df["Customer ID"].astype(int)
)

print("\nCustomer dataset created!")

print(
    "Customer transaction rows:",
    len(customer_df)
)

print(
    "Unique customers:",
    customer_df["Customer ID"].nunique()
)


# 14. Create RFM dataset

reference_date = (
    customer_df["InvoiceDate"].max()
)

rfm = (
    customer_df
    .groupby("Customer ID")
    .agg(
        Recency=(
            "InvoiceDate",
            lambda x: (
                reference_date - x.max()
            ).days
        ),
        Frequency=(
            "Invoice",
            "nunique"
        ),
        Monetary=(
            "SalesAmount",
            "sum"
        )
    )
    .reset_index()
)

print("\nRFM dataset created!")

print(
    "Customers:",
    len(rfm)
)

print("\nRFM sample:")

print(
    rfm.head()
)


# 15. RFM quality checks

print("\nRFM data types:")

print(
    rfm.dtypes
)

print("\nMissing values:")

print(
    rfm.isna().sum()
)

print("\nRFM statistics:")

print(
    rfm[
        [
            "Recency",
            "Frequency",
            "Monetary"
        ]
    ].describe()
)


# 16. Save RFM dataset

rfm_file = "data/customer_rfm.csv"

rfm.to_csv(
    rfm_file,
    index=False
)

print(
    "\nRFM dataset saved successfully!"
)

print(
    "File:",
    rfm_file
)


# 17. Fix Customer ID before saving

# Pandas originally reads Customer ID as float
# because missing values exist.
# Convert it to nullable integer so values like
# 13085.0 become 13085 while missing values remain blank.

df["Customer ID"] = (
    df["Customer ID"].astype("Int64")
)


# 18. Save cleaned transaction dataset

cleaned_file = (
    "data/online_retail_cleaned.csv"
)

df.to_csv(
    cleaned_file,
    index=False
)

print(
    "\nCleaned transaction dataset saved successfully!"
)

print(
    "File:",
    cleaned_file
)
