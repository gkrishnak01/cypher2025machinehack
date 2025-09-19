# groq_client.py
import os
import json
import logging
from groq import Groq
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL")

client = Groq(api_key=API_KEY)

def optimise_routes(routes: List[Dict]) -> List[Dict]:
    """
    Send the list of routes to Groq and parse the response.

    Expected input format (per route):
    {
        "agent_id": "abc",
        "waypoints": [{"lat": ..., "lon": ...}, ...]
    }

    Expected Groq reply (very simple):
    {
        "routes": [
            {"agent_id": "abc", "waypoints": [...]},
            ...
        ]
    }
    """
    prompt = (
        "You are a traffic optimisation AI. "
        "Given the following planned routes for several vehicles, "
        "detect congestion and propose alternate routes that minimise "
        "total travel time. Return the routes in the same JSON format.\n\n"
        f"{json.dumps(routes, indent=2)}"
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a traffic AI."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=2048,
        )
        raw = response.choices[0].message.content
        data = json.loads(raw)
        return data.get("routes", [])
    except Exception as e:
        logging.error(f"Groq inference failed: {e}")
        return routes  # fallback: no optimisation