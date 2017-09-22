import Function as fc
from tkinter import *
import tkinter.messagebox #这个是消息框，对话框的关键
def OutputInfo(index,type = 0):
    return
# fc,HOST,fc.PORT,fc.USER,fc.PASSWD,fc.DB
def main(host,port,user,passwd,db):
    # 用户输入信息 函数
    fc.InputInfo(host,port,user,passwd,db)
    # 登录数据库
    if fc.DbLogin():
        #查询客户数据库 获取对应信息 函数 FindDBInfo()#得到一个数据库商品列表 INFOLIST_C
        if fc.FindDBInfo():
            SuccussCount = 0
            HavedCount = 0
            NowDoCount = 0
            #提取出数据库已有的每一条商品信息
            sqlShow_Info['text'] = "正在处理" + str(len(fc.INFOLIST_C)) + "条数据！\n请勿退出"
            root.update_idletasks()
            tkinter.messagebox.showinfo('正在上传','上传中')
            for i in range(len(fc.INFOLIST_C)):
                NowDoCount += 1
                fc.GOODS_SN = fc.INFOLIST_C[i][0] #货品编号
                fc.ADD_TIME = fc.INFOLIST_C[i][1] #添加时间
                fc.GOODS_DESC = b'<P>' + fc.INFOLIST_C[i][2] + b'</p>' #商品详情
                fc.GOODS_NAME = fc.INFOLIST_C[i][2] #商品名称
                fc.SUPPLIER_NAME = fc.INFOLIST_C[i][3] #店铺名称
                fc.USER_NAME = fc.INFOLIST_C[i][4] #入驻商账号  入驻商备注

                #检查该商品是否重复，重复则跳过 True 则重复
                if fc.CheckGoodsRepeat():
                    HavedCount += 1
                    print("第 ",i,"条 商品 重复，查看下一条")
                    continue
                #检查当前店铺是否存在 True 则重复
                if fc.CheckSupplierRepeat() == False:
                    #店铺不存在，则新建一个店铺
                    print('该店铺不存在，则新建一个店铺')
                    #新建店铺之前，确定supplier_id 和 user_id，便于直接绑定
                    fc.DefineID()
                    #新建一个店铺
                    fc.CreateSupplier()
                    #会员账号与店铺绑定
                    fc.BindUserSupplier()
                    #装修店铺
                    fc.DecorationSupplier()
                else:
                    print('该店铺已经存在')
                    # 确定Supplier_id  ,以便于添加商品
                    fc.DefineID(0)
                # 找到所有图片
                fc.FindImgInfo()

                #开始添加商品
                fc.AddGoods()
                #建立店铺分类
                fc.AddSupplierCategory()
                #商品与店铺绑定
                fc.BindCatGoods()
                #添加图片
                fc.AddGoodsImg()
                SuccussCount += 1

        #数据库数据提交 与 关闭
            tkinter.messagebox.showinfo('已完成\n', '成功: '+ str(SuccussCount)+'\n重复: '+ str(HavedCount) + '\n共计: ' + str (len(fc.INFOLIST_C)))
        fc.DbClose()
    else:
        #登录数据库失败处理
        tkinter.messagebox.showerror('you are wrong', '数据库登录信息有误')
        return False

# main()
class Reg(Frame):
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.sqlAddress = Label(frame, text="主机地址:")
        self.sqlAddress.grid(row=0, column=0, sticky=W)
        self.sqlAddress_Info = Entry(frame)
        self.sqlAddress_Info.grid(row=0, column=1, sticky=W)

        self.sqlPin = Label(frame, text="端口:")
        self.sqlPin.grid(row=1, column=0, sticky=W)
        self.sqlPin_Info = Entry(frame)
        self.sqlPin_Info.grid(row=1, column=1, sticky=W)

        self.sqlName = Label(frame, text="账户:")
        self.sqlName.grid(row=2, column=0, sticky=W)
        self.sqlName_Info = Entry(frame)
        self.sqlName_Info.grid(row=2, column=1, sticky=W)

        self.sqlPsw = Label(frame, text="密码:")
        self.sqlPsw.grid(row=3, column=0)
        self.sqlPsw_Info = Entry(frame, show="*")
        self.sqlPsw_Info.grid(row=3, column=1, sticky=W)

        self.sqlDB = Label(frame, text="数据库:")
        self.sqlDB.grid(row=4, column=0, sticky=W)
        self.sqlDB_Info = Entry(frame)
        self.sqlDB_Info.grid(row=4, column=1, sticky=W)

        self.button = Button(frame, text="登录", command=self.Submit)
        self.button.grid(row=5, column=1, sticky=E)

        self.sqlLogin_Info = Label(frame, text="计数")
        self.sqlLogin_Info.grid(row=7, column=0, sticky=W)

        self.button2 = Button(frame, text="退出", command=frame.quit)
        self.button2.grid(row=6, column=3, sticky=E)

    def Save_Count_Info(self, HOST, PORT, USER, PASSWD):
        f.open("C:/config_info.txt", 'w')
        f.write("%s %s %s %s", (HOST, PORT, USER, PASSWD))
        f.close()

    def Submit(self):
        fc.HOST = self.sqlAddress_Info.get()
        fc.PORT = int(self.sqlPin_Info.get())
        fc.USER = self.sqlName_Info.get()
        fc.PASSWD = self.sqlPsw_Info.get()
        fc.DB = self.sqlDB_Info.get()


        # if USER == 'admin' and USER == '123':
        #     self.sqlLogin_Info["text"] = "登陆成功"
        # else:
        #     self.sqlLogin_Info["text"] = "用户名或密码错误!"
        # # self.ent1.delete(0, len(s1))
        # # self.ent2.delete(0, len(s2))
        # if HOST == '1':
        #     tkinter.messagebox.showerror('错误', '数据库出错')
        # elif HOST == '2':
        #     tkinter.messagebox.showerror('错误', '出错了')
        # else:
        #     Save_Count_Info(HOST, PORT, USER, PASSWD)
def Submit():
    try:
        fc.HOST = sqlAddress_Info.get()
        fc.PORT = int(sqlPin_Info.get())
        fc.USER = sqlName_Info.get()
        fc.PASSWD = sqlPsw_Info.get()
        fc.DB = sqlDB_Info.get()
        main(fc.HOST, fc.PORT, fc.USER, fc.PASSWD, fc.DB)
    except ValueError:
        tkinter.messagebox.showerror('you are wrong', '请输入完整信息，不能为空')

def SetGui(master):
    global sqlAddress_Info
    global sqlPin_Info
    global sqlName_Info
    global sqlPsw_Info
    global sqlDB_Info
    global sqlShow_Info
    frame = Frame(master)
    frame.pack()
    fp = open("D:\config_c.txt", 'a')
    fp.close()
    file_object = open('D:\config_c.txt','r')
    try:
        textLines = file_object.readlines()
        if len(textLines)>1:
            HOST = textLines[0]
            PORT = textLines[1]
            USER = textLines[2]
            PASSWD = textLines[3]
            DB = textLines[4]
        else:
            HOST = ''
            PORT = ''
            USER = ''
            PASSWD = ''
            DB = ''
    finally:
        file_object.close()
    sqlAddress = Label(frame, text="主机地址:")
    sqlAddress.grid(row=0, column=0, sticky=W)
    a = StringVar()
    sqlAddress_Info = Entry(frame,textvariable = a)
    a.set(HOST)
    sqlAddress_Info.grid(row=0, column=1, sticky=W)

    sqlPin = Label(frame, text="  端  口  :")
    sqlPin.grid(row=1, column=0, sticky=W)
    b = StringVar()
    sqlPin_Info = Entry(frame,textvariable = b)
    b.set(PORT)
    sqlPin_Info.grid(row=1, column=1, sticky=W)

    sqlName = Label(frame, text="  账  户  :")
    sqlName.grid(row=2, column=0, sticky=W)
    c = StringVar()
    sqlName_Info = Entry(frame,textvariable = c)
    c.set(USER)
    sqlName_Info.grid(row=2, column=1, sticky=W)

    sqlPsw = Label(frame, text=" 密  码  :")
    sqlPsw.grid(row=3, column=0)
    d = StringVar()
    sqlPsw_Info = Entry(frame, show="*",textvariable = d)
    d.set(PASSWD)
    sqlPsw_Info.grid(row=3, column=1, sticky=W)

    sqlDB = Label(frame, text="数 据 库 :")
    sqlDB.grid(row=4, column=0, sticky=W)
    e = StringVar()
    sqlDB_Info = Entry(frame,textvariable = e)
    e.set(DB)
    sqlDB_Info.grid(row=4, column=1, sticky=W)

    button = Button(frame, text=" 登 录 ", command=Submit)
    button.grid(row=5, column=1, sticky=E)

    sqlShow_Info = Label(frame, text= "")
    sqlShow_Info.grid(row=5, column=0, sticky=W)

    button2 = Button(frame, text=" 退 出 ", command=frame.quit)
    button2.grid(row=6, column=3, sticky=E)
global root
root = Tk()
root.title("商品上传系统")
# app = Reg(root)
SetGui(root)
root.mainloop()
# if CheckSupplierRepeat():
#     print('该店铺已经存在，继续执行下一条指令')
# else:
#     print('开始添加店铺')
#绑定会员与商店
# BindUserSupplier()
#添加商品
# AddGoods()
#每次成功执行一次操作输出一次信息，给以互动

# rowNums = CURSOR.execute('SELECT * FROM ecs_supplier')
#         print('查询的总条数' + str(rowNums))
#
#         selectResultList = CURSOR.fetchall()
#         print(type(selectResultList[0]))
#         for i in range(len(selectResultList)):
#             print(selectResultList[i])