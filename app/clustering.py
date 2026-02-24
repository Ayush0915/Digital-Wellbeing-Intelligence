from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns
from sklearn.metrics import silhouette_score

def perform_clustering(df):

    features = [
        'screen_time_min',
        'EngagementScore',
        'InteractionRate',
        'ProductivityRatio'
    ]

    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Elbow Method
    inertia = []
    for k in range(1, 8):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        inertia.append(kmeans.inertia_)

    plt.plot(range(1, 8), inertia, marker='o')
    plt.title("Elbow Method")
    plt.xlabel("Number of Clusters")
    plt.ylabel("Inertia")
    plt.show()

    # Final clustering (k=3)
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X_scaled)

    # 🔥 Silhouette Score
    score = silhouette_score(X_scaled, df['Cluster'])
    print("\nSilhouette Score:", round(score, 4))
    
    import joblib
    import os

    # Ensure model folder exists
    os.makedirs("model", exist_ok=True)

    # Save trained model and scaler
    joblib.dump(kmeans, "model/kmeans.pkl")
    joblib.dump(scaler, "model/scaler.pkl")

    return df


def interpret_clusters(df):

    summary = df.groupby('Cluster')[[
        'screen_time_min',
        'EngagementScore',
        'InteractionRate',
        'ProductivityRatio'
    ]].mean()

    print("\nCluster Behavioral Summary:\n")
    print(summary)

    return summary


def visualize_clusters(df):

    features = [
        'screen_time_min',
        'EngagementScore',
        'InteractionRate',
        'ProductivityRatio'
    ]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    df['PCA1'] = X_pca[:, 0]
    df['PCA2'] = X_pca[:, 1]

    plt.figure(figsize=(8,6))
    sns.scatterplot(
        data=df,
        x='PCA1',
        y='PCA2',
        hue='Cluster',
        palette='viridis'
    )
    plt.title("User Behavioral Clusters (PCA Projection)")
    plt.show()
    
    
def assign_behavior_labels(df):

    summary = df.groupby('Cluster')[[
        'screen_time_min',
        'ProductivityRatio'
    ]].mean()

    cluster_labels = {}

    for cluster in summary.index:

        screen_time = summary.loc[cluster, 'screen_time_min']
        productivity = summary.loc[cluster, 'ProductivityRatio']

        if productivity == summary['ProductivityRatio'].max():
            cluster_labels[cluster] = "Balanced Productive"

        elif productivity == summary['ProductivityRatio'].min():
            cluster_labels[cluster] = "Distracted Users"

        else:
            cluster_labels[cluster] = "High Engagement Users"

    df['BehaviorType'] = df['Cluster'].map(cluster_labels)

    return df, cluster_labels