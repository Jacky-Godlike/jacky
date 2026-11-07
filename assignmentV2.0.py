#initialization
pos_x = 0
pos_y = 0
battery = 100
movement = 0
recharge=0
#class to record moves
class Path:
    def __init__(self,x=0,y=0,z=100):
        self.point = [(x,y,z)] #start
    def record(self,x,y,z):
        self.point.append((x,y,z))

#function to check obstacles
def barr_check():
    if pos_x == 2 and pos_y in [1,2]:
        print("Obstacle ahead!")
        return False
    else:
        return True

#function to check edge
def edge_check():
    if pos_x not in range(0,5) or pos_y not in range(0,5):
        print("You can not cross the edge!")
        return False
    else:
        return True

#function to check batteries
def battery_check():
    global battery
    if battery < 0:
        print("You can not move , please charge your battery!")
        return False
    else:
        return True

#function to move
def move():
    action = input("Please enter your action: ").lower()
    global pos_x, pos_y, battery, movement,recharge
    if action == "a":  # press a (left)
        pos_x -= 1
        battery -= 10
        if barr_check() and edge_check() and battery_check():
            movement += 1
            pass
        else:
            pos_x += 1
            battery += 10
        return 0

    elif action == "d":  # press d (right)
        pos_x += 1
        battery -= 10
        if barr_check() and edge_check() and battery_check():
            movement += 1
            pass
        else:
            pos_x -= 1
            battery += 10
        return 0

    elif action == "w":  # press w (up)
        pos_y += 1
        battery -= 10
        if barr_check() and edge_check() and battery_check():
            movement += 1
            pass
        else:
            pos_y -= 1
            battery += 10
        return 0

    elif action == "s":  # press s (down)
        pos_y -= 1
        battery -= 10
        if barr_check() and edge_check() and battery_check():
            movement += 1
            pass
        else:
            pos_y += 1
            battery += 10
        return 0

    elif action == "c":  # press c (charge)
        if battery == 100:
            print("You cannot charge your battery because it is full!")
        else:
            battery = 100
            print("Charged successfully!")
            recharge += 1
        return 0

    elif action == "h":  # press h (help/hint)
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

    elif action == "q":  # press q (quit)
        print("You have quit the movement.")
        print(f"Final position :({pos_x},{pos_y})")
        print(f"Left Battery : {battery}%")
        print(f"recharged times: {recharge}")
        return 1
    else:
        print("Invalid action")

# define track，instantiate a class
track = Path(pos_x,pos_y,battery)

#while loops，until reaches the end
while pos_x != 4 or pos_y != 4:
    print("---------------------")
    print(f"Current position :({pos_x},{pos_y})")
    print(f"Current battery :{battery}%")
    print(f"recharged times: {recharge}")
    if move() == 1:# test if q was pressed to quit
        break
    else:
        pass
    track.record(pos_x,pos_y,battery)
#ending
if pos_x == 4 and pos_y == 4:
    print(f"You have successfully reached destination(4,4)!")
    print(f"Left Battery : {battery}%")
print(f"successful movement:{movement}")
print("Your path :",track.point)
print("recharged times:",recharge)
