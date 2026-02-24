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
        "behavior": None,
        "risk_score": None,
        "chart": None
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

    cluster = predict_user(
        screen_time,
        unlocks,
        notifications,
        social,
        utility,
        entertainment
    )

    behavior = cluster_to_label(cluster)

    risk_score = min(
        100,
        int(
            (screen_time * 0.3) +
            (notifications * 0.2) +
            (unlocks * 0.2) -
            (utility * 0.2)
        ) // 5
    )

    # Create stacked bar chart
    fig = go.Figure()
    fig.add_bar(name="Social", x=["Today"], y=[social])
    fig.add_bar(name="Utility", x=["Today"], y=[utility])
    fig.add_bar(name="Entertainment", x=["Today"], y=[entertainment])
    fig.update_layout(
        barmode="stack",
        template="plotly_dark",
        title="Category Usage Breakdown"
    )

    chart_html = pio.to_html(fig, full_html=False)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "behavior": behavior,
        "risk_score": risk_score,
        "chart": chart_html
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api.main:app", host="0.0.0.0", port=port)