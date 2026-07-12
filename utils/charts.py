"""
Chart builders using pandas (aggregation) + Plotly (visualization).

Every function returns a Plotly figure as a JSON-serializable dict, ready to
be passed into a template and rendered client-side with Plotly.js:

    fig_json = charts.weekly_hours_figure(user_id)
    return render_template("dashboard.html", weekly_fig=fig_json)

    <div id="weeklyChart"></div>
    <script>
      var fig = {{ weekly_fig | safe }};
      Plotly.newPlot('weeklyChart', fig.data, fig.layout, {responsive: true});
    </script>
"""
import json
from datetime import date

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.utils

from config import Config
from models.activity import get_activity
from models.progress import domain_hours_completed
from models.skill import get_user_skills

# Shared dark theme so every chart matches the app's design system
PLOT_BGCOLOR = "#171C3F"
PAPER_BGCOLOR = "#171C3F"
GRID_COLOR = "#2E3566"
TEXT_COLOR = "#9096C0"
TEAL = "#4FD1C5"
AMBER = "#F2A93B"

BASE_LAYOUT = dict(
    plot_bgcolor=PLOT_BGCOLOR,
    paper_bgcolor=PAPER_BGCOLOR,
    font=dict(color=TEXT_COLOR, family="Inter, sans-serif", size=12),
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor=GRID_COLOR, zeroline=False),
    yaxis=dict(gridcolor=GRID_COLOR, zeroline=False),
    showlegend=False,
)


def _to_json(fig):
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def _activity_dataframe(user_id):
    rows = get_activity(user_id)
    if not rows:
        return pd.DataFrame(columns=["date", "hours"])
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["activity_date"])
    df["hours"] = df["hours_spent"].astype(float)
    return df[["date", "hours"]]


def weekly_hours_figure(user_id, weeks=8):
    df = _activity_dataframe(user_id)
    today = pd.Timestamp(date.today())

    if df.empty:
        labels = [f"Wk {i+1}" for i in range(weeks)]
        values = [0] * weeks
    else:
        df["week"] = df["date"].dt.to_period("W-SUN").apply(lambda p: p.start_time)
        grouped = df.groupby("week")["hours"].sum()
        recent_weeks = pd.period_range(end=today, periods=weeks, freq="W-SUN")
        labels, values = [], []
        for p in recent_weeks:
            wk_start = p.start_time
            labels.append(wk_start.strftime("%b %d"))
            values.append(round(float(grouped.get(wk_start, 0.0)), 1))

    fig = go.Figure(data=[
        go.Scatter(x=labels, y=values, mode="lines+markers", line=dict(color=TEAL, width=3),
                    marker=dict(color=TEAL, size=7), fill="tozeroy",
                    fillcolor="rgba(79, 209, 197, 0.12)")
    ])
    fig.update_layout(**BASE_LAYOUT, yaxis_title="Hours")
    return _to_json(fig)


def monthly_hours_figure(user_id, months=6):
    df = _activity_dataframe(user_id)
    today_period = pd.Timestamp(date.today()).to_period("M")

    if df.empty:
        labels = [(today_period - i).strftime("%b %Y") for i in range(months - 1, -1, -1)]
        values = [0] * months
    else:
        df["month"] = df["date"].dt.to_period("M")
        grouped = df.groupby("month")["hours"].sum()
        labels, values = [], []
        for i in range(months - 1, -1, -1):
            m = today_period - i
            labels.append(m.strftime("%b %Y"))
            values.append(round(float(grouped.get(m, 0.0)), 1))

    fig = go.Figure(data=[
        go.Bar(x=labels, y=values, marker_color=AMBER, marker_line_width=0)
    ])
    fig.update_layout(**BASE_LAYOUT, yaxis_title="Hours")
    fig.update_traces(marker=dict(cornerradius=6))
    return _to_json(fig)


def skill_radar_figure(user_id):
    ratings = {s["skill_name"]: s["rating"] for s in get_user_skills(user_id)}
    labels = Config.SKILL_NAMES
    values = [ratings.get(name, 0) for name in labels]
    # close the loop for a clean radar polygon
    labels_closed = labels + [labels[0]]
    values_closed = values + [values[0]]

    fig = go.Figure(data=[
        go.Scatterpolar(r=values_closed, theta=labels_closed, fill="toself",
                          line=dict(color=AMBER), fillcolor="rgba(242, 169, 59, 0.18)")
    ])
    fig.update_layout(
        plot_bgcolor=PLOT_BGCOLOR, paper_bgcolor=PAPER_BGCOLOR,
        font=dict(color=TEXT_COLOR, family="Inter, sans-serif", size=11),
        margin=dict(l=30, r=30, t=30, b=30),
        polar=dict(
            bgcolor=PLOT_BGCOLOR,
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=GRID_COLOR, showticklabels=False),
            angularaxis=dict(gridcolor=GRID_COLOR, color=TEXT_COLOR),
        ),
        showlegend=False,
    )
    return _to_json(fig)


def domain_distribution_figure(user_id):
    rows = domain_hours_completed(user_id)
    if not rows:
        return None

    labels = [r["domain"] for r in rows]
    values = [float(r["hours"]) for r in rows]
    palette = [TEAL, AMBER, "#8A6A2C", "#2E6E68", "#9096C0", "#F2666A", "#5B6BD6", "#C9843B"]

    fig = go.Figure(data=[
        go.Pie(labels=labels, values=values, hole=0.55,
                marker=dict(colors=palette, line=dict(color=PAPER_BGCOLOR, width=2)))
    ])
    fig.update_layout(
        plot_bgcolor=PLOT_BGCOLOR, paper_bgcolor=PAPER_BGCOLOR,
        font=dict(color=TEXT_COLOR, family="Inter, sans-serif", size=12),
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.1),
    )
    return _to_json(fig)


def health_score_gauge_figure(score, tone_color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number=dict(suffix="", font=dict(color=TEXT_COLOR, size=32)),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor=TEXT_COLOR, tickfont=dict(color=TEXT_COLOR)),
            bar=dict(color=tone_color),
            bgcolor=PLOT_BGCOLOR,
            borderwidth=0,
            steps=[
                dict(range=[0, 40], color="rgba(242, 102, 106, 0.15)"),
                dict(range=[40, 70], color="rgba(242, 169, 59, 0.15)"),
                dict(range=[70, 100], color="rgba(79, 209, 197, 0.15)"),
            ],
        ),
    ))
    fig.update_layout(
        plot_bgcolor=PLOT_BGCOLOR, paper_bgcolor=PAPER_BGCOLOR,
        font=dict(color=TEXT_COLOR, family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=30, b=10), height=220,
    )
    return _to_json(fig)


def prediction_trend(user_id):
    """Simple linear-trend read on weekly hours (NumPy polyfit), used by the
    analytics page to describe whether the learner's pace is improving."""
    df = _activity_dataframe(user_id)
    if df.empty:
        return {"trend": "no_data", "avg_weekly_hours": 0}

    df["week"] = df["date"].dt.to_period("W-SUN")
    grouped = df.groupby("week")["hours"].sum()
    values = np.array(grouped.tail(6).values, dtype=float)

    avg_weekly_hours = float(values.mean()) if len(values) else 0.0
    if len(values) >= 2 and values.sum() > 0:
        x = np.arange(len(values))
        slope, _ = np.polyfit(x, values, 1)
        trend = "improving" if slope > 0.15 else ("declining" if slope < -0.15 else "steady")
    else:
        trend = "no_data"

    return {"trend": trend, "avg_weekly_hours": round(avg_weekly_hours, 1)}
