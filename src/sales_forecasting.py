import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.ensemble import RandomForestRegressor


# ============================================================
# 1. Load raw combined data
# ============================================================

input_file = "data/online_retail_combined.csv"

df = pd.read_csv(input_file)

print("Original rows:", len(df))


# ============================================================
# 2. Clean the data
# ============================================================

# Convert InvoiceDate
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Remove exact duplicates
df = df.drop_duplicates()

# Remove negative-price accounting adjustments
df = df[df["Price"] >= 0]

# Remove zero-price transactions
df = df[df["Price"] > 0]

print("Rows after cleaning:", len(df))


# ============================================================
# 3. Calculate SalesAmount
# ============================================================

df["SalesAmount"] = df["Quantity"] * df["Price"]


# ============================================================
# 4. Create monthly sales
# ============================================================

df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

monthly_sales = (
    df.groupby("YearMonth")["SalesAmount"]
    .sum()
    .reset_index()
)

monthly_sales["YearMonth"] = (
    monthly_sales["YearMonth"].dt.to_timestamp()
)

monthly_sales = monthly_sales.sort_values("YearMonth")


print("\nMonthly sales created!")
print("Number of months:", len(monthly_sales))

print("\nFirst 10 months:")
print(monthly_sales.head(10).to_string(index=False))


# ============================================================
# 5. Save monthly sales dataset
# ============================================================

monthly_file = "data/monthly_sales.csv"

monthly_sales.to_csv(
    monthly_file,
    index=False
)

print("\nMonthly sales saved to:", monthly_file)


# ============================================================
# 6. Visualize monthly sales
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["YearMonth"],
    monthly_sales["SalesAmount"],
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Sales Amount")
plt.title("Monthly Sales Trend")

plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.show()


# ============================================================
# 7. Create time-series features
# ============================================================

monthly_sales["Year"] = monthly_sales["YearMonth"].dt.year

monthly_sales["Month"] = monthly_sales["YearMonth"].dt.month

monthly_sales["MonthIndex"] = np.arange(
    len(monthly_sales)
)

# Lag features
monthly_sales["Lag1"] = (
    monthly_sales["SalesAmount"].shift(1)
)

monthly_sales["Lag2"] = (
    monthly_sales["SalesAmount"].shift(2)
)

monthly_sales["Lag3"] = (
    monthly_sales["SalesAmount"].shift(3)
)


# ============================================================
# 8. Remove rows created by lagging
# ============================================================

model_data = monthly_sales.dropna().copy()


# ============================================================
# 9. Train/Test split
# ============================================================

# Use the last 6 months as test data
test_months = 6

train = model_data.iloc[:-test_months].copy()

test = model_data.iloc[-test_months:].copy()


print("\nTraining rows:", len(train))
print("Testing rows:", len(test))


# ============================================================
# 10. Select features
# ============================================================

features = [
    "Year",
    "Month",
    "MonthIndex",
    "Lag1",
    "Lag2",
    "Lag3"
]

X_train = train[features]

y_train = train["SalesAmount"]

X_test = test[features]

y_test = test["SalesAmount"]


# ============================================================
# 11. Train Random Forest forecasting model
# ============================================================

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    max_depth=8
)

model.fit(
    X_train,
    y_train
)

print("\nRandom Forest forecasting model trained!")


# ============================================================
# 12. Predict test period
# ============================================================

predictions = model.predict(X_test)

test["PredictedSales"] = predictions


# ============================================================
# 13. Evaluate model
# ============================================================

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)

print("\nModel Performance")
print("-------------------------")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))


# ============================================================
# 14. Display actual vs predicted
# ============================================================

print("\nActual vs Predicted:")

print(
    test[
        [
            "YearMonth",
            "SalesAmount",
            "PredictedSales"
        ]
    ].round(2).to_string(index=False)
)


# ============================================================
# 15. Plot actual vs predicted
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    test["YearMonth"],
    test["SalesAmount"],
    marker="o",
    label="Actual Sales"
)

plt.plot(
    test["YearMonth"],
    test["PredictedSales"],
    marker="o",
    label="Predicted Sales"
)

plt.xlabel("Month")
plt.ylabel("Sales Amount")

plt.title(
    "Actual vs Predicted Monthly Sales"
)

plt.xticks(rotation=45)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# 16. Save predictions
# ============================================================

prediction_file = "data/sales_forecast_predictions.csv"

test[
    [
        "YearMonth",
        "SalesAmount",
        "PredictedSales"
    ]
].to_csv(
    prediction_file,
    index=False
)

print(
    "\nForecast predictions saved to:",
    prediction_file
)


# ============================================================
# 17. Feature importance
# ============================================================

importance = pd.DataFrame(
    {
        "Feature": features,
        "Importance": model.feature_importances_
    }
).sort_values(
    "Importance",
    ascending=False
)

print("\nFeature Importance:")
print(
    importance.round(4).to_string(index=False)
)