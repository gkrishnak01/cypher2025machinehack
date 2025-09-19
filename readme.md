# 🚦 Route AI – Traffic Optimisation for Bangalore using Groq API

> *"Bangalore loses **~600 million person-hours annually** in traffic congestion. What if AI agents inside every car could talk to each other, coordinate, and reduce this chaos?"*  

Route AI is a **real-time, AI-driven traffic optimisation system** built specifically for Bangalore.  
It leverages **Groq API** for ultra-fast inference, enabling **cars (agents)** to share routes, detect congestion, and dynamically optimise travel paths – *together, as a swarm of intelligent vehicles.*

---

## 🌍 Why Bangalore?
- **Most congested city in the world** (TomTom Traffic Index 2022).  
- **Commuters spend 2x–3x more time on the road** compared to global averages.  
- **Environmental impact**: wasted fuel & CO₂ emissions.  
- **Economic loss**: billions lost yearly due to inefficiency.

⚡ *Solving Bangalore’s traffic problem means saving lives, money, and the environment. Route AI is a step toward that future.*

---

## 🤖 How It Works
Each **car = an agent** with its own AI-powered brain.  

1. **Agent State**  
   - Knows its **current location**, **destination**, and **route**.  
   - Detects **nearby agents** over WebSocket.  

2. **Route Planning**  
   - Initially generates a **naïve straight-line route**.  

3. **Groq-powered Optimisation**  
   - Periodically, all agents send their planned routes to Groq.  
   - Groq AI detects **congestion patterns** and returns **optimised alternative routes**.  
   - Agents update routes in **real-time**, ensuring better coordination.  

4. **Simulation**  
   - A grid-based model of Bangalore roads is used to simulate vehicles.  
   - Agents continuously join, leave, and adapt their journeys.  

---

## 🛠️ Tech Stack
- **FastAPI** – backend server with REST & WebSocket endpoints  
- **Groq API** – AI inference for large-scale route optimisation  
- **NetworkX** – simulation of Bangalore road networks  
- **WebSockets** – agent-to-agent real-time communication  
- **Docker-ready** – future-proofing for deployment  

---

## 🚀 Running the Project

### 1. Clone the repo
```bash
git clone https://github.com/your-username/route-ai.git
cd route-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables
Create a `.env` file:
```
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=gemma-7b
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

### 5. Demo Simulation
Spin up **10 simulated cars** and see agents in action:
```bash
curl http://127.0.0.1:8000/demo?num_cars=10
```

Optimise all active routes:
```bash
curl -X POST http://127.0.0.1:8000/optimise
```

---

## 🔍 Project Structure
```
├── agent.py        # Agent state & naive route planning
├── groq_client.py  # Groq API integration for route optimisation
├── main.py         # FastAPI server, REST & WebSocket endpoints
├── simulator.py    # Fake Bangalore road network & simulation
├── requirements.txt
└── README.md
```

---

## 🎥 How to Visualise
- Connect agents via **WebSocket** (`/ws/agent`)  
- Watch them receive **neighbour updates** and **new routes** in real-time  
- Extend easily with a **frontend map** (Leaflet / Mapbox)  

---

## 🌟 Why This Project Stands Out
- **Scalable**: Works from 10 cars → 10,000+ cars.  
- **Real-time AI**: Powered by Groq’s **ultra-low latency LLMs**.  
- **Future-ready**: Can integrate with Google Maps, Uber, Ola, EV fleets.  
- **Social Impact**: Reduces traffic jams, emissions, and wasted human time.  

> ⚡ *Route AI is not just a hackathon project – it’s a blueprint for the future of Bangalore’s mobility.*

---

## 🏆 Hackathon Vision
- **MVP today**: Simulated Bangalore traffic with AI-driven coordination.  
- **Tomorrow**: Integration with **real-world GPS apps**, **IoT-enabled cars**, and **city-level traffic control systems**.  
- **Impact Goal**: Save **hundreds of hours per commuter annually**.  

---

## 🙌 Contributors
- **Team Route AI** – passionate about solving Bangalore’s most pressing problem with AI.  

---

## 📜 License
MIT License. Free to use, extend, and deploy.

---

🚦 *Let’s build a Bangalore where traffic flows like water, not concrete.* 🌆
