# agent.py
from pydantic import BaseModel
from typing import List, Dict
import uuid

class Route(BaseModel):
    id: str
    waypoints: List[Dict[str, float]]  # [{"lat":..., "lon":...}, ...]

class AgentState(BaseModel):
    id: str
    location: Dict[str, float]
    destination: Dict[str, float]
    route: Route | None = None
    neighbours: List[str] = []  # IDs of nearby agents

    def plan_route(self) -> Route:
        """
        Very naive “straight‑line” route generator. In practice this would be
        a routing algorithm (OSRM / GraphHopper / custom Dijkstra).
        """
        waypoints = [
            {"lat": self.location["lat"], "lon": self.location["lon"]},
            {"lat": self.destination["lat"], "lon": self.destination["lon"]},
        ]
        return Route(id=str(uuid.uuid4()), waypoints=waypoints)