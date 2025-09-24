# an-autonomous-delivery-agent-that-navigates-a-2D-grid-city-to-deliver-packages-no-ai-tools
An autonomous delivery agent that intelligently navigates grid-based cities using A* and local search algorithms. It dynamically adapts routes around moving obstacles and varying terrains to optimize package delivery efficiency in real-time scenarios.  


# Autonomous Delivery Agent: Grid City Navigator  

This is a small project showing how an agent can deliver packages inside a grid city. The agent needs to:  
- avoid roadblocks,  
- handle terrain with different travel costs,  
- and replan if obstacles move during the run.  

Algorithms  
- BFS → basic shortest path, ignores costs  
- UCS → finds cheapest path considering costs  
- A\ → faster with heuristic help  
- Hill Climb (with restarts)** → adapts when the world changes  

Features  
- Run tests on maps (from tiny grids to bigger “traffic” cases)  
- Tracks cost, time, and visited nodes  
- CLI to pick algorithm and run  
- You can make your own maps with a simple editor  
- Option to export results into a text or plot report  

Prerequisites  
- Python 3.8+  
- pip

SET UP 

1.Clone repo

Installation  
```bash
git clone https://github.com/your-username/autonomous-grid-delivery.git
cd autonomous-grid-delivery
```
2.Make venv (optional)
python -m venv venv
source venv/bin/activate     # mac/linux
venv\Scripts\activate        # win

3.Install deps if you see requirements.txt:
 
```bash
pip install requests
```

(Optionally: `pip install -r requirements.txt`)  


Usage  

Run BFS:  
```bash
python city_agent.py --algo bfs
```

Run UCS:  
```bash
python city_agent.py --algo ucs
```

Run A*:  
```bash
python city_agent.py --algo astar
```

Run Hill Climb:  
```bash
python city_agent.py --algo hill
```

Example Output  
```
Algorithm: A*
Path: [(0,0), (0,1), (1,1), (2,1), (3,1), (3,2), (3,3)]
Cost: 6
Visited: 18
Time: 0.002s
```
Contributing  
- Fork  
- Make a branch  
- Commit + push  
- Open PR  

License  
MIT  




