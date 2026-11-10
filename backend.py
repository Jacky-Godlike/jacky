GRID_SIZE = 5  # map 1--4
GOAL = (4, 4)  # end
OBSTACLES = {(2, 1), (2, 2)}  # obstacles
COST = 10  # cost with every move
FULL = 100  # full battery

HELP_TEXT = """Commands:
  W - move up    (y + 1)
  S - move down  (y - 1)
  A - move left  (x - 1)
  D - move right (x + 1)
  C - charge battery to 100%
  H - show this help
  Q - quit"""


def roll_ball(roll_x, roll_y):
    roll_x, roll_y = robot.x, robot.y
    path = [(robot.x, robot.y)]
    keys = ""
    if (roll_x, roll_y) in [(0, 1), (0, 2), (1, 1), (1, 2)]:
        while (roll_x, roll_y) != GOAL:
            while roll_y != 4:
                roll_y += 1
                path.append((roll_x, roll_y))
            roll_x += 1
            path.append((roll_x, roll_y))
    else:
        while (roll_x, roll_y) != GOAL:
            while roll_x != 4:
                roll_x += 1
                path.append((roll_x, roll_y))
            if (roll_x, roll_y) == GOAL:
                break
            roll_y += 1
            path.append((roll_x, roll_y))
    print("The best way to reach (4,4):  ",path)
    return path, keys

class Robot:
    def __init__(self,output=None):
        self.output=output
        self.x = x=0
        self.y = y=0
        self.battery = battery=FULL
        self.movement = 0
        self.recharges = 0
        self.path = [(x, y, battery)]  # record moves, start

    # test edge
    def edge_check(self, x, y):
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            print("You can not cross the edge!")
            return False
        return True

    # test obstacles
    def barr_check(self, x, y):
        if (x, y) in OBSTACLES:
            print("Obstacle ahead!")
            return False
        return True

    # test battery: lower the cost of one move, stop moving
    def battery_check(self):
        if self.battery < COST:
            print("You can not move, please charge your battery! (press C)")
            self.output("insufficient battery")
            return False
        return True

    # recharge: full battery should not be recharged
    def charge(self):
        if self.battery >= FULL:
            print("Battery is already full.")
        else:
            self.battery = FULL
            self.recharges += 1
            print("Battery charged to 100%.")

    # show status
    def show_status(self):
        print("---------------------")
        print(f"Current position :({self.x},{self.y})")
        print(f"Current battery :{self.battery}%")
        print(f"Successful moves :{self.movement}")
        print(f"Recharges :{self.recharges}")

    # end summery, appear in any kind of end
    def show_summary(self):
        delivered = (self.x, self.y) == GOAL
        print("========== Summary ==========")
        print(f"Final position :({self.x},{self.y})")
        print(f"Battery :{self.battery}%")
        print(f"Successful moves :{self.movement}")
        print(f"Recharges :{self.recharges}")
        print(f"Status :{'Delivered' if delivered else 'Not delivered'}")
        print("Your path :", self.path)

    # Process an instruction: return 1 for exit, 0 for continuation.
    def move(self, action):
        if action == "":
            print("You entered nothing. Press H to see all commands.")
            return 0
        if action == "q":
            return 1
        if action == "h":
            print(HELP_TEXT)
            roll_ball(self.x,self.y)

            return 0
        if action == "c":
            self.charge()
            return 0

        directions = {"a": (-1, 0), "d": (1, 0), "w": (0, 1), "s": (0, -1)}
        if action not in directions:
            print(f"Invalid command '{action}'. Press H to see all commands.")
            return 0

        dx, dy = directions[action]
        new_x, new_y = self.x + dx, self.y + dy

        # Check sequence: Edge, Obstacle, Battery. Short-circuit evaluation guarantees only the first failure is alerted.
        if (self.edge_check(new_x, new_y)
                and self.barr_check(new_x, new_y)
                and self.battery_check()):
            self.x, self.y = new_x, new_y
            self.battery -= COST
            self.movement += 1
            self.path.append((self.x, self.y, self.battery))
        return 0

robot = Robot()

# only end when reaches the final or q was pressed
if __name__ == "__main__":
    robot = Robot()
    while (robot.x,robot.y) != GOAL:
        robot.show_status()
        action = input("Command (w/a/s/d/c/h/q): ").strip().lower()
        if robot.move(action) == 1:
            break

    if (robot.x,robot.y) == GOAL:
        print(f"You have successfully reached destination{GOAL}!")
    robot.show_summary()