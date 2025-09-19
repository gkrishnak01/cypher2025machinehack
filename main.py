# main.py
import os
import json
import asyncio
from typing import Dict, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from starlette.websockets import WebSocketState

from dotenv import load_dotenv

# ------------------------------------------------------------------
# Imports from local modules – make sure the files exist!
# ------------------------------------------------------------------
from agent import AgentState, Route          # <-- import Route explicitly
from groq_client import optimise_routes
from simulator import run_simulation

load_dotenv()

app = FastAPI(
    title="Route AI Backend",
    description="MVP for agent‑to‑agent route optimisation",
)

# In‑memory stores
agents: Dict[str, AgentState] = {}
ws_to_agent: Dict[WebSocket, str] = {}

# ------------------------------------------------------------------
# WebSocket endpoint
# ------------------------------------------------------------------
@app.websocket("/ws/agent")
async def agent_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        # 1️⃣  Initial state from the agent
        data = await websocket.receive_text()
        init_state = AgentState.parse_raw(data)
        agents[init_state.id] = init_state
        ws_to_agent[websocket] = init_state.id
        print(f"[WS] Agent {init_state.id} connected")

        await broadcast_neighbour_update()
    except Exception as e:
        await websocket.close()
        return

    try:
        while True:
            raw = await websocket.receive_text()
            update = AgentState.parse_raw(raw)
            agents[update.id] = update
            # In a real system you could forward to Groq here
    except WebSocketDisconnect:
        agent_id = ws_to_agent.pop(websocket)
        agents.pop(agent_id, None)
        print(f"[WS] Agent {agent_id} disconnected")
        await broadcast_neighbour_update()
    except Exception as e:
        print(f"[WS] Error: {e}")
        await websocket.close()

# ------------------------------------------------------------------
# Helper: broadcast nearby agents
# ------------------------------------------------------------------
async def broadcast_neighbour_update():
    """Send every connected agent the list of nearby agents."""
    for ws, agent_id in ws_to_agent.items():
        if ws.application_state != WebSocketState.CONNECTED:
            continue
        agent = agents[agent_id]
        neighbours = [
            a.id
            for a in agents.values()
            if a.id != agent.id and distance(a.location, agent.location) < 0.05
        ]
        payload = {"type": "neighbours", "neighbours": neighbours}
        await ws.send_json(payload)

def distance(a: Dict[str, float], b: Dict[str, float]) -> float:
    return ((a["lat"] - b["lat"]) ** 2 + (a["lon"] - b["lon"]) ** 2) ** 0.5

# ------------------------------------------------------------------
# REST endpoint – batch optimisation via Groq
# ------------------------------------------------------------------
@app.post("/optimise")
async def optimise_endpoint():
    # 1️⃣  Build payload
    routes_payload = [
        {
            "agent_id": a.id,
            "waypoints": a.route.waypoints if a.route else [],
        }
        for a in agents.values()
    ]

    # 2️⃣  Call Groq
    updated_routes = optimise_routes(routes_payload)

    # 3️⃣  Update in memory & push back to the agent
    for upd in updated_routes:
        agent_id = upd["agent_id"]
        if agent_id in agents:
            route_payload = {"id": agent_id, "waypoints": upd["waypoints"]}
            agents[agent_id].route = Route(**route_payload)

            # Find the socket and send the new route
            for ws, aid in ws_to_agent.items():
                if aid == agent_id and ws.application_state == WebSocketState.CONNECTED:
                    payload = {"type": "route", "route": upd}
                    await ws.send_json(payload)

    return JSONResponse({"status": "optimised", "agents": list(agents.keys())})

# ------------------------------------------------------------------
# Demo endpoint – spin up a few mock cars
# ------------------------------------------------------------------
@app.get("/demo")
async def demo(num_cars: int = 10):
    new_agents = await run_simulation(num_cars)
    for a in new_agents:
        agents[a.id] = a
    return {"agents": [a.id for a in new_agents]}

# ------------------------------------------------------------------
# To run: uvicorn main:app --reload
# ------------------------------------------------------------------

