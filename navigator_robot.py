"""
Warehouse Robot Delivery Simulator - Navigator version (additional features)

How to run:
    python navigator_robot.py          # play in the console
    python navigator_robot.py demo     # step-by-step demo of the BFS algorithm
Commands: W/A/S/D = move, C = recharge, H = help + shortest route, Q = quit
Needs assignment_full.py in the same folder. Python 3 only, no extra packages.

Additional features (on top of the core Robot in assignment_full.py):
  1. BFS shortest-route hint (shown with H)
  2. Auto navigation (auto_step, used by the GUI "Auto" button)
  3. Extra obstacles that appear when the robot is close to the goal,
     followed by automatic re-planning. The fixed obstacles from Table 1
     are never changed, and the goal always stays reachable.

Note: this file was written with the help of an AI assistant (Claude).
"""

import sys
from collections import deque
from assignment_full import Robot, GRID_SIZE, GOAL, OBSTACLES, COST

TRIGGER_STEPS = 3      # Extra obstacles appear once the robot is within 3 steps of the goal


class NavigatorRobot(Robot):
    """Robot subclass that adds BFS navigation, auto-driving and dynamic obstacles."""

    DIRECTIONS = {"W": (0, 1), "S": (0, -1), "A": (-1, 0), "D": (1, 0)}

    def __init__(self, *args, **kwargs):
        """Build the parent state, then add a private obstacle set and the BFS height map."""
        super().__init__(*args, **kwargs)  # *args / **kwargs pass every parent argument through
        self.obstacles = set(OBSTACLES)    # Own copy, so extra obstacles never touch the original set
        self.extra_added = False           # Extra obstacles appear only once
        self.obstacle_log = []             # Record of when / where extra obstacles were added
        self.heights = self.bfs(GOAL)      # Steps-to-goal for every reachable cell

    def barr_check(self, x, y):
        """Same as the parent, but checks this robot's own obstacle set (including extra obstacles)."""
        if (x, y) in self.obstacles:
            self.output("Obstacle ahead!")
            return False
        return True

    def move(self, action):
        """Run the parent's rules unchanged, then add the route hint on H and check for extra obstacles."""
        result = super().move(action)
        if result == 1:                    # Quit: go straight to the summary
            return result
        if action == "h":
            self.show_route_hint()
        self.check_extra_obstacles()
        return result

    # ---------- Extra obstacles near the goal ----------
    def check_extra_obstacles(self):
        """Trigger the extra obstacles once, when the robot is within TRIGGER_STEPS of the goal."""
        if self.extra_added:
            return
        pos = (self.x, self.y)
        if pos == GOAL:
            return
        if self.heights.get(pos, 999) <= TRIGGER_STEPS:
            self.add_extra_obstacles()

    def add_extra_obstacles(self):
        """Block the current recommended route, but keep any cell that would make the goal unreachable."""
        robot_pos = (self.x, self.y)
        old_path, _ = self.shortest_path(robot_pos)
        if old_path is None:
            return
        added = []
        # Try to block every route cell except the robot's cell and the goal
        for cell in old_path[1:-1]:
            self.obstacles.add(cell)
            if robot_pos in self.bfs(GOAL):  # Goal still reachable?
                added.append(cell)           # Yes: keep this obstacle
            else:
                self.obstacles.remove(cell)  # No: remove it again
        self.extra_added = True
        self.heights = self.bfs(GOAL)        # Map changed, so recompute the height map
        self.obstacle_log.append({"move": self.movement,
                                  "position": robot_pos,
                                  "blocked_route": old_path,
                                  "added": added})
        self.output("Old route: " + " -> ".join(map(str, old_path)))
        self.output(f"New obstacles appeared at {added}! Re-planning...")
        self.show_route_hint()

    # ---------- Auto navigation ----------
    def auto_step(self):
        """Take one step along the shortest route (or recharge if needed). Return False if it cannot continue."""
        if (self.x, self.y) == GOAL:
            return False
        path, keys = self.shortest_path((self.x, self.y))
        if path is None:
            self.output("No route to the goal from here.")
            return False
        if self.battery < COST:
            self.move("c")                   # Not enough battery: recharge first
        else:
            self.move(keys[0].lower())       # Parent move() expects lowercase commands
        return True

    def show_summary(self):
        """Parent summary plus a line about the extra obstacles."""
        super().show_summary()
        if not self.obstacle_log:
            self.output("Extra obstacles :never appeared")
        for rec in self.obstacle_log:
            self.output(f"Extra obstacles :{rec['added']} appeared after "
                        f"move {rec['move']} at {rec['position']}")

    # ---------- BFS ("ball rolling downhill") ----------
    def is_free(self, cell):
        """Return True if the cell is inside the grid and not an obstacle."""
        x, y = cell
        return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and cell not in self.obstacles

    def neighbors(self, cell):
        """Yield (key, neighbour_cell) for every free neighbour of `cell`."""
        x, y = cell
        for key, (dx, dy) in self.DIRECTIONS.items():
            n = (x + dx, y + dy)
            if self.is_free(n):
                yield key, n

    def bfs(self, start, show_steps=False):
        """Breadth-first search from `start`. Return {cell: number of steps from start}."""
        dist = {start: 0}
        queue = deque([start])               # First in, first out
        step = 0
        while queue:
            cell = queue.popleft()           # Take the oldest cell in the queue
            new = []
            for _, n in self.neighbors(cell):
                if n not in dist:            # First time we reach a cell = shortest distance
                    dist[n] = dist[cell] + 1
                    queue.append(n)
                    new.append(n)
            if show_steps:
                step += 1
                self.output(f"Step {step:2}: take {cell} (distance {dist[cell]})"
                            f" -> new {new if new else 'none'}")
                self.output(f"         queue: {list(queue)}")
        return dist

    def shortest_path(self, start):
        """Follow the height map downhill (height - 1 each step) to the goal. Return (cells, keys)."""
        if start not in self.heights:
            return None, None
        path, keys = [start], []
        cell = start
        while self.heights[cell] > 0:
            for key, n in self.neighbors(cell):
                if self.heights.get(n) == self.heights[cell] - 1:
                    path.append(n)
                    keys.append(key)
                    cell = n
                    break
        return path, keys

    def show_route_hint(self):
        """Print the shortest route, keys, steps and battery needed. Does not change any state."""
        path, keys = self.shortest_path((self.x, self.y))
        if path is None:
            self.output("No route to the goal from here.")
            return
        self.output("Shortest route (ball rolling downhill):")
        self.output("  " + " -> ".join(map(str, path)))
        self.output(f"  Keys: {' '.join(keys)}   Steps: {len(keys)}"
                    f"   Battery needed: {len(keys) * COST}%")

    # ---------- Algorithm demo ----------
    def print_map(self, dist, title=""):
        """Print the step count of every cell as a grid (largest y at the top)."""
        if title:
            self.output(title)
        for y in range(GRID_SIZE - 1, -1, -1):
            row = []
            for x in range(GRID_SIZE):
                if (x, y) in self.obstacles:
                    row.append(" X")
                elif (x, y) in dist:
                    row.append(f"{dist[(x, y)]:2}")
                else:
                    row.append(" .")
            self.output(f"  y={y}: " + " ".join(row))
        self.output("        " + " ".join(f"{x:2}" for x in range(GRID_SIZE)))

    def show_wave(self):
        """Show how the BFS wave spreads out, one layer at a time."""
        for layer in range(max(self.heights.values()) + 1):
            reached = {c: d for c, d in self.heights.items() if d <= layer}
            self.print_map(reached, f"\n--- Layer {layer} ---")

    def demo(self):
        """Full walkthrough: queue steps, wave layers, shortest route, and re-planning after a block."""
        self.output(f"\nGoal {GOAL}, obstacles {sorted(self.obstacles)}")
        self.output("\n===== 1. How the queue changes each step =====")
        self.bfs(GOAL, show_steps=True)
        self.output("\n===== 2. The wave spreading layer by layer =====")
        self.show_wave()
        self.output("\n===== 3. Rolling down from the start =====")
        path, keys = self.shortest_path((self.x, self.y))
        self.output("Route: " + " -> ".join(map(str, path)))
        self.output(f"Keys: {' '.join(keys)} ({len(keys)} steps)")

        self.output("\n===== 4. Near the goal, the recommended route gets blocked =====")
        self.x, self.y = 4, 1  # Assume the robot went along the right side to (4,1)
        self.output(f"Assume the robot is at {(self.x, self.y)}")
        self.add_extra_obstacles()
        self.print_map(self.heights, "New height map:")


if __name__ == "__main__":
    robot = NavigatorRobot()

    if "demo" in sys.argv:  # python navigator_robot.py demo
        robot.demo()
    else:
        # Same main loop as assignment_full.py, using the subclass
        while (robot.x, robot.y) != GOAL:
            robot.show_status()
            action = input("Command (w/a/s/d/c/h/q): ").strip().lower()
            if robot.move(action) == 1:
                break

        if (robot.x, robot.y) == GOAL:
            print(f"You have successfully reached destination{GOAL}!")
        robot.show_summary()
