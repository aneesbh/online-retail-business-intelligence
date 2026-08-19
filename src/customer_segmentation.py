import pandas as pd

# Load customer RFM data
rfm = pd.read_csv("data/customer_rfm.csv")

print("RFM data loaded successfully!")
print("Customers:", len(rfm))
print("Columns:", rfm.columns.tolist())

print("\nFirst 5 customers:")
print(rfm.head())

print("\nMissing values:")
print(rfm[["Recency", "Frequency", "Monetary"]].isna().sum())

print("\nNegative values:")
print("Negative Recency:", (rfm["Recency"] < 0).sum())
print("Negative Frequency:", (rfm["Frequency"] < 0).sum())
print("Negative Monetary:", (rfm["Monetary"] < 0).sum())

print("\nRFM statistics:")
print(
    rfm[
        ["Recency", "Frequency", "Monetary"]
    ].describe()
)

from sklearn.preprocessing import StandardScaler

# Select features for clustering
features = rfm[
    ["Recency", "Frequency", "Monetary"]
].copy()

# Scale the features
scaler = StandardScaler()

rfm_scaled = scaler.fit_transform(features)

print("\nRFM features scaled successfully!")

print("Scaled data shape:", rfm_scaled.shape)

print("\nFirst 5 scaled rows:")
print(rfm_scaled[:5])

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

inertia = []

# Test K values from 2 to 10
for k in range(2, 11):

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    kmeans.fit(rfm_scaled)

    inertia.append(kmeans.inertia_)

print("\nElbow Method results:")

for k, value in zip(range(2, 11), inertia):
    print(f"K={k}: Inertia={value:.2f}")

# Plot the Elbow curve
plt.figure(figsize=(8, 5))

plt.plot(
    range(2, 11),
    inertia,
    marker="o"
)

plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.title("Elbow Method for Customer Segmentation")

plt.xticks(range(2, 11))
plt.grid(True)

plt.show()

from sklearn.metrics import silhouette_score

print("\nSilhouette Scores:")

for k in range(2, 7):

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(rfm_scaled)

    score = silhouette_score(
        rfm_scaled,
        labels
    )

    print(f"K={k}: Silhouette Score={score:.4f}")
    from sklearn.metrics import silhouette_score

print("\nSilhouette Scores:")

for k in range(2, 7):

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(rfm_scaled)

    score = silhouette_score(
        rfm_scaled,
        labels
    )

    print(f"K={k}: Silhouette Score={score:.4f}")
    
    
from sklearn.metrics import silhouette_score

silhouette_scores = {}

print("\nSilhouette Scores:")

for k in range(2, 7):

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(rfm_scaled)

    score = silhouette_score(
        rfm_scaled,
        labels
    )

    silhouette_scores[k] = score

    print(f"K={k}: Silhouette Score={score:.4f}")

# Select K with the highest score
best_k = max(
    silhouette_scores,
    key=silhouette_scores.get
)

print("\nBest K:", best_k)
print(
    "Best Silhouette Score:",
    round(silhouette_scores[best_k], 4)
)
final_kmeans = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=10
)

# Create customer segments
rfm["Segment"] = final_kmeans.fit_predict(rfm_scaled)

print("\nFinal K-Means model trained!")
print("Number of segments:", best_k)

print("\nCustomers in each segment:")
print(rfm["Segment"].value_counts().sort_index())

segment_summary = rfm.groupby("Segment").agg(
    Customers=("Customer ID", "count"),
    AvgRecency=("Recency", "mean"),
    AvgFrequency=("Frequency", "mean"),
    AvgMonetary=("Monetary", "mean")
).reset_index()

print("\nSegment Summary:")
print(segment_summary.round(2).to_string(index=False))

# Rank segments based on their average monetary value
segment_summary["ValueRank"] = segment_summary["AvgMonetary"].rank(
    method="first",
    ascending=False
)

def assign_segment(row):
    if row["AvgMonetary"] >= segment_summary["AvgMonetary"].quantile(0.75):
        return "VIP Customers"

    elif row["AvgFrequency"] >= segment_summary["AvgFrequency"].median():
        return "Loyal Customers"

    elif row["AvgRecency"] >= segment_summary["AvgRecency"].median():
        return "At-Risk Customers"

    else:
        return "Potential Customers"


segment_summary["SegmentName"] = segment_summary.apply(
    assign_segment,
    axis=1
)

print("\nBusiness Segment Labels:")
print(
    segment_summary[
        [
            "Segment",
            "Customers",
            "AvgRecency",
            "AvgFrequency",
            "AvgMonetary",
            "SegmentName"
        ]
    ].round(2).to_string(index=False)
)
output_file = "data/customer_segments.csv"

rfm.to_csv(
    output_file,
    index=False
)

print("\nCustomer segmentation dataset saved!")
print("File:", output_file)

output_file = "data/customer_segments.csv"

rfm.to_csv(
    output_file,
    index=False
)

print("\nCustomer segmentation dataset saved!")
print("File:", output_file)

segment_mapping = {
    0: "At Risk",
    1: "Potential Loyal",
    2: "New Customers",
    3: "Loyal Customers",
    4: "Champions"
}

rfm["SegmentName"] = rfm["Segment"].map(segment_mapping)

segment_mapping = {
    0: "At Risk",
    1: "Potential Loyal",
    2: "New Customers",
    3: "Loyal Customers",
    4: "Champions"
}

rfm["SegmentName"] = rfm["Segment"].map(segment_mapping)