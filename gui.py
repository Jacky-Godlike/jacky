import tkinter as tk
from tkinter import scrolledtext
from assignment_full import GRID_SIZE, GOAL, OBSTACLES
from navigator_robot import NavigatorRobot

root = tk.Tk()
root.title("Delivery Robot + Navigator")

# ---------- 消息框（可以往下滚） ----------
text_box = scrolledtext.ScrolledText(root, width=60, height=12, font=("Consolas", 9))
text_box.grid(row=GRID_SIZE + 3, column=0, columnspan=GRID_SIZE, padx=5, pady=5)


def show_message(msg):   # 接到 Robot 的 output 接口
    text_box.insert("end", msg + "\n")
    text_box.see("end")  # 自动滚到最下面


robot = NavigatorRobot(output=show_message)
auto_running = False     # 自动导航是不是正在跑
game_over = False

# ---------- 用 for loop 画地图 ----------
cells = []
for i in range(GRID_SIZE):               # i 是行（从上往下）
    row = []
    for j in range(GRID_SIZE):           # j 是列（从左往右）
        cell = tk.Label(root, width=6, height=3, relief="ridge",
                        font=("Arial", 12, "bold"))
        cell.grid(row=i, column=j)
        row.append(cell)
    cells.append(row)

# 状态
status_label = tk.Label(root, font=("Arial", 11), justify="left")
status_label.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE, sticky="w", pady=5)

# 两个勾选框：显示最短路线 / 显示 BFS 步数
show_path = tk.BooleanVar(value=True)
show_heights = tk.BooleanVar(value=False)


def refresh():
    path_cells = set()
    if show_path.get():
        path, _ = robot.shortest_path((robot.x, robot.y))
        if path:
            path_cells = set(path)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = j
            y = GRID_SIZE - 1 - i        # 第 0 行在最上面，对应 y 最大
            pos = (x, y)
            text, bg = "", "white"
            if show_heights.get() and pos in robot.heights:
                text = str(robot.heights[pos])
            if pos in path_cells:
                bg = "lightblue"
            if pos == GOAL:
                text, bg = "G", "lightgreen"
            if pos in OBSTACLES:
                text, bg = "X", "gray"           # 老师原本的障碍
            elif pos in robot.obstacles:
                text, bg = "X", "orange"         # 后来出现的障碍
            if pos == (robot.x, robot.y):
                text, bg = "R", "yellow"
            cells[i][j].config(text=text, bg=bg)

    extra = "appeared" if robot.extra_added else "not yet"
    status_label.config(text=f"Position: ({robot.x},{robot.y})   "
                             f"Battery: {robot.battery}%   "
                             f"Moves: {robot.movement}   "
                             f"Recharges: {robot.recharges}   "
                             f"Extra obstacles: {extra}")


def finish():
    global game_over, auto_running
    game_over = True
    auto_running = False
    if (robot.x, robot.y) == GOAL:
        show_message(f"You have successfully reached destination{GOAL}!")
    robot.show_summary()
    for b in buttons:
        b.config(state="disabled")


def do(action):
    if game_over:
        return
    show_message(f"> {action.upper()}")
    result = robot.move(action)
    if result == 1 or (robot.x, robot.y) == GOAL:
        finish()
    refresh()


# ---------- 自动导航 ----------
def auto_tick():
    global auto_running
    if not auto_running or game_over:
        return
    ok = robot.auto_step()
    if (robot.x, robot.y) == GOAL:
        finish()
    elif not ok:
        auto_running = False
    refresh()
    if auto_running:
        root.after(400, auto_tick)       # 0.4 秒后再走下一步


def toggle_auto():
    global auto_running
    auto_running = not auto_running
    if auto_running:
        show_message("> AUTO start")
        auto_tick()
    else:
        show_message("> AUTO stop")


def reset():
    global robot, game_over, auto_running
    auto_running = False
    game_over = False
    text_box.delete("1.0", "end")
    robot = NavigatorRobot(output=show_message)
    for b in buttons:
        b.config(state="normal")
    show_message("New game. Reach G. Orange X will appear near the goal!")
    refresh()


# ---------- 按钮 ----------
buttons = []
keys = ["w", "a", "s", "d", "c", "h", "q"]
frame = tk.Frame(root)
frame.grid(row=GRID_SIZE + 1, column=0, columnspan=GRID_SIZE, pady=5)
for k in keys:
    b = tk.Button(frame, text=k.upper(), width=4,
                  command=lambda k=k: do(k))
    b.pack(side="left", padx=2)
    buttons.append(b)

auto_btn = tk.Button(frame, text="Auto", width=6, command=toggle_auto)
auto_btn.pack(side="left", padx=2)
buttons.append(auto_btn)

frame2 = tk.Frame(root)
frame2.grid(row=GRID_SIZE + 2, column=0, columnspan=GRID_SIZE)
tk.Checkbutton(frame2, text="Show path", variable=show_path,
               command=refresh).pack(side="left")
tk.Checkbutton(frame2, text="Show BFS steps", variable=show_heights,
               command=refresh).pack(side="left")
tk.Button(frame2, text="Reset", command=reset).pack(side="left", padx=8)

# 键盘也能操作
root.bind("<Key>", lambda e: do(e.char.lower()) if e.char.lower() in keys else None)

show_message("Reach G at (4,4). Press H for help. Orange X will appear near the goal!")
refresh()
root.mainloop()
