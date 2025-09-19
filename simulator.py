# simulator.py
import networkx as nx
from random import uniform
from typing import Dict, Tuple
import uuid
import asyncio

# 5x5 grid graph as a stand‑in for city roads
BASE_MAP = nx.grid_2d_graph(5, 5, create_using=nx.DiGraph)

def node_to_latlon(node: Tuple[int, int]) -> Dict[str, float]:
    """Map grid node to fake lat/lon."""
    base_lat, base_lon = 12.9716, 77.5946   # Bangalore center
    offset = 0.02
    lat = base_lat + node[0] * offset
    lon = base_lon + node[1] * offset
    return {"lat": lat, "lon": lon}

def sample_start_end() -> Tuple[Dict, Dict]:
    start = uniform(0, 4)
    end = uniform(0, 4)
    return node_to_latlon((int(start), int(start))), node_to_latlon((int(end), int(end)))

async def run_simulation(num_cars: int = 10):
    from agent import AgentState
    agents = []

    for _ in range(num_cars):
        start, dest = sample_start_end()
        agent = AgentState(
            id=str(uuid.uuid4()),
            location=start,
            destination=dest
        )
        agent.route = agent.plan_route()
        agents.append(agent)

    return agents