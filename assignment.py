## 定义一个 Robot class 
class Robot:
    def __init__(self, x=0, y=0, battery=100):
        self.x = x
        self.y = y
        self.battery = battery

    def pos_check(self, next_x, next_y):
        # 检查下一个位置是否是障碍物：(2,1) 和 (2,2)
        if (next_x == 2 and next_y == 1) or (next_x == 2 and next_y == 2):
            return False
        return True

# 初始数据与实例化小车
my_robot = Robot(0, 0, 100)
Destination = (4, 4)

# 小车移动代码
while my_robot.x < 4 or my_robot.y < 4:
    print(f"position now :({my_robot.x},{my_robot.y})")
    print(f"battery now :{my_robot.battery}%")
    
    origin_action = input("Please enter next step :")
    action = origin_action.lower()
    
    # 记录移动前的坐标，用于后面判断是否撞到障碍
    next_x, next_y = my_robot.x, my_robot.y
    moved = False

    if action == "a":  # 操作 a (向左)
        if my_robot.x == 0:
            print("Invalid action")
        else:
            next_x = my_robot.x - 1
            moved = True

    elif action == "d":  # 操作 d (向右)
        if my_robot.x == 4:
            print("Invalid action")
        else:
            next_x = my_robot.x + 1
            moved = True

    elif action == "w":  # 操作 w (向上)
        if my_robot.y == 4:
            print("Invalid action")
        else:
            next_y = my_robot.y + 1
            moved = True

    elif action == "s":  # 操作 s (向下)
        if my_robot.y == 0:
            print("Invalid action")
        else:
            next_y = my_robot.y - 1
            moved = True

    elif action == "c":  # 操作 c (充电)
        my_robot.battery = 100
        print("Battery has been fully charged.")

    elif action == "h":  # 操作 h (电量检查)
        # 计算曼哈顿距离判断剩余电量
        remaining_distance = (4 - my_robot.x) + (4 - my_robot.y)
        if remaining_distance * 10 > my_robot.battery:
            print("You can not reach destination without charging.")
        else:
            print("You can reach destination without charging by applying the shortest way.")

    elif action == "q":  # 操作 q (退出)
        print("You have quit the movement.")
        print(f"Final position :({my_robot.x},{my_robot.y})")
        print(f"Left Battery : {my_robot.battery}%")
        break

    else:
        print("Invalid action")

    # 如果触发了有效移动方向，进行障碍检查和电量扣除
    if moved:
        if not my_robot.pos_check(next_x, next_y):
            print("Obstacle ahead! Movement blocked.")
        else:
            my_robot.x = next_x
            my_robot.y = next_y
            my_robot.battery -= 10

    print("------------------------------")
    
# 结局
if my_robot.x == 4 and my_robot.y == 4:
    print(f"You have successfully reached destination(4,4)!")
    print(f"Left Battery : {my_robot.battery}%")
