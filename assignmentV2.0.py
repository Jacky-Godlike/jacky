#初始化
pos_x = 0
pos_y = 0
battery = 100
movement = 0
#class记录轨迹
class Path:
    def __init__(self,x=0,y=0,z=100):
        self.point = [(x,y,z)] #起点
    def record(self,x,y,z):
        self.point.append((x,y,z))

#障碍检测函数
def barr_check():
    if pos_x == 2 and pos_y in [1,2]:
        print("Obstacle ahead!")
        return False
    else:
        return True

#边界检测函数
def edge_check():
    if pos_x not in range(0,5) or pos_y not in range(0,5):
        print("You can not cross the edge!")
        return False
    else:
        return True

#电量检测函数
def battery_check():
    global battery
    if battery < 0:
        print("You can not move , please charge your battery!")
        return False
    else:
        return True

#行动函数
def move():
    action = input("Please enter your action: ").lower()
    global pos_x, pos_y, battery
    if action == "a":  # 操作 a (向左)
        pos_x -= 1
        battery -= 10
        if barr_check() and edge_check() and battery_check():
            movement += 1
            pass
        else:
            pos_x += 1
            battery += 10
        return 0

    elif action == "d":  # 操作 d (向右)
        pos_x += 1
        battery -= 10
        if barr_check() and edge_check() and battery_check():
            movement += 1
            pass
        else:
            pos_x -= 1
            battery += 10
        return 0

    elif action == "w":  # 操作 w (向上)
        pos_y += 1
        battery -= 10
        if barr_check() and edge_check() and battery_check():
            movement += 1
            pass
        else:
            pos_y -= 1
            battery += 10
        return 0

    elif action == "s":  # 操作 s (向下)
        pos_y -= 1
        battery -= 10
        if barr_check() and edge_check() and battery_check():
            movement += 1
            pass
        else:
            pos_y += 1
            battery += 10
        return 0

    elif action == "c":  # 操作 c (充电)
        if battery == 100:
            print("You cannot charge your battery because it is full!")
        else:
            battery = 100
            print("Charged successfully!")
        return 0

    elif action == "h":  # 操作 h (提示)
        print("press a, s, w, d to move")
        print("press c to recharge")
        print("press h to help")
        print("press q to quit")
        manhattan_distance = 8 - pos_x - pos_y# 计算曼哈顿距离判断剩余电量
        if manhattan_distance * 10 > battery:
            print("You can't reach the destination without charging!")
        else:
            print("You don't need to charge your battery")
        return 0

    elif action == "q":  # 操作 q (退出)
        print("You have quit the movement.")
        print(f"Final position :({pos_x},{pos_y})")
        print(f"Left Battery : {battery}%")
        return 1
    else:
        print("Invalid action")

#定义track，对接class
track = Path(pos_x,pos_y,battery)

#while循环，直到到达终点
while pos_x != 4 or pos_y != 4:
    print("---------------------")
    print(f"Current position :({pos_x},{pos_y})")
    print(f"Current battery :{battery}%")
    if move() == 1:#检测是否按下q退出
        break
    else:
        pass
    track.record(pos_x,pos_y,battery)
#结局
if pos_x == 4 and pos_y == 4:
    print(f"You have successfully reached destination(4,4)!")
    print(f"Left Battery : {battery}%")
print(f"successful movement:"{movement})
print("Your path :",track.point)

