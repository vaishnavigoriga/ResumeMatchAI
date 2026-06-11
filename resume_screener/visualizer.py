import plotly.graph_objects as go


PALETTE = {
    "high":   "#22c55e",
    "mid":    "#f59e0b",
    "low":    "#ef4444",
    "bg":     "#1e2130",
    "grid":   "#2d3347",
    "text":   "#e2e8f0",
    "blue":   "#4f8ef7",
    "red":    "#f87171",
}

_BASE_LAYOUT = dict(
    paper_bgcolor=PALETTE["bg"],
    plot_bgcolor=PALETTE["bg"],
    font=dict(color=PALETTE["text"], family="Inter, Arial, sans-serif"),
    margin=dict(l=20, r=20, t=40, b=20),
)


def _bar_color(score: float) -> str:
    if score >= 70:
        return PALETTE["high"]
    if score >= 45:
        return PALETTE["mid"]
    return PALETTE["low"]


def plot_match_scores(ranked: list[tuple]) -> go.Figure:
    """Horizontal bar chart of all candidate match scores."""
    names  = [name for name, _ in ranked]
    scores = [data["score"] for _, data in ranked]
    colors = [_bar_color(s) for s in scores]

    fig = go.Figure(go.Bar(
        x=scores,
        y=names,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{s}%" for s in scores],
        textposition="outside",
        hovertemplate="%{y}: %{x}%<extra></extra>",
    ))

    fig.update_layout(
        **_BASE_LAYOUT,
        title=dict(text="Match Scores", font=dict(size=15)),
        xaxis=dict(range=[0, 110], gridcolor=PALETTE["grid"], ticksuffix="%"),
        yaxis=dict(autorange="reversed", gridcolor=PALETTE["grid"]),
        showlegend=False,
    )
    return fig


def plot_skill_gap(name: str, data: dict) -> go.Figure:
    """Donut chart showing matched vs missing skills for the top candidate."""
    matched_count = len(data["matched"])
    missing_count = len(data["missing"])

    fig = go.Figure(go.Pie(
        labels=["Matched Skills", "Missing Skills"],
        values=[matched_count, missing_count],
        hole=0.55,
        marker=dict(colors=[PALETTE["high"], PALETTE["red"]]),
        textinfo="label+value",
        hovertemplate="%{label}: %{value} skills<extra></extra>",
    ))

    fig.update_layout(
        **_BASE_LAYOUT,
        title=dict(text=f"Skill Gap — {name}", font=dict(size=15)),
        annotations=[dict(
            text=f"{data['score']}%",
            x=0.5, y=0.5,
            font=dict(size=22, color=PALETTE["text"]),
            showarrow=False,
        )],
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    )
    return fig
