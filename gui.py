"""
Warehouse Robot Delivery Simulator - Tkinter GUI (optional extra)

How to run:
    python gui.py
Click the buttons or press W/A/S/D/C/H/Q on the keyboard.
"Auto" drives along the shortest route; "Reset" starts a new game.
Needs assignment_full.py and navigator_robot.py in the same folder.
Python 3 only (tkinter is part of the standard library).

Note: this file was written with the help of an AI assistant (Claude).
"""

import tkinter as tk
from tkinter import scrolledtext
from assignment_full import GRID_SIZE, GOAL, OBSTACLES
from navigator_robot import NavigatorRobot

root = tk.Tk()
root.title("Delivery Robot + Navigator")

# ---------- Message box (scrollable) ----------
text_box = scrolledtext.ScrolledText(root, width=60, height=12, font=("Consolas", 9))
text_box.grid(row=GRID_SIZE + 3, column=0, columnspan=GRID_SIZE, padx=5, pady=5)


def show_message(msg):
    """Output function passed to the robot: append a line and scroll to the bottom."""
    text_box.insert("end", msg + "\n")
    text_box.see("end")


robot = NavigatorRobot(output=show_message)
auto_running = False     # Is auto navigation running?
game_over = False

# ---------- Draw the grid with a for loop ----------
cells = []
for i in range(GRID_SIZE):               # i = row, top to bottom
    row = []
    for j in range(GRID_SIZE):           # j = column, left to right
        cell = tk.Label(root, width=6, height=3, relief="ridge",
                        font=("Arial", 12, "bold"))
        cell.grid(row=i, column=j)
        row.append(cell)
    cells.append(row)

# Status line
status_label = tk.Label(root, font=("Arial", 11), justify="left")
status_label.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE, sticky="w", pady=5)

# Two checkboxes: show shortest route / show BFS step counts
show_path = tk.BooleanVar(value=True)
show_heights = tk.BooleanVar(value=False)


def refresh():
    """Redraw every cell and the status line from the robot's current state."""
    path_cells = set()
    if show_path.get():
        path, _ = robot.shortest_path((robot.x, robot.y))
        if path:
            path_cells = set(path)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = j
            y = GRID_SIZE - 1 - i        # Row 0 is at the top, which is the largest y
            pos = (x, y)
            text, bg = "", "white"
            if show_heights.get() and pos in robot.heights:
                text = str(robot.heights[pos])
            if pos in path_cells:
                bg = "lightblue"
            if pos == GOAL:
                text, bg = "G", "lightgreen"
            if pos in OBSTACLES:
                text, bg = "X", "gray"           # Fixed obstacles from Table 1
            elif pos in robot.obstacles:
                text, bg = "X", "orange"         # Extra obstacles added near the goal
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
    """End the game: show the result and summary, then disable the buttons."""
    global game_over, auto_running
    game_over = True
    auto_running = False
    if (robot.x, robot.y) == GOAL:
        show_message(f"You have successfully reached destination{GOAL}!")
    robot.show_summary()
    for b in buttons:
        b.config(state="disabled")


def do(action):
    """Send one command to the robot, finish if it quit or delivered, then redraw."""
    if game_over:
        return
    show_message(f"> {action.upper()}")
    result = robot.move(action)
    if result == 1 or (robot.x, robot.y) == GOAL:
        finish()
    refresh()


# ---------- Auto navigation ----------
def auto_tick():
    """Take one auto step, then schedule the next one 0.4 s later while auto is on."""
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
        root.after(400, auto_tick)


def toggle_auto():
    """Start or stop auto navigation."""
    global auto_running
    auto_running = not auto_running
    if auto_running:
        show_message("> AUTO start")
        auto_tick()
    else:
        show_message("> AUTO stop")


def reset():
    """Start a new game with a fresh robot."""
    global robot, game_over, auto_running
    auto_running = False
    game_over = False
    text_box.delete("1.0", "end")
    robot = NavigatorRobot(output=show_message)
    for b in buttons:
        b.config(state="normal")
    show_message("New game. Reach G. Orange X will appear near the goal!")
    refresh()


# ---------- Buttons ----------
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

# Keyboard control as well
root.bind("<Key>", lambda e: do(e.char.lower()) if e.char.lower() in keys else None)

show_message("Reach G at (4,4). Press H for help. Orange X will appear near the goal!")
refresh()
root.mainloop()
