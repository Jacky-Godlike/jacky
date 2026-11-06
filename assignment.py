
pos_x = int(0)
pos_y = int(0)
battery = int(100)
movement=int(0)

#下面的这个我打算用来判断是否是喷到了障碍，但在下方操作代码中还没有加。
#(2,1)和(2,2)是障碍，小车的位置不能在这两点
def pos_check():
    if pos_x == 2 and pos_y == 1:
        return False
    elif pos_x == 2 and pos_y == 2:
        return False
    else:
        return True

#小车移动代码
while pos_x < 4 or pos_y < 4:
    print(f"position now :({pos_x},{pos_y})")
    print(f"battery now :{battery}%")
    origin_action = input("Please enter next step :")
    action = origin_action.lower()
    if action == "a":#操作a
        if pos_x == 0:
            print("Invalid action")
        else:
            pos_x -= 1
            ready=pos_check()#检查是否遇到障碍
            if ready==True:
                battery -= 10
                movement += 1
            else:
                pos_x += 1
                print("across obstacle")

    elif action == "d":#操作d
        if pos_x == 4:
            print("Invalid action")
        else:
            pos_x += 1
            ready = pos_check()  # 检查是否遇到障碍
            if ready == True:
                battery -= 10
                movement += 1
            else:
                pos_x -= 1
                print("across obstacle")

    elif action == "w":#操作w
        if pos_y == 4:
            print("Invalid action")
        else:
            pos_y += 1
            ready = pos_check()  # 检查是否遇到障碍
            if ready == True:
                battery -= 10
                movement += 1
            else:
                pos_y -= 1
                print("across obstacle")
    elif action == "s":#操作s
        if pos_y == 0:
            print("Invalid action")
        else:
            pos_y -= 1
            ready = pos_check()  # 检查是否遇到障碍
            if ready == True:
                battery -= 10
                movement += 1
            else:
                pos_y += 1
                print("across obstacle")
    elif action == "c":#操作c
        if battery==100:
            print("already fully charged, valid")
        else:
            battery = 100
            print("Battery has been fully charged.")
    elif action == "h":#操作h
        print("battery stage: ",battery)
        print("position now: ",(pos_x,pos_y))
        print("successful movement: ",movement)
        print("press a, s, w, d to move")
        print("press c to recharge")
        print("press h to help")
        print("press q to quit")
    elif action == "q":#操作q
        print("You have quit the movement.")
        print(f"Final position :({pos_x},{pos_y})")
        print(f"Left Battery : {battery}%")
        break
    else:
        print("Invalid action")
    print("------------------------------")




#结局
if pos_x == 4 and pos_y == 4:
    print(f"You have successfully reached destination(4,4)!")
    print(f"Left Battery : {battery}%")
