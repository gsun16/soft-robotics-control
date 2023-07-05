import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType
from time import sleep
import numpy as np

# 全局变量(当前坐标)
current_actual = None

def connect_robot():
    try:
        ip = "192.168.5.1"
        dashboard_p = 29999
        move_p = 30003
        feed_p = 30004
        print("正在建立连接...")
        dashboard = DobotApiDashboard(ip, dashboard_p)
        move = DobotApiMove(ip, move_p)
        feed = DobotApi(ip, feed_p)
        print(">.<连接成功>!<")
        return dashboard, move, feed
    except Exception as e:
        print(":(连接失败:(")
        raise e



def get_feed(feed: DobotApi):
    global current_actual
    hasRead = 0
    while True:
        data = bytes()
        while hasRead < 1440:
            temp = feed.socket_dobot.recv(1440 - hasRead)
            if len(temp) > 0:
                hasRead += len(temp)
                data += temp
        hasRead = 0

        a = np.frombuffer(data, dtype=MyType)
        if hex((a['test_value'][0])) == '0x123456789abcdef':

            # Refresh Properties
            current_actual = a["tool_vector_actual"][0]
            print("tool_vector_actual:", current_actual)

        sleep(0.001)



if __name__ == '__main__':
    dashboard, move, feed = connect_robot()
    print("开始上电...")
    dashboard.PowerOn()
    print("请耐心等待,机器人正在努力启动中...")
    count = 3
    while count > 0 :
        print(count)
        count = count - 1
        sleep(1)
    print("开始使能...")
    dashboard.EnableRobot()
    print("完成使能:)")
    '''
    feed_thread = threading.Thread(target=get_feed, args=(feed,))
    feed_thread.setDaemon(True)
    feed_thread.start()
    '''
    dashboard.SpeedFactor(50)

    dashboard.GetAngle()
    print("moving to initial position")
    move.JointMovJ(0,40,85,50,90,0)
    sleep(5)


    end = 0
    
    while end == 0:
        lang = input("waiting for command:\n")
        match lang:
            case "up":
                move.RelMovLTool(0,20,0,0,0,0,0)
                sleep(1)
                end =0


            case "down":
                print("going down")
                move.RelMovLTool(0,-20,0,0,0,0,0)
                sleep(1)
                end =0

            case "left":
                print("going left")
                move.RelMovLTool(20,0,0,0,0,0,0)
                sleep(1)
                end =0
        
            case "right":
                print("going right")
                move.RelMovLTool(-20,0,0,0,0,0,0)
                sleep(1)
                end =0


            case "grab":
                print("grabbing")
                end = 0
            case "release":
                print("releasing")
                end = 0


            case "end":
                print("ending program")
                move.JointMovJ(0,40,85,50,90,0)
                sleep(2)
                dashboard.DisableRobot()
                dashboard.close()
                end = 1

            case "reset":
                print("reseting position")
                move.JointMovJ(0,40,85,50,90,0)
                sleep(2)
                end = 0


            case _:
                print("invalid command, you can call up, down, left, right, grab, release, reset, or end")
                end = 0


