"""
Warehouse Robot Delivery Simulator - core version (ERA111 Assignment)

How to run:
    python assignment_full.py
Then type a command and press Enter:
    W/A/S/D = move, C = recharge, H = help, Q = quit
Commands are case-insensitive; leading/trailing spaces are ignored.
Requires Python 3 only (no extra packages).
"""

GRID_SIZE = 5                     # Warehouse is 5 x 5, x and y range 0..4
GOAL = (4, 4)                     # Delivery destination
OBSTACLES = {(2, 1), (2, 2)}      # Fixed obstacles from Table 1
COST = 10                         # Battery used per successful move (%)
FULL = 100                        # Full battery level (%)

HELP_TEXT = """Commands:
  W - move up    (y + 1)
  S - move down  (y - 1)
  A - move left  (x - 1)
  D - move right (x + 1)
  C - charge battery to 100%
  H - show this help
  Q - quit"""


class Robot:
    """Stores the robot state (position, battery, counters) and handles commands."""

    def __init__(self, x=0, y=0, battery=FULL, output=print):
        """Set the start state. `output` is where messages go (print for console, a GUI function otherwise)."""
        self.output = output
        self.x = x
        self.y = y
        self.battery = battery
        self.movement = 0               # Successful moves
        self.recharges = 0              # Recharge count
        self.path = [(x, y, battery)]   # Trail of (x, y, battery), starting point first

    def edge_check(self, x, y):
        """Return True if (x, y) is inside the grid, otherwise explain and return False."""
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            self.output("You can not cross the edge!")
            return False
        return True

    def barr_check(self, x, y):
        """Return True if (x, y) is not an obstacle, otherwise explain and return False."""
        if (x, y) in OBSTACLES:
            self.output("Obstacle ahead!")
            return False
        return True

    def battery_check(self):
        """Return True if there is enough battery for one move (10% is enough)."""
        if self.battery < COST:
            self.output("You can not move, please charge your battery! (press C)")
            return False
        return True

    def charge(self):
        """Recharge to 100%. The recharge counter only increases if the battery was below 100%."""
        if self.battery >= FULL:
            self.output("Battery is already full.")
        else:
            self.battery = FULL
            self.recharges += 1
            self.output("Battery charged to 100%.")

    def show_status(self):
        """Show position, battery, successful moves and recharges (before each command)."""
        self.output("---------------------")
        self.output(f"Current position :({self.x},{self.y})")
        self.output(f"Current battery :{self.battery}%")
        self.output(f"Successful moves :{self.movement}")
        self.output(f"Recharges :{self.recharges}")

    def show_summary(self):
        """Final summary, shown on both delivery and quit."""
        delivered = (self.x, self.y) == GOAL
        self.output("========== Summary ==========")
        self.output(f"Final position :({self.x},{self.y})")
        self.output(f"Battery :{self.battery}%")
        self.output(f"Successful moves :{self.movement}")
        self.output(f"Recharges :{self.recharges}")
        self.output(f"Status :{'Delivered' if delivered else 'Not delivered'}")
        self.output(f"Your path :{self.path}")

    def move(self, action):
        """Handle one command (already lowercased and stripped). Return 1 to quit, 0 to continue."""
        if action == "":
            self.output("You entered nothing. Press H to see all commands.")
            return 0
        if action == "q":
            return 1
        if action == "h":
            self.output(HELP_TEXT)
            return 0
        if action == "c":
            self.charge()
            return 0

        directions = {"a": (-1, 0), "d": (1, 0), "w": (0, 1), "s": (0, -1)}
        if action not in directions:
            self.output(f"Invalid command '{action}'. Press H to see all commands.")
            return 0

        dx, dy = directions[action]
        new_x, new_y = self.x + dx, self.y + dy

        # Check order: boundary -> obstacle -> battery.
        # Short-circuit `and` means only the first failing check is reported,
        # and the state is only updated when all three pass.
        if (self.edge_check(new_x, new_y)
                and self.barr_check(new_x, new_y)
                and self.battery_check()):
            self.x, self.y = new_x, new_y
            self.battery -= COST
            self.movement += 1
            self.path.append((self.x, self.y, self.battery))
        return 0


if __name__ == "__main__":
    robot = Robot()

    # Main loop: ends on delivery or when the user presses Q
    while (robot.x, robot.y) != GOAL:
        robot.show_status()
        action = input("Command (w/a/s/d/c/h/q): ").strip().lower()
        if robot.move(action) == 1:
            break

    if (robot.x, robot.y) == GOAL:
        print(f"You have successfully reached destination{GOAL}!")
    robot.show_summary()
