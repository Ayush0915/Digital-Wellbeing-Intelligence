import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import requests

# Create Dash App
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": "#0f1117",
        "color": "white",
        "padding": "30px",
        "fontFamily": "Arial"
    },
    children=[

        html.H1("🧠 Digital Wellbeing Intelligence Dashboard"),

        html.Div([
            dcc.Input(id="screen_time", type="number", placeholder="Screen Time (min)"),
            dcc.Input(id="unlocks", type="number", placeholder="Unlocks"),
            dcc.Input(id="notifications", type="number", placeholder="Notifications"),
            dcc.Input(id="social", type="number", placeholder="Social Time"),
            dcc.Input(id="utility", type="number", placeholder="Utility Time"),
            dcc.Input(id="entertainment", type="number", placeholder="Entertainment Time"),
            html.Button("Analyze", id="analyze_btn")
        ], style={"display": "flex", "gap": "10px", "flexWrap": "wrap"}),

        html.Br(),

        html.H2(id="behavior_output"),
        html.H3(id="risk_output"),

        html.Br(),

        dcc.Graph(id="usage_chart"),
        dcc.Graph(id="risk_gauge")
    ]
)


@app.callback(
    [
        Output("behavior_output", "children"),
        Output("risk_output", "children"),
        Output("usage_chart", "figure"),
        Output("risk_gauge", "figure"),
    ],
    Input("analyze_btn", "n_clicks"),
    [
        State("screen_time", "value"),
        State("unlocks", "value"),
        State("notifications", "value"),
        State("social", "value"),
        State("utility", "value"),
        State("entertainment", "value"),
    ],
)
def analyze(n, screen_time, unlocks, notifications, social, utility, entertainment):

    if not n:
        return "", "", go.Figure(), go.Figure()

    # Call FastAPI backend
    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json={
            "screen_time": screen_time,
            "unlocks": unlocks,
            "notifications": notifications,
            "social": social,
            "utility": utility,
            "entertainment": entertainment,
        },
    )

    data = response.json()

    behavior_text = f"Behavior: {data['behavior']}"
    risk_text = f"Risk Score: {data['risk_score']}/100"

    # Stacked Category Chart
    fig_bar = go.Figure()
    fig_bar.add_bar(name="Social", x=["Today"], y=[social])
    fig_bar.add_bar(name="Utility", x=["Today"], y=[utility])
    fig_bar.add_bar(name="Entertainment", x=["Today"], y=[entertainment])
    fig_bar.update_layout(
        barmode="stack",
        template="plotly_dark",
        title="Category Usage Breakdown",
    )

    # Risk Gauge
    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=data["risk_score"],
            title={"text": "Digital Risk Level"},
            gauge={"axis": {"range": [0, 100]}},
        )
    )
    fig_gauge.update_layout(template="plotly_dark")

    return behavior_text, risk_text, fig_bar, fig_gauge


if __name__ == "__main__":
    app.run(debug=True)