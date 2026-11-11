GRID_SIZE = 5                     # 地图 0~4
GOAL = (4, 4)                     # 终点
OBSTACLES = {(2, 1), (2, 2)}      # 障碍
COST = 10                         # 每步耗电
FULL = 100                        # 满电

HELP_TEXT = """Commands:
  W - move up    (y + 1)
  S - move down  (y - 1)
  A - move left  (x - 1)
  D - move right (x + 1)
  C - charge battery to 100%
  H - show this help
  Q - quit"""


class Robot:
    def __init__(self, x=0, y=0, battery=FULL, output=print):
        self.output = output            # 输出接口：控制台用 print，GUI 传入自己的函数
        self.x = x
        self.y = y
        self.battery = battery
        self.movement = 0
        self.recharges = 0
        self.path = [(x, y, battery)]   # 记录轨迹，起点

    # 边界检测
    def edge_check(self, x, y):
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            self.output("You can not cross the edge!")
            return False
        return True

    # 障碍检测
    def barr_check(self, x, y):
        if (x, y) in OBSTACLES:
            self.output("Obstacle ahead!")
            return False
        return True

    # 电量检测：电量不够走一步就不能动
    def battery_check(self):
        if self.battery < COST:
            self.output("You can not move, please charge your battery! (press C)")
            return False
        return True

    # 充电：满电时不计数
    def charge(self):
        if self.battery >= FULL:
            self.output("Battery is already full.")
        else:
            self.battery = FULL
            self.recharges += 1
            self.output("Battery charged to 100%.")

    # 显示当前状态
    def show_status(self):
        self.output("---------------------")
        self.output(f"Current position :({self.x},{self.y})")
        self.output(f"Current battery :{self.battery}%")
        self.output(f"Successful moves :{self.movement}")
        self.output(f"Recharges :{self.recharges}")

    # 最终总结，无论哪种方式结束都调用
    def show_summary(self):
        delivered = (self.x, self.y) == GOAL
        self.output("========== Summary ==========")
        self.output(f"Final position :({self.x},{self.y})")
        self.output(f"Battery :{self.battery}%")
        self.output(f"Successful moves :{self.movement}")
        self.output(f"Recharges :{self.recharges}")
        self.output(f"Status :{'Delivered' if delivered else 'Not delivered'}")
        self.output(f"Your path :{self.path}")

    # 处理一条指令：返回 1 表示退出，0 表示继续
    def move(self, action):
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

        # 检查顺序：边界 → 障碍 → 电量（短路求值保证只提示第一个失败项）
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

    # 只在送达或按 Q 时结束
    while (robot.x, robot.y) != GOAL:
        robot.show_status()
        action = input("Command (w/a/s/d/c/h/q): ").strip().lower()
        if robot.move(action) == 1:
            break

    if (robot.x, robot.y) == GOAL:
        print(f"You have successfully reached destination{GOAL}!")
    robot.show_summary()