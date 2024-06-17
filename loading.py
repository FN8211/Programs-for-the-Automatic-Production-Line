# write your script here
# from Plasma_Charging_Background import *
import time

write_digital_main_io(18, False)
write_digital_main_io(19, False)
write_digital_main_io(20, False)
write_digital_main_io(21, False)
write_digital_main_io(22, False)
write_digital_main_io(23, False)
write_digital_main_io(24, False)

# 防撞击
wait(0.2)
if get_global_variable("reset") == 1:
    write_digital_main_io(19, False)
    write_digital_main_io(20, False)
    pose = read_tcp_pose()
    move_tool(pose[0], pose[1], 600, pose[3], velocity=5, acceleration=10, block=True, relative=False, frame='base',
              mode='deprecated', profile='trapezoidal')
else:
    pass

move_to_pose("home", profile='trapezoidal')

vel = 120
acc = 120
Z = 423
a = 0
b = 0
c = 0
d = 0
a1 = 0
b1 = 0
c1 = 0
d1 = 0
P1 = 0
P2 = 0
P3 = 0
P4 = 0
overflag = 0

# 读取按钮状态，判断上料工位
start_parallel_script("Plasma_Charging_Parallel")


# 读取IO输入状态
def read_io_status():
    condition_1 = False
    condition_2 = False
    condition_3 = False
    condition_4 = False
    condition_5 = False
    condition_6 = False
    condition_7 = False
    condition_8 = False
    condition_10 = False
    condition_11 = False
    condition_16 = False


def timer(seconds):
    start_time = time.time()
    end_time = start_time + seconds
    return end_time


while True:
    # get_global_variable("reset")
    get_global_variable("x1")
    get_global_variable("x2")
    get_global_variable("x3")
    get_global_variable("x4")
    get_global_variable("p1")
    get_global_variable("p2")
    get_global_variable("p3")
    get_global_variable("p4")
    condition_1 = read_digital_main_io(1)
    condition_2 = read_digital_main_io(2)
    condition_3 = read_digital_main_io(3)
    condition_4 = read_digital_main_io(4)
    condition_5 = read_digital_main_io(5)
    condition_6 = read_digital_main_io(6)
    condition_7 = read_digital_main_io(7)
    condition_8 = read_digital_main_io(8)
    condition_10 = read_digital_main_io(10)
    condition_11 = read_digital_main_io(11)
    condition_16 = read_digital_main_io(16)
    condition_17 = read_digital_tool_io(1)
    condition_18 = read_digital_tool_io(2)

    # condition_2 = read_digital_main_io(2)
    # condition_4 = read_digital_main_io(4)
    # condition_6 = read_digital_main_io(6)
    # condition_8 = read_digital_main_io(8)
    if condition_1 == 1 or condition_3 == 1 or condition_5 == 1 or condition_7 == 1:
        if condition_2 == 1 or condition_4 == 1 or condition_6 == 1 or condition_8 == 1:
            out_high_range_time = timer(2)
            now_time = time.time()
            if out_high_range_time > now_time:
                write_digital_main_io(18, True)
                overflag = 1
                set_global_variable("overhigh", 1)
            else:
                pass
        else:
            pass
    else:
        pass

    # 每个工位不取料或者取超过12次，初始化数据
    if a > 12 or not get_global_variable("x1"):
        a = 0
    if b > 12 or not get_global_variable("x2"):
        b = 0
    if c > 12 or not get_global_variable("x3"):
        c = 0
    if d > 12 or not get_global_variable("x4"):
        d = 0

    # 每个工位允许运行的标志：
    if b == 0 and c == 0 and d == 0:
        a1 = 1
    else:
        a1 = 0
    if a == 0 and c == 0 and d == 0:
        b1 = 1
    else:
        b1 = 0
    if a == 0 and b == 0 and d == 0:
        c1 = 1
    else:
        c1 = 0
    if a == 0 and b == 0 and c == 0:
        d1 = 1
    else:
        d1 = 0

    # # 破真空后复原层数减1
    if get_global_variable("p1") == 1 and a >= 0 and a1 == 1:
        a = a - 1
        set_global_variable("p1", False)
    if get_global_variable("p1") == 1 and b >= 0 and b1 == 1:
        b = b - 1
        set_global_variable("p1", False)
    if get_global_variable("p1") == 1 and c >= 0 and c1 == 1:
        c = c - 1
        set_global_variable("p1", False)
    if get_global_variable("p1") == 1 and d >= 0 and d1 == 1:
        d = d - 1
        set_global_variable("p1", False)

    if get_global_variable("x1"):
        write_digital_main_io(24, True)
    else:
        write_digital_main_io(24, False)
    if get_global_variable("x2"):
        write_digital_main_io(23, True)
    else:
        write_digital_main_io(23, False)
    if get_global_variable("x3"):
        write_digital_main_io(22, True)
    else:
        write_digital_main_io(22, False)
    if get_global_variable("x4"):
        write_digital_main_io(21, True)
    else:
        write_digital_main_io(21, False)

    # 1号开始上料，没有检测到物料就持续上料
    if get_global_variable("x1") and a1 and condition_8 == 0 and condition_7:
        tail = 1
        if not condition_16:
            # 'condition_16' is False
            # wait(0.8)
            Z = 423
            a += 1
            Z = Z - a * 25 - (a - 1)
            if Z > 350:  # Z分两个高度走两种轨迹
                condition_a = True
            else:
                condition_a = False
            if condition_a:
                # 'condition_a' is True
                move_tool(245.5, 0, 580, [180, 0, 180], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(286.6, -570.6, 580, [179.5, 0.2, -177.5], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                move_tool(286.6, -570.6, Z + 15, [179.5, 0.2, -177.5], velocity=40, acceleration=100, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(286.6, -570.6, Z, [179.5, 0.2, -177.5], velocity=40, acceleration=100, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                while tail:
                    wait(0.1)
                    condition_17 = read_digital_tool_io(1)
                    condition_18 = read_digital_tool_io(2)
                    print(condition_17)
                    print(condition_18)
                    if condition_17 == 0 and condition_18 == 0:
                        tail = 0
                        a -= 1
                        print(a)
                        wait(0.5)
                    else:
                        if get_global_variable("p1") == 1 and a >= 0 and a1 == 1:
                            a = a - 1
                            set_global_variable("p1", False)
                        print(tail)
                        write_digital_main_io(19, False)
                        write_digital_main_io(20, False)
                        print(a)
                        print(1111111111111111)
                        Z = 423 - a * 25
                        print(Z)
                        move_tool(286.6, -570.6, Z, [179.5, 0.2, -177.5], velocity=80, acceleration=120, block=True,
                                  relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                        a += 1
                        write_digital_main_io(19, True)
                        write_digital_main_io(20, True)
                        wait(0.5)

                wait(0.5)
                pose = read_tcp_pose()
                Z = pose[2]
                if Z < 155 and Z > 125:
                    print(22222)
                    play_path("1-2")
                elif Z < 130:
                    play_path("1-1")
                elif Z < 350:
                    print(99999)
                    move_tool(286.6, -570.6, 350, [179.5, 0.2, -177.5], velocity=40, acceleration=100, block=True,
                              relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                else:
                    pass
                move_tool(286.6, -570.6, 580, [179.5, 0.2, -177.5], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(105.1, -195.2, 580, [179.5, 0.2, -177.5], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, 1.3, 580, [180, 0, -178], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, 1.3, 392, [180, 0, -178], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, False)
                write_digital_main_io(20, False)
                move_tool(374.6, 1.3, 580, [180, 0, -178], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                wait(20)
            else:
                # 'condition_a' is False
                move_tool(245.5, 0, 580, [180, 0, 180], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(286.6, -570.6, 580, [179.5, 0.2, -177.5], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                if Z < 335:
                    move_tool(286.6, -570.6, 350, [179.5, 0.2, -177.5], vel, acc, block=True, relative=False,
                              frame='base', mode='deprecated', profile='trapezoidal')
                else:
                    pass
                move_tool(286.6, -570.6, Z + 15, [179.5, 0.2, -177.5], vel, acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(286.6, -570.6, Z, [179.5, 0.2, -177.5], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                while tail:
                    condition_17 = read_digital_tool_io(1)
                    condition_18 = read_digital_tool_io(2)
                    if condition_17 == 0 and condition_18 == 0:
                        tail = 0
                        a -= 1
                        print(a)
                        wait(0.5)
                    else:
                        write_digital_main_io(19, False)
                        write_digital_main_io(20, False)
                        print(a)
                        Z = 423 - a * 25
                        print(Z)
                        move_tool(286.6, -570.6, Z, [179.5, 0.2, -177.5], vel, acc, block=True, relative=False,
                                  frame='base', mode='deprecated', profile='trapezoidal')
                        write_digital_main_io(19, True)
                        write_digital_main_io(20, True)
                        a += 1
                        wait(0.5)
                wait(0.5)
                if Z < 155 and Z > 125:
                    play_path("1-2")
                elif Z < 130:
                    play_path("1-1")
                else:
                    pass
                move_tool(286.6, -570.6, 350, [179.5, 0.2, -177.5], velocity=40, acceleration=100, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(286.6, -570.6, 580, [179.5, 0.2, -177.5], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(105.1, -195.2, 580, [179.5, 0.2, -177.5], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, 1.3, 580, [180, 0, -178], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, 1.3, 392, [180, 0, -178], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, False)
                write_digital_main_io(20, False)
                move_tool(374.6, 1.3, 580, [180, 0, -178], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                wait(20)


    # 2号开始上料，没有检测到物料就持续上料
    elif get_global_variable("x2") and b1 and condition_6 == 0 and condition_5:
        # 'x2' is True
        if not condition_16:
            # 'condition_16' is False
            # wait(0.8)
            Z = 423
            b += 1
            print(b)
            Z = Z - b * 25 - (b - 1)
            print(Z)
            if Z > 350:  # Z分两个高度走两种轨迹
                condition_a = True
            else:
                condition_a = False
            if condition_a:
                # 'condition_a' is True
                # move_tool(297.4, -558.4, 580, [179.8, -0.4, -179], vel, acc, block=True, relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, -0.7, 580, [180, 0, -179], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-48.4, -234.9, 580, [180, 0, -179], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-114.4, -558.4, 580, [179.8, -0.4, -179], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                move_tool(-114.4, -558.4, Z + 15, [179.8, -0.4, -179], vel, acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-114.4, -558.4, Z, [179.8, -0.4, -179], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, True)
                write_digital_main_io(20, True)
                wait(1)
                move_tool(-114.4, -558.4, 580, [179.8, -0.4, -179], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-48.4, -234.9, 580, [180, 0, -179], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, -0.7, 580, [180, 0, -179], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, -0.7, 392, [180, 0, -179], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, False)
                write_digital_main_io(20, False)
                move_tool(374.6, -0.7, 580, [180, 0, 180], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                wait(20)
            else:
                # 'condition_a' is False
                move_tool(374.6, -0.7, 580, [180, 0, -179], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-48.4, -234.9, 580, [180, 0, -179], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-114.4, -558.4, 580, [179.8, -0.4, -179], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                if Z < 335:
                    move_tool(-114.4, -558.4, 350, [179.8, -0.4, -179], vel, acc, block=True, relative=False,
                              frame='base', mode='deprecated', profile='trapezoidal')
                else:
                    pass
                move_tool(-114.4, -558.4, Z + 15, [179.8, -0.4, -179], vel, acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-114.4, -558.4, Z, [179.8, -0.4, -179], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, True)
                write_digital_main_io(20, True)
                wait(1)
                if Z < 155 and Z > 125:
                    move_to_pose("2-2", velocity=10, acceleration=50, block=True, offset=None, mode='deprecated',
                                 profile='trapezoidal')
                elif Z < 130:
                    move_to_pose("2-1", velocity=10, acceleration=50, block=True, offset=None, mode='deprecated',
                                 profile='trapezoidal')
                else:
                    pass
                move_tool(-114.4, -558.4, 350, [179.8, -0.4, -179], velocity=40, acceleration=100, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-114.4, -558.4, 580, [179.8, -0.4, -179], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-48.4, -234.9, 580, [180, 0, -179], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, -0.7, 580, [180, 0, -179], velocity=80, acceleration=150, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, -0.7, 392, [180, 0, -179], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, False)
                write_digital_main_io(20, False)
                move_tool(374.6, -0.7, 580, [180, 0, 180], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                wait(20)

    # 3号开始上料，没有检测到物料就持续上料
    elif get_global_variable("x3") and c1 and condition_4 == 0 and condition_3:
        # 'x3<3' is True
        if not condition_16:
            # 'condition_16' is False
            # wait(0.8)
            Z = 423
            c += 1
            Z = Z - c * 25 - (c - 1)
            if Z > 350:  # Z分两个高度走两种轨迹
                condition_a = True
            else:
                condition_a = False
            if condition_a:
                # 'condition_a' is True
                # move_tool(304.2, 561.7, 580, [-179.5,-0.4,-178.2], vel, acc, block=True, relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, -0.7, 580, [180, -0.6, -178.2], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-58.1, 258.1, 580, [-179.5, -0.4, -178.2], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-104.3, 561.7, 580, [-179.5, -0.4, -178.2], vel, acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-104.3, 561.7, Z + 15, [-179.5, -0.4, -178.2], vel, acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-104.3, 561.7, Z, [-179.5, -0.4, -178.2], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, True)
                write_digital_main_io(20, True)
                wait(1)
                move_tool(-104.3, 561.7, 580, [-179.5, -0.4, -178.2], velocity=40, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-58.1, 258.1, 580, [-179.5, -0.4, -178.2], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                move_tool(374.6, -0.7, 580, [180, -0.6, -178.2], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, -0.7, 392, [180, -0.6, -178.2], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, False)
                write_digital_main_io(20, False)
                move_tool(374.6, -0.7, 580, [180, 0, -178.2], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                wait(20)
            else:
                # 'condition_a' is False
                # move_tool(304.2, 561.7, 580, [180,0.6,-178.2], vel, acc, block=True, relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, -0.7, 580, [180, -0.6, -178.2], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-58.1, 258.1, 580, [-179.5, -0.4, -178.2], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                move_tool(-104.3, 561.7, 580, [-179.5, -0.4, -178.2], vel, acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                if Z < 335:
                    move_tool(-104.3, 561.7, 350, [-179.5, -0.4, -178.2], vel, acc, block=True, relative=False,
                              frame='base', mode='deprecated', profile='trapezoidal')
                else:
                    pass
                move_tool(-104.3, 561.7, Z + 15, [-179.5, -0.4, -178.2], vel, acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-104.3, 561.7, Z, [-179.5, -0.4, -178.2], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, True)
                write_digital_main_io(20, True)
                wait(1)
                if Z < 155 and Z > 125:
                    move_to_pose("3-2", velocity=10, acceleration=50, block=True, offset=None, mode='deprecated',
                                 profile='trapezoidal')
                elif Z < 130:
                    move_to_pose("3-1", velocity=10, acceleration=50, block=True, offset=None, mode='deprecated',
                                 profile='trapezoidal')
                else:
                    pass
                move_tool(-104.3, 561.7, 350, [-179.5, -0.4, -178.2], velocity=40, acceleration=100, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-104.3, 561.7, 580, [-179.5, -0.4, -178.2], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-58.1, 258.1, 580, [-179.5, -0.4, -178.2], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                move_tool(374.6, -0.7, 580, [180, -0.6, -178.2], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, -0.7, 392, [180, -0.6, -178.2], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, False)
                write_digital_main_io(20, False)
                move_tool(374.6, -0.7, 580, [180, 0, -178.2], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                wait(20)

        # 4号开始上料，没有检测到物料就持续上料
    elif get_global_variable("x4") and d1 and condition_2 == 0 and condition_1:
        # 'x4' is True
        if not condition_16:
            # 'condition_16' is False
            # wait(0.8)
            Z = 423
            d += 1
            Z = Z - d * 25 - (d - 1)
            if Z > 350:  # Z分两个高度走两种轨迹
                condition_a = True
            else:
                condition_a = False
            if condition_a:
                # 'condition_a' is True
                move_tool(177.3, 233.8, 580, [180, 0.3, -179.6], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(307.2, 548.1, 580, [180, 0.3, -179.6], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                move_tool(307.2, 548.1, Z + 15, [180, 0.3, -179.6], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                move_tool(307.2, 548.1, Z, [180, 0.3, -179.6], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, True)
                write_digital_main_io(20, True)
                wait(1)
                move_tool(307.2, 548.1, 580, [180, 0.3, -179.6], velocity=40, acceleration=100, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(177.3, 233.8, 580, [180, 0.3, -179.6], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, 0.3, 580, [180, 0, 180], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, 0.3, 392, [180, 0, 180], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, False)
                write_digital_main_io(20, False)
                move_tool(374.6, 0.3, 580, [180, 0, 180], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                wait(20)
            else:
                # 'condition_a' is False
                move_tool(177.3, 233.8, 580, [180, 0.3, -179.6], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(307.2, 548.1, 580, [180, 0.3, -179.6], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                if Z < 335:
                    move_tool(307.2, 548.1, 350, [180, 0.3, -179.6], vel, acc, block=True, relative=False, frame='base',
                              mode='deprecated', profile='trapezoidal')
                else:
                    pass
                move_tool(307.2, 548.1, Z + 15, [180, 0.3, -179.6], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                move_tool(307.2, 548.1, Z, [180, 0.3, -179.6], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, True)
                write_digital_main_io(20, True)
                wait(1)
                if Z < 155 and Z > 125:
                    move_to_pose("4-2", velocity=10, acceleration=50, block=True, offset=None, mode='deprecated',
                                 profile='trapezoidal')
                elif Z < 130:
                    move_to_pose("4-1", velocity=10, acceleration=50, block=True, offset=None, mode='deprecated',
                                 profile='trapezoidal')
                else:
                    pass
                move_tool(307.2, 548.1, 350, [180, 0.3, -179.6], velocity=40, acceleration=100, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(307.2, 548.1, 580, [180, 0.3, -179.6], velocity=80, acceleration=160, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(177.3, 233.8, 580, [180, 0.3, -179.6], velocity=80, acceleration=120, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, 0.3, 580, [180, 0, 180], velocity=80, acceleration=120, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(374.6, 0.3, 392, [180, 0, 180], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                write_digital_main_io(19, False)
                write_digital_main_io(20, False)
                move_tool(374.6, 0.3, 580, [180, 0, 180], vel, acc, block=True, relative=False, frame='base',
                          mode='deprecated', profile='trapezoidal')
                wait(20)
    else:
        # 4个工位都没有物料，回原
        write_digital_main_io(24, False)
        write_digital_main_io(23, False)
        write_digital_main_io(22, False)
        write_digital_main_io(21, False)
        move_to_pose("home", profile='trapezoidal')

