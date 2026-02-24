import joblib
import numpy as np

# Load trained model + scaler
kmeans = joblib.load("model/kmeans.pkl")
scaler = joblib.load("model/scaler.pkl")


def compute_features(screen_time, unlocks, notifications,
                     social_time, utility_time, entertainment_time):

    # Avoid division by zero
    screen_time = max(screen_time, 1)

    # Derived behavioral metrics
    distraction_ratio = (social_time + entertainment_time) / screen_time
    productivity_ratio = utility_time / screen_time
    notification_density = notifications / screen_time
    unlock_intensity = unlocks / screen_time

    # Engagement score (same logic style as training)
    engagement_score = (
        screen_time * 0.5 +
        unlocks * 0.3 +
        notifications * 0.2
    )

    return np.array([
        screen_time,
        engagement_score,
        unlock_intensity,
        productivity_ratio
    ])


def predict_user(screen_time, unlocks, notifications,
                 social_time, utility_time, entertainment_time):

    features = compute_features(
        screen_time,
        unlocks,
        notifications,
        social_time,
        utility_time,
        entertainment_time
    )

    features_scaled = scaler.transform([features])
    cluster = kmeans.predict(features_scaled)[0]

    return cluster
def cluster_to_label(cluster):

    mapping = {
        0: "Balanced Productive",
        1: "Distracted Users",
        2: "High Engagement Users"
    }

    return mapping.get(cluster, "Unknown")