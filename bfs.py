# bfs.py —— 只放 BFS 算法，不放游戏逻辑
# 地图设置从 assignment.py 引入；找不到就用默认值，方便单独运行
# 运行：python bfs.py

from collections import deque

try:
    from assignment import GRID_SIZE, GOAL, OBSTACLES
    print("已从 assignment.py 引入地图设置")
except ImportError:
    GRID_SIZE = 5
    GOAL = (4, 4)
    OBSTACLES = {(2, 1), (2, 2)}
    print("找不到 assignment.py，使用默认地图")

DIRECTIONS = {"W": (0, 1), "S": (0, -1), "A": (-1, 0), "D": (1, 0)}


def is_free(cell):
    """格子在地图内，而且不是障碍。"""
    x, y = cell
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and cell not in OBSTACLES


def neighbors(cell):
    """回传 (按键, 邻居格子)，只包含能走的邻居。"""
    x, y = cell
    for key, (dx, dy) in DIRECTIONS.items():
        n = (x + dx, y + dy)
        if is_free(n):
            yield key, n


def bfs(start, show_steps=False):
    """
    从 start 出发做 BFS，回传 {格子: 步数}。
    从终点出发时，步数就是“高度”。
    show_steps=True 会印出每一步队列的变化。
    """
    dist = {start: 0}
    queue = deque([start])             # 先进先出
    step = 0

    while queue:
        cell = queue.popleft()         # 取出最早放进去的格子
        new = []
        for _, n in neighbors(cell):
            if n not in dist:          # 第一次发现 = 最短步数
                dist[n] = dist[cell] + 1
                queue.append(n)
                new.append(n)

        if show_steps:
            step += 1
            print(f"第{step:2}步 取出 {cell} (步数 {dist[cell]})"
                  f" -> 新发现 {new if new else '无'}")
            print(f"        队列: {list(queue)}")
    return dist


def print_map(dist, title=""):
    """把每格的步数印成地图，y 大的在上面。"""
    if title:
        print(title)
    for y in range(GRID_SIZE - 1, -1, -1):
        row = []
        for x in range(GRID_SIZE):
            if (x, y) in OBSTACLES:
                row.append(" X")
            elif (x, y) in dist:
                row.append(f"{dist[(x, y)]:2}")
            else:
                row.append(" .")       # 还没被波扩散到 / 到不了
        print(f"  y={y}: " + " ".join(row))
    print("        " + " ".join(f"{x:2}" for x in range(GRID_SIZE)))


def show_wave(dist):
    """一层一层显示波怎么往外扩。"""
    for layer in range(max(dist.values()) + 1):
        reached = {c: d for c, d in dist.items() if d <= layer}
        print_map(reached, f"\n--- 第 {layer} 层 ---")


def shortest_path(heights, start):
    """沿着高度一路 -1 走到终点（小球往下滚）。"""
    if start not in heights:
        return None, None
    path, keys = [start], []
    cell = start
    while heights[cell] > 0:
        for key, n in neighbors(cell):
            if heights.get(n) == heights[cell] - 1:
                path.append(n)
                keys.append(key)
                cell = n
                break
    return path, keys


if __name__ == "__main__":
    print(f"\n终点 {GOAL}，障碍 {sorted(OBSTACLES)}")

    print("\n===== 1. 每一步队列怎么变 =====")
    heights = bfs(GOAL, show_steps=True)

    print("\n===== 2. 波一层一层往外扩 =====")
    show_wave(heights)

    print("\n===== 3. 从起点滚下去 =====")
    path, keys = shortest_path(heights, (0, 0))
    print("路线:", " -> ".join(map(str, path)))
    print("按键:", " ".join(keys), f"（共 {len(keys)} 步）")
