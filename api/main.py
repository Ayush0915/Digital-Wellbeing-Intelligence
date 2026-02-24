from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.predict import predict_user, cluster_to_label
import plotly.graph_objects as go
import plotly.io as pio
import os
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="api/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "behavior": None
    })


@app.post("/analyze", response_class=HTMLResponse)
def analyze(
    request: Request,
    screen_time: float = Form(...),
    unlocks: float = Form(...),
    notifications: float = Form(...),
    social: float = Form(...),
    utility: float = Form(...),
    entertainment: float = Form(...)
):

    # -------------------------
    # ML Prediction
    # -------------------------
    cluster = predict_user(
        screen_time,
        unlocks,
        notifications,
        social,
        utility,
        entertainment
    )

    behavior = cluster_to_label(cluster)
    # -------------------------
    # Behavior Badge Mapping
    # -------------------------

    if behavior == "Balanced Productive":
        badge_label = "🟢 Productive"
        badge_color = "#34c759"  # Apple green
    elif behavior == "Distracted Users":
        badge_label = "🔴 Distracted"
        badge_color = "#ff3b30"  # Apple red
    else:
        badge_label = "🟡 Balanced"
        badge_color = "#ffcc00"  # Apple yellow

    # -------------------------
    # Productivity Score
    # -------------------------
    productivity_score = int(
        (utility * 1.5) /
        (screen_time + notifications * 0.3) * 100
    )
    productivity_score = max(0, min(productivity_score, 100))

    # -------------------------
    # Risk Score
    # -------------------------
    risk_score = min(
        100,
        int(
            (screen_time * 0.3) +
            (notifications * 0.2) +
            (unlocks * 0.2) -
            (utility * 0.2)
        ) // 5
    )

    # -------------------------
    # Productivity Gauge
    # -------------------------
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=productivity_score,
        title={"text": "Productivity Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "steps": [
                {"range": [0, 40], "color": "#ff4d4d"},
                {"range": [40, 70], "color": "#ffd633"},
                {"range": [70, 100], "color": "#4CAF50"}
            ],
        }
    ))
    gauge.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
    gauge_chart = pio.to_html(gauge, full_html=False)

    # -------------------------
    # Radar Chart
    # -------------------------
    radar = go.Figure()
    radar.add_trace(go.Scatterpolar(
        r=[
            screen_time / 10,
            unlocks,
            notifications,
            social,
            utility,
            entertainment
        ],
        theta=[
            "Screen Time",
            "Unlocks",
            "Notifications",
            "Social",
            "Utility",
            "Entertainment"
        ],
        fill='toself'
    ))
    radar.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
    radar_chart = pio.to_html(radar, full_html=False)


    # -------------------------
    # Advanced AI Insight Engine
    # -------------------------
    social_ratio = social / screen_time if screen_time else 0
    notification_density = notifications / screen_time if screen_time else 0
    unlock_intensity = unlocks / screen_time if screen_time else 0

    insight_parts = []

    # Behavioral Diagnosis
    if social_ratio > 0.45:
        insight_parts.append("Your social media usage dominates daily activity, indicating potential distraction cycles.")

    if notification_density > 0.4:
        insight_parts.append("High notification frequency suggests reactive engagement patterns.")

    if unlock_intensity > 0.25:
        insight_parts.append("Frequent device unlocks indicate fragmented attention span.")

    if productivity_score > 70:
        insight_parts.append("Strong productivity indicators detected. Utility usage supports focused digital habits.")

    # Optimization Suggestions
    if productivity_score < 50:
        reduction = int(social * 0.3)
        insight_parts.append(f"Reducing social usage by approximately {reduction} minutes daily could significantly improve your productivity score.")

    if notifications > 80:
        insight_parts.append("Consider enabling notification batching or focus mode to reduce cognitive interruptions.")

    if not insight_parts:
        insight_parts.append("Your digital behavior appears stable with balanced usage patterns.")

    insight = insight_parts

    return templates.TemplateResponse("index.html", {
        "request": request,
        "behavior": behavior,
        "badge_label": badge_label,
        "badge_color": badge_color,
        "risk_score": risk_score,
        "productivity_score": productivity_score,
        "total_time": screen_time,
        "gauge_chart": gauge_chart,
        "radar_chart": radar_chart,
        "insight": insight
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api.main:app", host="0.0.0.0", port=port)