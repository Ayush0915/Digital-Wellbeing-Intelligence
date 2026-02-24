from app.data_loader import load_data
from app.feature_engineering import create_features
from app.clustering import perform_clustering, interpret_clusters
from app.clustering import assign_behavior_labels

def main():

    path = "data/wellbeing_dataset.csv"

    # 1️⃣ Load raw data
    df = load_data(path)

    # 2️⃣ Aggregate + feature engineering
    user_df = create_features(df)

    # 3️⃣ Perform clustering
    clustered_df = perform_clustering(user_df)

    # 4️⃣ Interpret clusters
    summary = interpret_clusters(clustered_df)
    
    clustered_df, labels = assign_behavior_labels(clustered_df)

    print("\n==============================")
    print("DW - Digital Wellbeing Results")
    print("==============================\n")

    print("Cluster Behavioral Summary:\n")
    print(summary)

    print("\nAssigned Behavioral Labels:\n")
    for cluster, label in labels.items():
        print(f"Cluster {cluster}: {label}")

    print("\nSample User Classification:\n")
    print(clustered_df[['user_id', 'BehaviorType']].head())
    
    print("\nUser Distribution per Behavior Type:\n")
    print(clustered_df['BehaviorType'].value_counts())


from app.predict import predict_user, cluster_to_label

cluster = predict_user(
    screen_time=300,
    unlocks=80,
    notifications=120,
    social_time=150,
    utility_time=60,
    entertainment_time=90
)

print("Predicted Behavior:", cluster_to_label(cluster))

if __name__ == "__main__":
    main()