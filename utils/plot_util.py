import plotly.graph_objects as go
import networkx as nx


def generate_plotly_html(G, results):
    # Layout positions for nodes
    pos = nx.spring_layout(G, seed=42, k=0.25)
    x_nodes = [pos[n][0] for n in G.nodes]
    y_nodes = [pos[n][1] for n in G.nodes]

    # Edge coordinates
    edge_x, edge_y = [], []
    for src, dst in G.edges():
        edge_x += [pos[src][0], pos[dst][0], None]
        edge_y += [pos[src][1], pos[dst][1], None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=1, color='gray'),
        hoverinfo='none'
    )

    colors = ["green" if results[n] else "red" for n in G.nodes]
    node_trace = go.Scatter(
        x=x_nodes, y=y_nodes,
        mode='markers+text',
        text=list(G.nodes),
        textposition="bottom center",
        marker=dict(color=colors, size=30, line=dict(width=2, color='black')),
        hovertemplate='Node: %{text}<extra></extra>'
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="DAG Health Visualization",
        title_x=0.5,
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig
