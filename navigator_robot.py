import sys
from collections import deque
from assignment_full import Robot, GRID_SIZE, GOAL, OBSTACLES, COST

class NavigatorRobot(Robot):  # 继承 Robot
    DIRECTIONS = {"W": (0, 1), "S": (0, -1), "A": (-1, 0), "D": (1, 0)}

    def __init__(self, *args, **kwargs):#全部Robot父类有什么都塞进来“*agrs"负责没有名字data变成tuple，”**kwargs"负责装下全部参数名字
        super().__init__(*args, **kwargs)  # 先让父类建好 x, y, battery…
        self.heights = self.bfs(GOAL)  # 再加上子类自己的高度图，用终点为起点

    # 重新写parent的move
    def move(self, action):
        result = super().move(action)  # 原本的规则完全照旧
        if action == "h":
            self.show_route_hint()  # 提供h加功能路线参考
        return result

    # BFS高山小球方法
    def is_free(self, cell):
        """
        格子有没有出格
        有没有障碍物
        """
        x, y = cell
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and cell not in OBSTACLES:
            return True
        return False

    def neighbors(self, cell):
        """
        机器人呼叫这个定义邻居，然后抽看抽direction信息key后检查这个邻居可不可以用后保存
        """
        x, y = cell
        for key, (dx, dy) in self.DIRECTIONS.items():
            n = (x + dx, y + dy)
            if self.is_free(n):
                yield key, n

    def bfs(self, start, show_steps=False):
        """从 start 出发做 BFS，回传 {格子: 步数}。"""
        dist = {start: 0}
        queue = deque([start])  # 第1个进去也是出去
        step = 0
        while queue:
            cell = queue.popleft()  # 取出最早放进去的格子
            new = []
            for _, n in self.neighbors(cell): #按键用不到，就写 _
                if n not in dist:  # 第一次发现 = 最短步数
                    dist[n] = dist[cell] + 1
                    queue.append(n)
                    new.append(n)
            if show_steps:
                step += 1
                self.output(f"第{step:2}步 取出 {cell} (步数 {dist[cell]})"
                            f" -> 新发现 {new if new else '无'}")
                self.output(f"        队列: {list(queue)}")
        return dist

    def shortest_path(self, start):
        """沿着高度一路 -1 走到终点（小球往下滚）。"""
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
        """帮助里的最短路线参考（只显示，不改变任何状态）。"""
        path, keys = self.shortest_path((self.x, self.y))
        if path is None:
            self.output("No route to the goal from here.")
            return
        self.output("Shortest route (ball rolling downhill):")
        self.output("  " + " -> ".join(map(str, path)))
        self.output(f"  Keys: {' '.join(keys)}   Steps: {len(keys)}"
                    f"   Battery needed: {len(keys) * COST}%")

    #显示算法过程
    def print_map(self, dist, title=""):
        """把每格的步数印成地图，y 大的在上面。"""
        if title:
            self.output(title)
        for y in range(GRID_SIZE - 1, -1, -1):
            row = []
            for x in range(GRID_SIZE):
                if (x, y) in OBSTACLES:
                    row.append(" X")
                elif (x, y) in dist:
                    row.append(f"{dist[(x, y)]:2}")
                else:
                    row.append(" .")
            self.output(f"  y={y}: " + " ".join(row))
        self.output("        " + " ".join(f"{x:2}" for x in range(GRID_SIZE)))

    def show_wave(self):
        """一层一层显示波怎么往外扩。"""
        for layer in range(max(self.heights.values()) + 1):
            reached = {c: d for c, d in self.heights.items() if d <= layer}
            self.print_map(reached, f"\n--- 第 {layer} 层 ---")

    def demo(self):
        """完整展示算法过程。"""
        self.output(f"\n终点 {GOAL}，障碍 {sorted(OBSTACLES)}")
        self.output("\n===== 1. 每一步队列怎么变 =====")
        self.bfs(GOAL, show_steps=True)
        self.output("\n===== 2. 波一层一层往外扩 =====")
        self.show_wave()
        self.output("\n===== 3. 从起点滚下去 =====")
        path, keys = self.shortest_path((self.x, self.y))
        self.output("路线: " + " -> ".join(map(str, path)))
        self.output(f"按键: {' '.join(keys)}（共 {len(keys)} 步）")


if __name__ == "__main__":
    robot = NavigatorRobot()

    if "demo" in sys.argv:  # python navigator_robot.py demo
        robot.demo()
    else:
        # 和 assignment 一样的主循环，只是换成子类
        while (robot.x, robot.y) != GOAL:
            robot.show_status()
            action = input("Command (w/a/s/d/c/h/q): ").strip().lower()
            if robot.move(action) == 1:
                break

        if (robot.x, robot.y) == GOAL:
            print(f"You have successfully reached destination{GOAL}!")
        robot.show_summary()