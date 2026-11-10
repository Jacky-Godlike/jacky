import tkinter as tk
from backend import Robot, GOAL, OBSTACLES

# ---------- 继承：GuiRobot 是 Robot 的子类 ----------
class GuiRobot(Robot):
    def __init__(self):
        self.messages = []                          # 子类新增的属性
        super().__init__(output=self.add_message)   # 调用父类的 __init__

    def add_message(self, msg):                     # 子类新增的方法
        self.messages.append(msg)

    def charge(self):                               # 重写（override）父类方法
        super().charge()                            # 先做父类原本的充电逻辑
        self.add_message(f"Total recharges: {self.recharges}")

robot = GuiRobot()

root = tk.Tk()
root.title("Delivery Robot")

# ---------- 用 for loop 画 5x5 地图 ----------
cells = []
for i in range(5):               # i 是行（从上往下）
    row = []
    for j in range(5):           # j 是列（从左往右）
        cell = tk.Label(root, width=6, height=3, relief="ridge",
                        font=("Arial", 12, "bold"))
        cell.grid(row=i, column=j)
        row.append(cell)
    cells.append(row)

# 状态和提示
status_label = tk.Label(root, font=("Arial", 11), justify="left")
status_label.grid(row=5, column=0, columnspan=5, sticky="w", pady=5)

message_label = tk.Label(root, font=("Arial", 10), justify="left", fg="blue")
message_label.grid(row=6, column=0, columnspan=5, sticky="w")


ball_trail = []      # 小球已经滚过的格子（按 H 时的动画）
anim_id = None
game_over = False


def refresh():
    # 再用 for loop 更新每个格子
    for i in range(5):
        for j in range(5):
            x = j
            y = 4-i            #第零行在上方
            if (x, y) == (robot.x, robot.y):
                cells[i][j].config(text="R", bg="yellow")
            elif (x, y) in OBSTACLES:#用 j i来计算怎样的 x，y在障碍里面
                cells[i][j].config(text="X", bg="gray")
            elif (x, y) in ball_trail:
                cells[i][j].config(text="o", bg="lightblue")
            elif (x, y) == GOAL:
                cells[i][j].config(text="G", bg="#90ee90")
            else:
                cells[i][j].config(text=" ", bg="white")

    status_label.config(text=f"Position: ({robot.x},{robot.y})   "
                             f"Battery: {robot.battery}%   "
                             f"Moves: {robot.movement}   "
                             f"Recharges: {robot.recharges}")
    message_label.config(text="\n".join(robot.messages))

#最短路径函数
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
    return path,keys

def roll_animation(path,step=0):
    path, keys = roll_ball(robot.x, robot.y)
    # 每 300 毫秒让小球往下滚一格
    global anim_id
    if step < len(path):
        ball_trail.append(path[step])
        refresh()
        anim_id = root.after(300, roll_animation, path, step + 1)


def do(action):
    global anim_id
    if anim_id is not None:          # 停掉上一次的动画
        root.after_cancel(anim_id)
        anim_id = None
    ball_trail.clear()
    robot.messages.clear()
    result = robot.move(action)

    if game_over:
        return
    if result == 1 or (robot.x, robot.y) == GOAL:
        if (robot.x, robot.y) == GOAL:
            robot.add_message(f"You have successfully reached destination{GOAL}!")
        robot.show_summary()
        for b in buttons:
            b.config(state="disabled")

    refresh()
    if action == "h":                # 帮助：演示小球沿最短路线滚到终点
        path, keys = roll_ball(robot.x, robot.y)
        roll_animation(path,0)

def restart_game():
    """重置游戏，重新创建GuiRobot，恢复所有状态"""
    global robot, game_over, ball_trail, anim_id
    # 停止动画
    if anim_id is not None:
        root.after_cancel(anim_id)
        anim_id = None
    # 重置标记
    game_over = False
    ball_trail.clear()
    # 新建机器人实例
    robot = GuiRobot(output=None)
    robot.add_message("Reach G at (4,4). Press H for help.")
    # 恢复全部按钮可用
    for b in buttons:
        b.config(state="normal")
    refresh()


# ---------- 按钮 ----------
buttons = []
keys = ["w", "a", "s", "d", "c", "h", "q"]
frame = tk.Frame(root)
frame.grid(row=7, column=0, columnspan=5, pady=5)
for k in keys:
    b = tk.Button(frame, text=k.upper(), width=4,
                  command=lambda k=k: do(k))
    b.pack(side="left", padx=2)
    buttons.append(b)
# 新增 Restart 按钮
restart_btn = tk.Button(frame, text="RESTART", width=6, command=restart_game, bg="#88dd88")
restart_btn.pack(side="left", padx=4)
buttons.append(restart_btn)
# 键盘也能操作
root.bind("<Key>", lambda e: do(e.char.lower()) if e.char.lower() in keys else None)

robot.add_message("Reach G at (4,4). Press H for help.")
refresh()
root.mainloop()

# 初始化第一次游戏
restart_game()

root.mainloop()