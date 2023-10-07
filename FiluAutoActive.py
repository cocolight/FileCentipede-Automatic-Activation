# 导入包
import win32gui
import win32api
import win32con
import win32clipboard
import time
import pystray
from PIL import Image
import os
import threading
import psutil

stop_flag = 0



# 允许程序单实例运行
def multiRunJudge():

    current_pid = os.getpid()

    def proc_exist(process_name):
        pl = psutil.pids()
        p = None
        for pid in pl:
            if psutil.Process(pid).name() == process_name:
                if pid == current_pid:
                    continue
                else:
                    p = psutil.Process(pid)
        return p
            
    p = proc_exist('FiluAutoActive.exe')
    
    if p is not None:
        ##说明信息框
        s = win32api.MessageBox(0, "激活工具已运行 请勿重复运行!\n\n是否终止上一个进程 重新启动", "提醒",win32con.MB_OKCANCEL)
        if int(s) == 1:
            _exit(p)
        else:
            exit()

# 查找激活窗口句柄，查到返回 hwnd,edit,ddtime,btn；否则返回False
def findDlg():
    frame_class = 'Qt5152QWindowIcon'
    frame_name = '文件蜈蚣 - 激活码'
    hwnd = win32gui.FindWindow(frame_class,frame_name) 
    if hwnd == 0:
        return False
    elif hwnd > 0:
        left_top_x,left_top_y,right_bottom_x,right_bottom_y=win32gui.GetWindowRect(hwnd)

        # 文本框坐标
        def edit():
            edit_width = 578
            edit_height = 136
            edit_left_top_x = left_top_x + 12
            edit_left_top_y = left_top_y + 12
            # edit_right_bottom_x = edit_left_top_x + edit_width
            # edit_right_bottom_y = edit_left_top_y + edit_height
            edit_center_x = int(edit_left_top_x + edit_width/2)
            edit_center_y = int(edit_left_top_y + edit_height/2)
            return edit_center_x,edit_center_y

        # 到期时间坐标
        def ddtime():
            ddtime_width = 497
            ddtime_height = 25
            ddtime_left_top_x = left_top_x + 83
            ddtime_left_top_y = left_top_y + 303
            # ddtime_right_bottom_x = ddtime_left_top_x - ddtime_width
            # ddtime_right_bottom_y = ddtime_left_top_y + ddtime_height
            edit_center_x = int(ddtime_left_top_x + ddtime_width/2)
            edit_center_y = int(ddtime_left_top_y + ddtime_height/2)
            return edit_center_x,edit_center_y

        # 确定按钮
        def btn():
            ok_btn_width = 50
            ok_btn_height = 28
            ok_btn_right_bottom_x = right_bottom_x - 12
            ok_btn_right_bottom_y = right_bottom_y - 10
            # ok_btn_left_top_x = ok_btn_right_bottom_x - ok_btn_width
            # ok_btn_left_top_y = ok_btn_right_bottom_y - ok_btn_height
            ok_btn_center_x = int(ok_btn_right_bottom_x - ok_btn_width/2)
            ok_btn_center_y = int(ok_btn_right_bottom_y - ok_btn_height/2)
            return ok_btn_center_x,ok_btn_center_y

        pos_edit = edit()
        pos_ddtime = ddtime()
        pos_btn = btn()
        return hwnd,pos_edit,pos_ddtime,pos_btn

# 通过句柄窗口置顶
def winPos(hwnd,p = 1):
    try:
        if p == 1:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
        else:
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0,0,800,600, win32con.SWP_SHOWWINDOW)
    except Exception as e:
        pass

def findSuccessDlg():
    frame_class = 'Qt5152QWindowIcon'
    frame_name = 'success'
    hwnd = win32gui.FindWindow(frame_class,frame_name) 
    if hwnd == 0:
        return False
    elif hwnd > 0:
        left_top_x,left_top_y,right_bottom_x,right_bottom_y=win32gui.GetWindowRect(hwnd)

        # 确定按钮
        def btn():
            ok_btn_width = 48
            ok_btn_height = 28
            ok_btn_right_bottom_x = right_bottom_x - 15
            ok_btn_right_bottom_y = right_bottom_y - 13
            ok_btn_center_x = int(ok_btn_right_bottom_x - ok_btn_width/2)
            ok_btn_center_y = int(ok_btn_right_bottom_y - ok_btn_height/2)
            return ok_btn_center_x,ok_btn_center_y

        pos_btn = btn()
        return hwnd,pos_btn

# 点击左坐标控件
def pressLeft(x_y:tuple):
    win32api.SetCursorPos(x_y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_y[0],x_y[1],0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x_y[0],x_y[1],0,0)

def releaseKey(key_code):
    """
        函数功能：抬起按键
        参   数：key:按键值
    """
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), win32con.KEYEVENTF_KEYUP, 0)
 
def pressKey(key_code):
    """
        函数功能：按下按键
        参   数：key:按键值
    """
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 0, 0)

def ctrlA():
    # 模拟组合键输入ctrl+A
    # 注意：先按下的要后抬起
    CTRL = 17
    A = 65
    pressKey(CTRL)
    pressKey(A)
    releaseKey(A)
    releaseKey(CTRL)

def ctrlC():
    # 模拟组合键输入ctrl+C
    # 注意：先按下的要后抬起
    CTRL = 17
    C = 67
    pressKey(CTRL)
    pressKey(C)
    releaseKey(C)
    releaseKey(CTRL)

def ctrlV():
    # 模拟组合键输入ctrl+V
    # 注意：先按下的要后抬起
    CTRL = 17
    V = 86
    pressKey(CTRL)
    pressKey(V)
    releaseKey(V)
    releaseKey(CTRL)

def backspace():
    # 模拟backspace键的输入
    BACKSPACE = 8
    pressKey(BACKSPACE)
    releaseKey(BACKSPACE)

def getClickBoard():
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return text

def setClickBoard(str):
    win32clipboard .OpenClipboard()
    win32clipboard .EmptyClipboard()
    win32clipboard .SetClipboardData(win32con.CF_UNICODETEXT, str)
    win32clipboard .CloseClipboard()

def ctrl2():
    # 按下 ctrl 键
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    # 松开 ctrl 键
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    # 再次按下 ctrl 键
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    # 再次松开 ctrl 键
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

def str2DDatetime(time_str):
    from datetime import datetime
    format = "%Y-%m-%d %H:%M:%S"
    date_time = datetime.strptime(time_str,format)
    return date_time

def _db(data:list=None, query=False):
    from tinydb import TinyDB
    db = TinyDB("database.json")
    table = db.table("Code_ls")
    result = None
    if query is False:
        db.truncate()
        index = table.insert_multiple(data)
    else:
        result = table.all()
    db.close()
    return result

def getCode():
    code_ls = _db(query=True)

    def compare():
        code = None
        time_now = timeNow()
        # 选取可用激活码
        for code_row in code_ls:
            time_start = str2DDatetime(code_row['time_start'])
            time_stop = str2DDatetime(code_row['time_stop'])
            if time_now > time_start and time_now < time_stop:   
                code = code_row['code']
        return code
    
    code = compare()
    if code is None:
        code_ls = requestCode()
        _db(code_ls,query=False)
        getCode()
    else:
        return code

def requestCode():

    code_ls = []

    import requests
    import chardet
    from bs4 import BeautifulSoup

    url = "http://filecxx.com/zh_CN/activation_code.html"

    response = requests.get(url) # 发送一个 GET 请求
    encoding = chardet.detect(response.content)["encoding"] # 检测网页编码
    soup = BeautifulSoup(response.content, "html.parser", from_encoding=encoding) # 创建一个 BeautifulSoup 对象，并指定网页编码
    div_str = soup.find('div', id='code_list').find(name='pre').contents[0].strip().replace(" ", "")
    for row_raw in div_str.split('\n\n'):
        row = row_raw.split('\n')
        time_range = row[0]
        time_start = time_range[0:10] +" "+ time_range[10:18]
        # time_start = str2DDatetime(time_start)
        time_stop = time_range[19:29] +" "+ time_range[29:-1]
        # time_stop = str2DDatetime(time_stop)
        code = row[1]
        code_ls.append({'time_start':time_start,'time_stop':time_stop,'code':code})

    return code_ls
    
# 获取当前时间，返回YYYY-MM-DD HH:MM:SS
def timeNow() -> str:
    from time import strftime
    now = strftime("%Y-%m-%d %H:%M:%S")
    now = str2DDatetime(now)
    return now
 
# 退出
def _exit(p=None):
        if p is None:
            current_pid = os.getpid()
            p = psutil.Process(current_pid)
        try:
            p.kill()
        except Exception as e:
            pass
    
# 托盘程序退出
def on_exit(icon):
    stop_flag = 1
    _exit()
    icon.stop()

# 托盘菜单初始化
def trayInit():
    menu = (pystray.MenuItem(text='退出', action=on_exit),)
    image = Image.open("app_icon.png")
    icon = pystray.Icon("name", image, "文件蜈蚣\n自动激活", menu)
    return icon


# 主要逻辑
def main():
    if stop_flag != 0:
        return
    # 判断窗口是否打开，若打开返回控件列表
    while 1:
        time.sleep(1)
        # 获取窗口
        win = findDlg() # hwnd,edit,ddtime,btn
        if win is False:
            continue
        else:
            break

    # 获取当前鼠标位置
    point = win32api.GetCursorPos()
    # 隐藏窗口

    # 请求激活码
    code = getCode()

    setClickBoard(code)

    # 显示窗口

    # 置顶窗口，填入激活码
    winPos(win[0])
    pressLeft(win[1])
    # 删掉现有内容
    ctrlA()
    backspace()
    time.sleep(0.5)
    # 从剪贴板获取激活码
    getClickBoard()
    # 输入激活码
    ctrlV()
    # 点击确定
    pressLeft(win[3])
    time.sleep(0.1)
    # 判断激活是否成功
    flag = 5
    while flag:
        # closeSuccessDlg()
        # closeFaildDlg()
        sd = findSuccessDlg()
        if sd is False:
            pass
        else:
            winPos(sd[0])
            pressLeft(sd[1])
        flag = flag -1
   
    # 双击ctrl释放快捷键
    # ctrl2()
    # 还原鼠标位置
    win32api.SetCursorPos(point)
    
    main()

#————————————————————————————————————

if __name__ =='__main__':
    multiRunJudge()
    icon = trayInit()
    t1 = threading.Thread(target=main,daemon=True)
    t1.start()
    icon.run()