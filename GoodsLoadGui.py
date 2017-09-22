from tkinter import *
import tkinter.messagebox #这个是消息框，对话框的关键
import Function as fc

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
        self.sqDB.grid(row=4, column=0, sticky=W)
        self.sqlDB_Info = Entry(frame)
        self.sqlDB_Info.grid(row=4, column=1, sticky=W)

        self.button = Button(frame, text="登录", command=self.Submit)
        self.button.grid(row=5, column=1, sticky=E)

        self.sqlLogin_Info = Label(frame, text="")
        self.sqlLogin_Info.grid(row=5, column=0, sticky=W)

        self.button2 = Button(frame, text="退出", command=frame.quit)
        self.button2.grid(row=6, column=3, sticky=E)

    def Save_Count_Info(self,HOST,PORT,USER,PASSWD):
        f.open("C:/config_info.txt",'w')
        f.write("%s %s %s %s",(HOST,PORT,USER,PASSWD))
        f.close()

    def Submit(self):
        fc.HOST = self.sqlAddress_Info.get()
        fc.PORT = self.sqlPin_Info.get()
        fc.USER = self.sqlName_Info.get()
        fc.PASSWD = self.sqlPsw_Info.get()
        fc.DB = self.sqlDB.get()

        # if USER == 'admin' and USER == '123':
        #     self.sqlLogin_Info["text"] = "登陆成功"
        # else:
        #     self.sqlLogin_Info["text"] = "用户名或密码错误!"
        # # self.ent1.delete(0, len(s1))
        # # self.ent2.delete(0, len(s2))
        if HOST == '1':
            tkinter.messagebox.showerror('错误', '数据库出错')
        elif HOST == '2':
            tkinter.messagebox.showerror('错误', '出错了')
        else:
            Save_Count_Info(HOST,PORT,USER,PASSWD)




root = Tk()
root.title("商品上传系统")
app = Reg(root)
root.mainloop()