# agent.py
"""
Agent module for Route AI.
Defines the AgentState and Route models, along with route planning logic.
"""

from __future__ import annotations
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
import uuid
import logging

logger = logging.getLogger(__name__)


class Route(BaseModel):
    """
    Represents a planned route for an agent.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    waypoints: List[Dict[str, float]]  # Each waypoint: {"lat": float, "lon": float}

    @validator('waypoints')
    def validate_waypoints(cls, v):
        if not v:
            raise ValueError("Route must have at least one waypoint")
        for point in v:
            if 'lat' not in point or 'lon' not in point:
                raise ValueError("Each waypoint must contain 'lat' and 'lon'")
        return v


class AgentState(BaseModel):
    """
    Represents the state of an agent (vehicle) in the system.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    location: Dict[str, float] = Field(..., description="Current location as {'lat': float, 'lon': float}")
    destination: Dict[str, float] = Field(..., description="Destination as {'lat': float, 'lon': float}")
    route: Optional[Route] = None
    neighbours: List[str] = Field(default_factory=list, description="IDs of nearby agents")

    @validator('location', 'destination')
    def validate_coordinates(cls, value: Dict[str, float]):
        if 'lat' not in value or 'lon' not in value:
            raise ValueError("Both 'lat' and 'lon' must be provided")
        if not isinstance(value['lat'], (float, int)) or not isinstance(value['lon'], (float, int)):
            raise ValueError("'lat' and 'lon' must be numeric")
        return value

    def plan_route(self) -> Route:
        """
        Generate a naive straight-line route from current location to destination.
        In production, replace with a proper routing algorithm (OSRM / GraphHopper / Dijkstra).
        """
        waypoints = [
            {"lat": self.location["lat"], "lon": self.location["lon"]},
            {"lat": self.destination["lat"], "lon": self.destination["lon"]},
        ]
        route = Route(waypoints=waypoints)
        logger.debug("Planned route for agent %s: %s", self.id, route)
        return route
