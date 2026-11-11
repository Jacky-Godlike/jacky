# Delivery Robot

A warehouse robot delivery simulator on a 5×5 grid (ERA111 Python assignment). The robot starts at `(0,0)` and has to reach the goal `G (4,4)` while avoiding obstacles and managing its battery.

On top of the core assignment, this version adds **BFS shortest-route navigation**, **auto-driving**, and **extra obstacles that appear near the goal**, plus a Tkinter GUI and a web version.

## Play online (no installation needed)

**https://robot-navigator-web.replit.app**

Open the link in a browser to play. You don't need to install Python or run anything locally.

- The web version was made with [Replit](https://replit.com). Replit's AI Agent converted the Tkinter GUI into a web app (React + TypeScript, compiled to JavaScript).
- In the browser the game logic runs as JavaScript, not Python. It ports the same rules: movement, battery, BFS shortest route, dynamic obstacles, auto navigation, message log and final summary. It also includes the BFS algorithm demo.
- You can download the original Python files from the site's "Source files" page.
- The Python files in this folder are the actual assignment submission. The web version is only an extra demo.


## Files

| File | Contents |
| --- | --- |
| `assignment_full.py` | Core `Robot` class: movement, boundary/obstacle/battery checks, recharging, status and summary. Can be run on its own in the console. |
| `navigator_robot.py` | `NavigatorRobot(Robot)` subclass: BFS height map, shortest-route hint, auto navigation, extra obstacles and an algorithm demo mode. |
| `gui.py` | Tkinter GUI built on `NavigatorRobot`. |
| `backup_original/` | Backup of the original code before changes. |

## Run locally

Requires Python 3 (developed on 3.13). Only the standard library is used (`tkinter`, `collections`, `sys`), so there is nothing to `pip install`.

```bash
# GUI
python gui.py

# Console: core assignment version
python assignment_full.py

# Console: navigator version
python navigator_robot.py

# BFS algorithm demo (queue changes, wave spreading layer by layer,
# shortest route, and re-planning after a block)
python navigator_robot.py demo
```

## Commands

| Key | Action |
| --- | --- |
| `W` | Move up (y + 1) |
| `S` | Move down (y - 1) |
| `A` | Move left (x - 1) |
| `D` | Move right (x + 1) |
| `C` | Recharge battery to 100% |
| `H` | Show help (the navigator version also shows the shortest route and the battery needed) |
| `Q` | Quit and show the summary |

Commands are case-insensitive, and leading/trailing spaces are ignored.

Extra controls in the GUI:
- **Navigator**: Navigator along the shortest route and recharges by itself when the battery is low. 
- **Show path**: highlights the current shortest route in light blue.
- **Show BFS steps**: shows each cell's BFS distance to the goal.
- **Reset**: starts a new game.
- You can also use the W/A/S/D/C/H/Q keys on the keyboard.

## Rules

- The grid is 5×5 with coordinates `(x, y)`. x increases to the right, y increases upwards, and `(0,0)` is the bottom-left corner.
- The battery starts at 100%, and each successful move uses 10%. You can still move with exactly 10% left, which leaves 0%. With less than 10% you must press `C` to recharge.
- A move is checked in this order: **boundary → obstacle → battery**. An invalid move is explained and the robot's state stays the same.
- Recharging only counts when the battery was below 100%.
- Obstacles:
  - Grey `X`: the fixed obstacles `(2,1)` and `(2,2)`, which never change.
  - Orange `X`: when the robot gets within 3 steps of the goal, the current recommended route is blocked. This happens only once, and the goal always stays reachable.
- The game ends when the robot reaches `(4,4)` (even with 0% battery) or when you press `Q`. The summary shows position, battery, successful moves, recharges, delivery status, the full path, and when and where extra obstacles appeared.

## How the navigation works (BFS, "ball rolling downhill")

1. Run BFS starting from the goal. This gives the minimum number of steps from every cell to the goal, which works like a height map with the goal at height 0.
2. At each step, the robot moves to a neighbour whose height is 1 lower, like a ball rolling downhill. Rolling all the way to the goal gives the shortest route.
3. When new obstacles appear, BFS runs again, the height map is updated, and the route is re-planned automatically.

You can change the settings at the top of `assignment_full.py` (`GRID_SIZE`, `GOAL`, `OBSTACLES`, `COST`, `FULL`) and `navigator_robot.py` (`TRIGGER_STEPS`).
