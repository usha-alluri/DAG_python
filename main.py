from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import random
import networkx as nx

from utils.plot_util import generate_plotly_html
from utils.html_header import overall_check
from fastapi.responses import HTMLResponse
from fastapi import UploadFile, File
import json


app = FastAPI(title="Modern DAG Health Checker")


class Node(BaseModel):
    id: str
    label: Optional[str] = None


class GraphInput(BaseModel):
    nodes: List[Node]
    edges: list[list[str]]


# Simulated async health check
async def check_node_health(node: str):
    await asyncio.sleep(0.2)  # simulate latency
    healthy = random.choice([True, True, True, False])  # 75% chance OK
    return node, healthy


def build_graph(data: GraphInput):
    G = nx.DiGraph()
    G.add_nodes_from([n.id for n in data.nodes])
    G.add_edges_from(data.edges)
    return G


# POST endpoint to check health
@app.post("/check/html", response_class=HTMLResponse)
async def check_health_html(graph: GraphInput):
    G = build_graph(graph)
    roots = [n for n in G.nodes if G.in_degree(n) == 0]

    # BFS traversal
    visited, queue = [], list(roots)
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
            queue.extend(G.successors(node))

    # Async health checks
    tasks = [check_node_health(n) for n in visited]
    results_list = await asyncio.gather(*tasks)
    results = {n: ok for n, ok in results_list}

    # Summary table (HTML)
    fig = generate_plotly_html(G, results)
    return overall_check(results, fig)


# Bonus: Optional GET demo endpoint

@app.get("/demo")
async def demo_report():
    sample = {
        "nodes": [
            {"id": "step1",  "label": "Step 1"},
            {"id": "step2",  "label": "Step 2"},
            {"id": "step3",  "label": "Step 3"},
            {"id": "step4",  "label": "Step 4"},
            {"id": "step5",  "label": "Step 5"},
            {"id": "step6",  "label": "Step 6"},
            {"id": "step7",  "label": "Step 7"},
            {"id": "step8",  "label": "Step 8"},
            {"id": "step9",  "label": "Step 9"},
            {"id": "step10", "label": "Step 10"},
            {"id": "step11", "label": "Step 11"}
        ],
        "edges": [
            ["step1", "step2"],
            ["step2", "step3"],
            ["step2", "step4"],
            ["step3", "step5"],
            ["step3", "step7"],
            ["step5", "step6"],
            ["step7", "step8"],
            ["step6", "step10"],
            ["step8", "step10"],
            ["step4", "step9"],
            ["step9", "step10"],
            ["step10", "step11"]
        ]
    }
    # Reuse the same logic for health checking and report generation
    return await check_health_html(GraphInput(**sample))


# Optional for now
@app.post("/upload", response_class=HTMLResponse)
async def upload_json(file: UploadFile = File(...)):
    """
    Accepts a JSON file upload containing nodes and edges,
    parses it into a DAG, and generates the same health report.
    """
    # Read and decode the uploaded file
    content = await file.read()
    try:
        data = json.loads(content)
        graph_input = GraphInput(**data)
    except Exception as e:
        return HTMLResponse(
            content=f"<h3 style='color:red;'>Invalid JSON file: {e}</h3>",
            status_code=400
        )

    # Reuse existing logic to check health and generate the report
    return await check_health_html(graph_input)
