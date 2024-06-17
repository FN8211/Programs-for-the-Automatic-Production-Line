# write your script here
import time
import random
import datetime

vel = 120
acc = 150
Z = 113
x1 = 10
x2 = 10
x3 = 10
x4 = 10
a1 = 0
b1 = 0
c1 = 0
d1 = 0
a = 0
b = 0
c = 0
d = 0
task = 0
Full_Warmming_task = 0
timeout_start = 0
time_start = 0
time_start = time.time()
set_global_variable("p3", False)
write_digital_main_io(9, False)
write_digital_main_io(11, False)
remainingDays = 0
global device_lock

# 防撞击
wait(0.2)
if get_global_variable("reset") == 1:
    pose = read_tcp_pose()
    move_tool(pose[0], pose[1], 600, pose[3], velocity=5, acceleration=10, block=True, relative=False, frame='base',
              mode='deprecated', profile='trapezoidal')
else:
    pass
move_tool(447.2, 7.8, 600, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False, frame='base',
          mode='deprecated', profile='trapezoidal')
move_tool(447.2, 7.8, 500, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False, frame='base',
          mode='deprecated', profile='trapezoidal')
end_time = 0
seconds = 12


# # 读取上料机报警状态及下料机破真空
def timer(seconds):
    start_time = time.time()
    end_time = start_time + seconds
    return end_time


# 读取IO状态
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
    condition_14 = False
    condition_15 = False
    condition_16 = False


# 打印文本内容
def print_in():
    with open(file="jiami_1.txt", mode="r+") as record_activateDateTime:
        data = record_activateDateTime.read()
        print(data)


# 初次激活记录时间以及更新时间
def date_update(num, ID, payDays=0):
    if_delay_days = 0
    activateTime = datetime.datetime.now()
    activateDateTime = activateTime.strftime("%Y-%m-%d %H:%M:%S\t" + "激活时间\n")
    Remain_Days = "剩余天数:" + str(num)
    record_activateDateTime = open(file="jiami_1.txt", mode="r+")
    size = record_activateDateTime.readlines()
    sizeStr = len(size)
    if not sizeStr:
        project_ID = "项目编号: " + str(ID) + "\n"
        record_activateDateTime.write(project_ID)
        record_activateDateTime.write(activateDateTime)
        record_activateDateTime.write(Remain_Days)
        record_activateDateTime.write("\n0")
        record_activateDateTime.close()
        print("Activate Time has recorded completely!")
        print_in()
    elif num != 0:
        warnings_flag = size[3]
        if warnings_flag == "1":
            remind_flag = 1
        else:
            remind_flag = 0
        record_activateDateTime.truncate(0)
        record_activateDateTime.close()
        project_ID = "项目编号: " + str(ID) + "\n"
        with open(file="jiami_1.txt", mode="r+") as record_activateDateTime:
            record_activateDateTime.write(project_ID)
            record_activateDateTime.write(activateDateTime)
            record_activateDateTime.write(Remain_Days)
            if num <= 7:
                record_activateDateTime.write("\n1")
            else:
                record_activateDateTime.write("\n0")
        print_in()
        # 设备接近锁定提醒
        if 0 < num <= 7:
            num = str(num)
            # LockWarn = "设备使用期限仅剩：" + num + " 天，请及时延长使用期限!"
            # if_delay_days = dialog_yes_no("是否延长设备使用期限？", title=LockWarn, dialog_type=0, dialog_value=None)
            if if_delay_days:
                payDays = payDays
                # int(dialog_text("请输入延期天数: ", title='分期付款设备解锁', dialog_type=0, dialog_value=None))
            else:
                pass
        else:
            pass
    elif num <= 0:
        device_lock = 0
        record_activateDateTime.truncate(0)
        record_activateDateTime.close()
        project_ID = "项目编号: " + str(ID) + "\n"
        with open(file="jiami_1.txt", mode="r+") as record_activateDateTime:
            record_activateDateTime.write(project_ID)
            record_activateDateTime.write(activateDateTime)
            record_activateDateTime.write(Remain_Days)
            record_activateDateTime.write("\n0")
        # if_delay_days = dialog_yes_no("是否延长设备使用期限？", title="设备使用权限已到期，请及时延长使用期限！",dialog_type=0, dialog_value=None)
        if if_delay_days:
            payDays = payDays
            # int(dialog_text("请输入延期天数: ", title='分期付款设备解锁', dialog_type=0, dialog_value=None))
        else:
            pass
        print_in()
    else:
        print("No need to reactivate!")
        record_activateDateTime.close()
    return payDays


# 读取记录时间
def ifAuthorityPass():
    global recordTime_Year
    global recordTime_Mon
    global recordTime_Day
    with open(file="jiami_1.txt", mode="r+") as record_activateDateTime:
        lineData = record_activateDateTime.readlines()
        # print(lineData[1].strip("\n"))
        InvalidTime = lineData[1].strip("\n")
        InvalidTime = InvalidTime[0:19]
        recordTime_Year = int(InvalidTime[0:4])
        recordTime_Mon = int(InvalidTime[5:7])
        recordTime_Day = int(InvalidTime[8:10])
        # print(recordTime_Year, recordTime_Mon, recordTime_Day)
        return recordTime_Year, recordTime_Mon, recordTime_Day


# 更新剩余时间
def update_remain_days(offset, Remain):
    difference = Remain - offset
    print(difference)
    with open(file="jiami_1.txt", mode="r+") as record_activateDateTime:
        projectID = record_activateDateTime.readlines()
        projectID = (projectID[0])[5:]
        projectID = int(projectID)
    if difference <= 0:
        Remain = 0
        payDays = date_update(Remain, projectID)
        return Remain, payDays
    else:
        Remain = difference
        payDays = date_update(Remain, projectID)
        return Remain, payDays


# 更新时间和减少剩余时间
def update_and_reduceRemainTime(recordTime_YearData, recordTime_MonData, recordTime_DayData):
    global remainingDays, if_delay_days
    payDays = 0
    if_delay_days = 0
    # 当前时间
    currentTime = datetime.datetime.now()
    currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
    currentTime_Year = int(currentTime[0:4])
    currentTime_Mon = int(currentTime[5:7])
    currentTime_Day = int(currentTime[8:10])
    print(currentTime)

    with open(file="jiami_1.txt", mode="r+") as record_activateDateTime:
        days = record_activateDateTime.readlines()
        project_ID = (days[0])[5:]
        project_ID = int(project_ID)
        days = (days[2])[5:]
        days = int(days)
        # print(days)

    if currentTime_Year != recordTime_YearData or currentTime_Mon != recordTime_MonData or currentTime_Day != recordTime_DayData:
        if currentTime_Year < recordTime_Year:
            remainingDays = 0
            if_delay_days = int(
                dialog_yes_no("是否延长设备使用期限？", title="设备使用权限已到期，请及时延长使用期限！", dialog_type=0,
                              dialog_value=None))
            if if_delay_days:
                payDays = int(
                    dialog_text("请输入延期天数: ", title='分期付款设备解锁', dialog_type=0, dialog_value=None))
                date_update(remainingDays, project_ID, payDays)
            else:
                if_delay_days = 20
                pass

        else:
            temp_Mon = (currentTime_Year - recordTime_Year) * 12 + currentTime_Mon - recordTime_Mon
            temp_Day = temp_Mon * 31 + currentTime_Day - recordTime_Day
            # print(temp_Day)
            temp_mid = update_remain_days(temp_Day, days)
            remainingDays = temp_mid[0]
            if 0 < remainingDays <= 7:
                remainingDays_if = str(remainingDays)
                LockWarn = "设备使用期限仅剩：" + remainingDays_if + " 天，请及时延长使用期限!"
                if_delay_days = int(
                    dialog_yes_no("是否延长设备使用期限？", title=LockWarn, dialog_type=0, dialog_value=None))
                if if_delay_days:
                    payDays = int(
                        dialog_text("请输入延期天数: ", title='分期付款设备解锁', dialog_type=0, dialog_value=None))
                else:
                    if_delay_days = 10
                    pass
            elif remainingDays <= 0:
                device_lock = 0
                if_delay_days = int(
                    dialog_yes_no("是否延长设备使用期限？", title="设备使用权限已到期，请及时延长使用期限！",
                                  dialog_type=0, dialog_value=None))
                if if_delay_days:
                    payDays = int(
                        dialog_text("请输入延期天数: ", title='分期付款设备解锁', dialog_type=0, dialog_value=None))
                else:
                    if_delay_days = 3
                    pass

    else:
        remainingDays = days
        with open(file="jiami_1.txt", mode="r+") as record_activateDateTime:
            warnings_flag = (record_activateDateTime.readlines())[3]
            if warnings_flag == "1":
                remind_flag = 1
                device_lock = 1
            else:
                remind_flag = 0
        if 7 >= days > 0 == remind_flag:
            days = str(days)
            LockWarn = "设备使用期限仅剩：" + days + " 天，请及时延长使用期限!"
            if_delay_days = int(
                dialog_yes_no("是否延长设备使用期限？", title=LockWarn, dialog_type=0, dialog_value=None))
            if if_delay_days:
                payDays = int(
                    dialog_text("请输入延期天数: ", title='分期付款设备解锁', dialog_type=0, dialog_value=None))
            else:
                if_delay_days = 2
                pass
        elif days <= 0:
            device_lock = 0
            if_delay_days = int(
                dialog_yes_no("是否延长设备使用期限？", title="设备使用权限已到期，请及时延长使用期限！", dialog_type=0,
                              dialog_value=None))
            if if_delay_days:
                payDays = int(
                    dialog_text("请输入延期天数: ", title='分期付款设备解锁', dialog_type=0, dialog_value=None))
            else:
                if_delay_days = 3
                pass
    return remainingDays, payDays, if_delay_days


# 项目编号输入：
def ProjectID_Input():
    global remainingDays
    with open(file="jiami_1.txt", mode="r+") as record_activateDateTime:
        size = record_activateDateTime.readlines()
        is_empty = len(size)
    if is_empty == 0:
        projectID = int(dialog_text("请输入项目编号: ", title='分期付款设备解锁', dialog_type=0, dialog_value=None))
        if projectID > 1000:
            remainingDays = 150
        else:
            device_lock = 0
            print("项目编号不正确，请重新输入")
            projectID = (ProjectID_Input())[1]
            print(projectID)
    else:
        pass
    return remainingDays, projectID


# 终极密码计算
def final_password(project_num, DelayPayDays):
    finalPassWord = ((project_num / 1000) | (project_num % 1000)) + project_num / 1000 + DelayPayDays
    return finalPassWord


def clear_txtData():
    with open(file="jiami_1.txt", mode="r+") as record_activateDateTime:
        record_activateDateTime.truncate(0)


# 分期解锁密码输入
def DelayPayPass(project_num, payDays):
    RandNum1 = random.randint(999, 100000)
    RandNum2 = random.randint(999, 100000)
    RandNum3 = random.randint(999, 100000)
    RandNum1_Str = "随机码1: " + str(RandNum1) + " "
    RandNum2_Str = "随机码2: " + str(RandNum2) + " "
    RandNum3_Str = "随机码3: " + str(RandNum3) + " "
    print(RandNum1)
    print(RandNum2)
    print(RandNum3)
    DelayPayPass = (RandNum1 & RandNum2 | RandNum3) + payDays
    finalPassWord = (int((project_num / 1000)) | (project_num % 1000)) + int(project_num / 1000) + payDays
    print(finalPassWord)
    print(DelayPayPass)

    wait(1)
    # code = '分期付款设备解锁:随机码1:%s , 随机码2:%s , 随机码3:%s', %(RandNum1_Str, RandNum2_Str, RandNum3_Str)
    passWord = dialog_text("请输入解锁密码：", title='分期付款设备解锁:\n' + RandNum1_Str + RandNum2_Str + RandNum3_Str,
                           dialog_type=0, dialog_value=None)
    passWord = int(passWord)
    return passWord, DelayPayPass, finalPassWord


# 主脚本

# clear_txtData()
DelayPayDays = 0
device_lock = 1
with open(file="jiami_1.txt", mode="r+") as record_activateDateTime:
    judge = record_activateDateTime.readlines()
    judgeStr = len(judge)
    if judgeStr != 0:
        if_remind = judge[3]
        readID = (judge[0])[5:]
        readID = int(readID)
        reduce_days = ifAuthorityPass()
        recordTime_Year = reduce_days[0]
        recordTime_Mon = reduce_days[1]
        recordTime_Day = reduce_days[2]
        date_change = update_and_reduceRemainTime(recordTime_Year, recordTime_Mon, recordTime_Day)
        day_num = date_change[0]
        DelayPayDays = date_change[1]
        DelayFlag = date_change[2]
        print(date_change)
        print(day_num)
        print(DelayPayDays)
        if day_num > 7:
            device_lock = 1
        else:
            device_lock = 0
            if DelayFlag == 1:
                while day_num <= 7:
                    code = DelayPayPass(readID, DelayPayDays)
                    pass_Code = code[0]
                    pass_Delay = code[1]
                    pass_Final = code[2]
                    if pass_Code == pass_Delay:
                        change_day = day_num + DelayPayDays
                        date_update(change_day, readID)
                        dialog_choice("设备使用权限已延期，请继续使用", ["好的"], title='设备延期成功', dialog_type=1,
                                      dialog_value=None)
                        device_lock = 1
                        break
                    elif pass_Code == pass_Final:
                        change_day = 65535
                        date_update(change_day, readID)
                        dialog_choice("设备使用权限永久解锁，请继续使用", ["好的"], title='设备延期成功', dialog_type=1,
                                      dialog_value=None)
                        device_lock = 1
                        break
                    else:
                        print("密码输入不正确，请重新输入")
            elif DelayFlag == 2:
                device_lock = 1
                with open(file="jiami_1.txt", mode="r+") as record_activateDateTime:
                    rewrite = record_activateDateTime.readlines()
                    record_activateDateTime.truncate(0)
                with open(file="jiami_1.txt", mode="r+") as record_activateDateTime:
                    record_activateDateTime.write(rewrite[0])
                    record_activateDateTime.write(rewrite[1])
                    record_activateDateTime.write(rewrite[2])
                    record_activateDateTime.write("1")
                print_in()
            else:
                if if_remind == "1":
                    device_lock = 1
                else:
                    device_lock = 0

    else:
        RemainingDays = ProjectID_Input()
        print("剩余时间为：" + str(remainingDays))
        date_update(RemainingDays[0], RemainingDays[1])

while device_lock:
    out_time = 1
    get_global_variable("reset")
    get_global_variable("p1")
    condition_1 = read_digital_main_io(1)
    condition_2 = read_digital_main_io(2)
    condition_3 = read_digital_main_io(3)
    condition_4 = read_digital_main_io(4)
    condition_5 = read_digital_main_io(5)
    condition_6 = read_digital_main_io(6)
    condition_7 = read_digital_main_io(7)
    condition_8 = read_digital_main_io(8)
    condition_10 = read_digital_main_io(10)
    condition_14 = read_digital_main_io(14)
    condition_15 = read_digital_main_io(15)
    condition_16 = read_digital_main_io(16)
    condition_17 = read_digital_main_io(17)
    condition_18 = read_digital_main_io(18)
    condition_19 = read_digital_main_io(19)
    condition_20 = read_digital_main_io(20)

    if get_global_variable("reset") == 1:
        pose = read_tcp_pose()
        move_tool(pose[0], pose[1], 600, pose[3], velocity=5, acceleration=10, block=True, relative=False, frame='base',
                  mode='deprecated', profile='trapezoidal')
        move_tool(447.2, 7.8, 600, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                  frame='base', mode='deprecated', profile='trapezoidal')
        move_tool(447.2, 7.8, 500, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                  frame='base', mode='deprecated', profile='trapezoidal')

    # 各个工位准备情况
    if not condition_7:
        # 'condition_7' is False(1号下料位)
        x1 = 1
    if condition_8:
        # 'condition_8' is True
        x1 = 0
    if not condition_5:
        # 'condition_5' is False(2号下料位)
        x2 = 1
    if condition_6:
        # 'condition_6' is True
        x2 = 0
    if not condition_3:
        # 'condition_3' is False(3号下料位)
        x3 = 1
    if condition_4:
        # 'condition_4' is True
        x3 = 0
    if not condition_1:
        # 'condition_1' is False(4号下料位)
        x4 = 1
    if condition_2:
        # 'condition_2' is True
        x4 = 0

    # 初始化数据：
    if condition_8 == 0 and condition_7 == 0:
        write_digital_main_io(19, False)
    elif condition_8 == 1 or a1 > 12 or condition_7 == 0:
        a1 = 0

    if condition_6 == 0 and condition_5 == 0:
        write_digital_main_io(20, False)
    elif condition_6 == 1 or b1 > 12 or condition_5 == 0:
        b1 = 0

    if condition_4 == 0 and condition_3 == 0:
        write_digital_main_io(17, False)
    elif condition_4 == 1 or c1 > 12 or condition_3 == 0:
        c1 = 0

    if condition_2 == 0 and condition_1 == 0:
        write_digital_main_io(18, False)
    elif condition_2 == 1 or d1 > 12 or condition_1 == 0:
        d1 = 0

    # 工位锁
    if b1 == 0 and c1 == 0 and d1 == 0:
        # 允许1号工位下料标志
        a = 1
    else:
        a = 0
    if a1 == 0 and c1 == 0 and d1 == 0:
        # 允许2号工位下料标志
        b = 1
    else:
        b = 0
    if a1 == 0 and b1 == 0 and d1 == 0:
        # 允许3号工位下料标志
        c = 1
    else:
        c = 0
    if a1 == 0 and b1 == 0 and c1 == 0:
        # 允许1号工位下料标志
        d = 1
    else:
        d = 0

    # 破真空后复原层数减1
    if get_global_variable("p1") == 1 and a == 1 and a1 != 0:
        a1 = a1 - 1
        set_global_variable("p1", False)
    if get_global_variable("p1") == 1 and b == 1 and b1 != 0:
        b1 = b1 - 1
        set_global_variable("p1", False)
    if get_global_variable("p1") == 1 and c == 1 and c1 != 0:
        c1 = c1 - 1
        set_global_variable("p1", False)
    if get_global_variable("p1") == 1 and d == 1 and d1 != 0:
        d1 = d1 - 1
        set_global_variable("p1", False)

    # 感应到来料
    if condition_16:
        # 'condition_16' is True
        # timeout_start = time.time()
        wait(4)
        # 1号工位
        if x1 == 1 and a == 1:
            # 'x1' is True
            Z = 85
            a1 = a1 + 1
            Z = Z + a1 * 28 - (a1 - 1) * 2
            print(Z)
            move_tool(447.2, 7.8, 500, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(447.2, 7.8, 378.1, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            write_digital_main_io(12, True)
            write_digital_main_io(13, True)
            wait(0.5)
            move_tool(447.2, 7.8, 391, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(460, 7.8, 391, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(460, 7.8, 580, [179, -0.2, 179], velocity=80, acceleration=160, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(296.1, 559.7, 580, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(296.1, 559.7, 450, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            if Z < 200:
                move_tool(296.1, 559.7, Z + 100, [-180, 0, 180], velocity=vel, acceleration=acc, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(296.1, 559.7, Z + 20, [-180, 0, 180], velocity=40, acceleration=80, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(296.1, 559.7, Z, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
            else:
                move_tool(296.1, 559.7, Z + 20, [-180, 0, 180], velocity=40, acceleration=80, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(296.1, 559.7, Z, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
            write_digital_main_io(12, False)
            write_digital_main_io(13, False)
            move_tool(296.1, 559.7, Z + 20, [-180, 0, 180], velocity=40, acceleration=80, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(296.1, 559.7, 580, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(447.2, 7.8, 500, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            time_start = time.time()
            if a1 == 12:
                x1 = 0
                a = 0
                a1 = 0
                set_global_variable("a1", 12)
                write_digital_main_io(19, True)

        # 2号工位
        elif x2 == 1 and b == 1:
            # 'x2' is True
            Z = 85
            b1 = b1 + 1
            Z = Z + b1 * 28 - (b1 - 1) * 2
            move_tool(447.2, 7.8, 500, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(447.2, 7.8, 378.1, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            write_digital_main_io(12, True)
            write_digital_main_io(13, True)
            wait(0.5)
            move_tool(447.2, 7.8, 391, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(460, 7.8, 391, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(460, 7.8, 580, [179, -0.2, 179], velocity=80, acceleration=160, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(238.9, 297.8, 580, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(-92.9, 556.8, 580, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(-92.9, 556.8, 450, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            if Z < 200:
                move_tool(-92.9, 559.8, Z + 100, [-180, 0, 180], velocity=vel, acceleration=acc, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-92.9, 559.8, Z + 20, [-180, 0, 180], velocity=40, acceleration=80, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-92.9, 559.8, Z, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
            else:
                move_tool(-92.9, 559.8, Z + 20, [-180, 0, 180], velocity=40, acceleration=80, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-92.9, 559.8, Z, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
            write_digital_main_io(12, False)
            write_digital_main_io(13, False)
            move_tool(-92.9, 559.8, Z + 20, [-180, 0, 180], velocity=40, acceleration=80, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(-92.9, 559.8, 580, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(447.2, 7.8, 500, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            time_start = time.time()
            if b1 == 12:
                x2 = 0
                b = 0
                b1 = 0
                set_global_variable("b1", 12)
                write_digital_main_io(20, True)

        # 3号工位
        elif x3 == 1 and c == 1:
            # 'x3' is True
            Z = 85
            c1 = c1 + 1
            Z = Z + c1 * 28 - (c1 - 1) * 2
            move_tool(447.2, 7.8, 500, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(447.2, 7.8, 378.1, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            write_digital_main_io(12, True)
            write_digital_main_io(13, True)
            wait(0.5)
            move_tool(447.2, 7.8, 391, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(460, 7.8, 391, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(460, 7.8, 580, [179, -0.2, 179], velocity=80, acceleration=160, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(-99.3, -558.4, 580, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(-99.3, -558.4, 450, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            if Z < 200:
                move_tool(-99.3, -558.4, Z + 100, [-180, 0, 180], velocity=vel, acceleration=acc, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-99.3, -558.4, Z + 20, [-180, 0, 180], velocity=40, acceleration=80, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-99.3, -558.4, Z, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
            else:
                move_tool(-99.3, -558.4, Z + 20, [-180, 0, 180], velocity=40, acceleration=80, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(-99.3, -558.4, Z, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
            write_digital_main_io(12, False)
            write_digital_main_io(13, False)
            move_tool(-99.3, -558.4, Z + 20, [-180, 0, 180], velocity=40, acceleration=80, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(-99.3, -558.4, 580, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(447.2, 7.8, 500, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            time_start = time.time()
            if c1 == 12:
                x3 = 0
                c = 0
                c1 = 0
                set_global_variable("c1", 12)
                write_digital_main_io(17, True)

        # 4号工位
        elif x4 == 1 and d == 1:
            # 'x4' is True
            Z = 85
            d1 = d1 + 1
            Z = Z + d1 * 28 - (d1 - 1) * 2
            move_tool(447.2, 7.8, 500, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(447.2, 7.8, 378.1, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            write_digital_main_io(12, True)
            write_digital_main_io(13, True)
            wait(0.5)
            move_tool(447.2, 7.8, 391, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(460, 7.8, 391, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(460, 7.8, 580, [179, -0.2, 179], velocity=80, acceleration=160, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(302.6, -569.5, 580, [-179.7, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(302.6, -569.5, 450, [-179.7, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            if Z < 200:
                move_tool(302.6, -569.5, Z + 100, [-180, 0, 180], velocity=vel, acceleration=acc, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(302.6, -569.5, Z + 20, [-180, 0, 180], velocity=vel, acceleration=acc, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(302.6, -569.5, Z, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
            else:
                move_tool(302.6, -569.5, Z + 20, [-180, 0, 180], velocity=vel, acceleration=acc, block=True,
                          relative=False, frame='base', mode='deprecated', profile='trapezoidal')
                move_tool(302.6, -569.5, Z, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                          frame='base', mode='deprecated', profile='trapezoidal')
            write_digital_main_io(12, False)
            write_digital_main_io(13, False)
            move_tool(302.6, -569.5, Z + 20, [-180, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(302.6, -569.5, 580, [-179.7, 0, 180], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            move_tool(447.2, 7.8, 500, [179, -0.2, 179], velocity=vel, acceleration=acc, block=True, relative=False,
                      frame='base', mode='deprecated', profile='trapezoidal')
            time_start = time.time()
            if d1 == 12:
                x4 = 0
                d = 0
                d1 = 0
                set_global_variable("d1", 12)
                write_digital_main_io(18, True)

        # 长时间有料提示，防呆报警
        elif get_global_variable("out_time") == 1:
            move_to_pose("home", velocity=80, acceleration=120, block=True, offset=None, mode='deprecated',
                         profile='trapezoidal')

    else:
        # 超时回原
        time_end = time.time()
        waitting_time = time_end - time_start
        # print(waitting_time)
        if waitting_time > 120:
            move_to_pose("home", velocity=80, acceleration=120, block=True, offset=None, mode='deprecated',
                         profile='trapezoidal')  # write your script here