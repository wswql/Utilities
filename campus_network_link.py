import tkinter as tk
import tkinter.messagebox
import pickle
from tkinter import ttk
import requests
from json import loads
from io import BytesIO
from PIL import Image, ImageTk
from plyer import notification
import plyer.platforms.win.notification

def login(usename, password, operator):
    usename = usename
    password = password
    oper = {"移动": 2, "电信": 3, "联通": 4}
    data ='{"username":"","password":"","channel":"3","ifautologin":"1","pagesign":"secondauth","usripadd":""}'
    headers ={
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36-alive',
    }
    usripadd = requests.get(url='http://10.255.255.34/api/v1/ip', headers=headers)
    date = loads(data)
    usripadd = loads(usripadd.text)['data']
    date['usripadd'] = usripadd
    date["username"] = usename
    date["password"] = password
    date["channel"] = str(oper[operator])
    date = str(date).replace('\'', '\"').replace(' ', '')
    response = requests.post(url="http://10.255.255.34/api/v1/login", data=date, headers=headers)
    return loads(response.text)



def initialization(icon1):
    try:
        with open('C:\\usr_info.pickle', 'rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)
    except FileNotFoundError:
        exist_usr_info = {}
    win_execute = True
    if exist_usr_info:
        win_execute = False
        name = exist_usr_info['usr_name']
        password = exist_usr_info['usr_pwd']
        operat = exist_usr_info['operator']
        oper = {"移动": 0, "电信": 1, "联通": 2}
        operator = oper[operat]
        response = login(name, password, operat)
        code = response['code']
        if code == 200:
            notification.notify(
                title=operat,
                message=name + '：已成功登录',
                app_icon=icon1,
                timeout=2
            )

    else:
        name = ''
        password = ''
        operator = 1
    return name, password, operator,win_execute


def window(name, password, operator):
    # 窗口
    window = tk.Tk()
    window.title('nuist')
    window.geometry('450x300')
    # 画布放置图片
    canvas = tk.Canvas(window, height=300, width=500)
    img = Image.open(BytesIO(requests.get(url='http://10.255.255.34/img/pc_bg.36769bdf.png' ).content))
    imagefile = ImageTk.PhotoImage(img.resize((500,300), Image.ANTIALIAS))
    canvas.create_image(0, 0, anchor='nw', image=imagefile)
    canvas.pack(side='top')
    # 标签 用户名密码

    tk.Label(window, text='用户名:').place(x=100, y=110)
    tk.Label(window, text='密码:').place(x=100, y=150)
    tk.Label(window, text='运营商:').place(x=100, y=190)
    # 用户名输入框
    # entry_usr_name = tk.Entry(window, textvariable=var_usr_operator)
    var_usr_name = tk.StringVar(value=name)
    entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
    entry_usr_name.place(x=160, y=110)
    # 密码输入框
    var_usr_pwd = tk.StringVar(value=password)
    entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
    entry_usr_pwd.place(x=160, y=150)

    var_usr_operator = tk.StringVar()
    usr_operator = ttk.Combobox(window, textvariable=var_usr_operator)     # #创建下拉菜单
    usr_operator.pack()     # #将下拉菜单绑定到窗体
    usr_operator["value"] = ("移动", "电信", "联通")    # #给下拉菜单设定值
    usr_operator.current(operator)
    usr_operator.place(x=160, y=190)

    # 登录函数
    def usr_log_in():
        usr_name = var_usr_name.get()
        usr_pwd = var_usr_pwd.get()
        var_usr_operator = usr_operator.get()
        response = login(usr_name, usr_pwd, var_usr_operator)
        code = response['code']
        try:
            with open('C:\\usr_info.pickle', 'rb') as usr_file:
                usrs_info = pickle.load(usr_file)
        except FileNotFoundError:
            with open('C:\\usr_info.pickle', 'wb') as usr_file:
                usrs_info = {}
                pickle.dump(usrs_info, usr_file)
        # 判断用户名和密码是否匹配
        if code == 200:
            print(code)
            usrs_info['usr_name'] = usr_name
            usrs_info['usr_pwd'] = usr_pwd
            usrs_info['operator'] = var_usr_operator
            tk.messagebox.showinfo(title=var_usr_operator,
                                   message='已成功登陆' + usr_name)
            with open('C:\\usr_info.pickle', 'wb') as usr_file:
                pickle.dump(usrs_info, usr_file)
            window.destroy()

    # 登录 注册按钮
    bt_login = tk.Button(window, text='登录', command=usr_log_in)
    bt_login.place(x=200, y=230)

    # 主循环
    window.mainloop()
if __name__ == '__main__':
    icon = r'C:\pyCode\VAE\联网\favicon.ico'
    icon1 = r'C:\pyCode\VAE\联网\favicon1.ico'
    name, password, operator,win_execute = initialization(icon1)
    if win_execute:
        window(name, password, operator)