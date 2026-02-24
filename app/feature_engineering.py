import pandas as pd

def create_features(df):

    # Convert date
    df['date'] = pd.to_datetime(df['date'])

    # Aggregate per user
    user_df = df.groupby('user_id').agg({
        'screen_time_min': 'mean',
        'launches': 'mean',
        'interactions': 'mean',
        'is_productive': 'mean',
        'youtube_views': 'mean',
        'youtube_likes': 'mean',
        'youtube_comments': 'mean'
    }).reset_index()

    # Fill missing YouTube values
    user_df = user_df.fillna(0)

    # Behavioral Features

    # Engagement Score
    user_df['EngagementScore'] = (
        user_df['screen_time_min'] * 0.5 +
        user_df['interactions'] * 0.3 +
        user_df['launches'] * 0.2
    )

    # Notification-like intensity (proxy using interactions)
    user_df['InteractionRate'] = user_df['interactions'] / (user_df['screen_time_min'] + 1)

    # Productivity Ratio
    user_df['ProductivityRatio'] = user_df['is_productive']

    return user_df