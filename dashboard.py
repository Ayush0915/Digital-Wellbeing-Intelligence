import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
from app.predict import predict_user, cluster_to_label


def analyze(screen_time, unlocks, notifications,
            social_time, utility_time, entertainment_time):

    # Predict cluster
    cluster = predict_user(
        screen_time,
        unlocks,
        notifications,
        social_time,
        utility_time,
        entertainment_time
    )

    behavior = cluster_to_label(cluster)

    # Risk Score (simple scaled logic)
    risk_score = min(
        100,
        int(
            (screen_time * 0.3) +
            (notifications * 0.2) +
            (unlocks * 0.2) -
            (utility_time * 0.2)
        ) // 5
    )

    # Generate Insight
    if behavior == "Distracted Users":
        insight = "High social/entertainment usage detected. Consider reducing distraction sources."
    elif behavior == "High Engagement Users":
        insight = "Heavy engagement patterns observed. Monitor burnout risk."
    else:
        insight = "Your usage pattern appears balanced and productive."

    # Create chart
    categories = ["Social", "Utility", "Entertainment"]
    values = [social_time, utility_time, entertainment_time]

    fig, ax = plt.subplots()
    ax.bar(categories, values)
    ax.set_ylabel("Minutes")
    ax.set_title("Category Usage Breakdown")

    return behavior, f"{risk_score}/100", insight, fig


with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("# 🧠 Digital Wellbeing Intelligence Dashboard")
    gr.Markdown("Analyze your daily digital behavior and receive AI-powered insights.")

    with gr.Row():
        screen_time = gr.Number(label="Total Screen Time (minutes)")
        unlocks = gr.Number(label="Total Unlock Count")
        notifications = gr.Number(label="Total Notifications")

    with gr.Row():
        social_time = gr.Number(label="Social Media Time (minutes)")
        utility_time = gr.Number(label="Utility/Productivity Time (minutes)")
        entertainment_time = gr.Number(label="Entertainment Time (minutes)")

    analyze_btn = gr.Button("Analyze Behavior")

    behavior_output = gr.Textbox(label="Behavior Type")
    risk_output = gr.Textbox(label="Digital Risk Score")
    insight_output = gr.Textbox(label="AI Insight")
    chart_output = gr.Plot(label="Usage Breakdown")

    analyze_btn.click(
        analyze,
        inputs=[
            screen_time,
            unlocks,
            notifications,
            social_time,
            utility_time,
            entertainment_time
        ],
        outputs=[
            behavior_output,
            risk_output,
            insight_output,
            chart_output
        ]
    )

demo.launch()