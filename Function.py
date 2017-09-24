import pymysql

# 全局变量名存储
global GOODS_SN  # -> 商品货号
global GOODS_NAME  # -> 商品名称
global GOODS_DESC  # -> 商品详情
global GOODS_THUMB  # -> 商品缩略图
global GOODS_IMG  # -> 商品图
global ORGINAL_IMG  # -> 原始图像
global ADD_TIME  # -> unix时间戳
global SUPPLIER_ID  # -> 店铺ID（当前商品属于哪个店铺
global USER_NAME  # 入驻商账号名
global USER_ID  # UID 入驻商账号ID
global SUPPLIER_NAME  # 店铺名字
global GOODS_ID  # 添加商品图片 用
global CAT_ID  #店铺内 分类ID

global CONN  # 数据库连接
global CURSOR  # 数据库游标

global HOST  # 主机地址
global USER  # 用户名
global PORT  # 端口
global PASSWD  # 用户密码
global DB  # 连接数据库

# 客户数据库连接，便于调取数据
global CONN_C  # 数据库连接 客户
global CURSOR_C  # 数据库游标 客户
global HOST_C  # 主机地址
global USER_C  # 用户名
global PORT_C  # 端口
global PASSWD_C  # 用户密码
global DB_C  # 连接数据库

global INFOLIST_C  # 客户数据库 的信息列表
global IMGLIST_C #客户数据库的图片列表


def InputInfo(host,port,user,passwd,db):
    return
    #存入文件，若文件不为空，则可以直接填充，否则提醒输入
    # global HOST  # 主机地址
    # global USER  # 用户名
    # global PORT  # 端口
    # global PASSWD  # 用户密码
    # global DB  # 连接数据库
    # HOST = input("请输入您的 主机地址：\n")
    # PORT = input("请输入您的 端口：\n")
    # PORT = int(PORT)
    # USER = input("请输入您的 用户名：\n")
    # PASSWD = input("请输入您的 用户密码：\n")
    # DB = input("请输入您的 数据库名称：\n")

    # 有一个输入的过程
    #HOST = '127.0.0.1'
    #USER = 'root'
    #PORT = 3306
    #PASSWD = '123456'
    #DB = 'db'
	

    # HOST = str(host)
    # USER = str(user)
    # PORT = int(port)
    # PASSWD = str(passwd)
    # DB = str(db)


def DbLogin():
    try:
        global CONN
        CONN = pymysql.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset='utf8')
    except pymysql.OperationalError:
        #连接失败
        ErrorInfo(1001)
        return False
    else:
        #连接成功
        SuccessInfo(200)
        file_object = open('D:\config_c.txt', 'w')
        try:
            textLines = file_object.writelines(HOST + ' ' + str(PORT) + ' ' + USER + ' ' + PASSWD + ' ' + DB)
        finally:
            file_object.close()
        #获取游标
        global CURSOR
        CURSOR = CONN.cursor()
    return True

#数据库关闭连接
def DbClose():
    global CONN
    global CURSOR
    CONN.commit()
    CURSOR.close()
    CONN.close()

#确定supplier_id 和 user_id，便于直接绑定
def DefineID(index=1):
    global SUPPLIER_ID
    global USER_ID
    global CURSOR
    #需要创建店铺，尽心查询
    if index:
        #确定 SUPPLIER_ID
        CURSOR.execute('SELECT MAX(supplier_id) FROM ecs_supplier')
        selectResultList = CURSOR.fetchall()
        # print (rownum)
        # if (rownum == 1):
        #     SUPPLIER_ID = ''
        # else:
        print (selectResultList[0][0])
        if (selectResultList[0][0] == None):
            SUPPLIER_ID = 0
        else:
            SUPPLIER_ID = selectResultList[0][0] + 1
        #确定 USER_ID  在原有基础上自加 1
        CURSOR.execute('SELECT MAX(uid) FROM ecs_supplier_admin_user')
        selectResultList = CURSOR.fetchall()
        # if (rownum == 1):
        #     USER_ID = 2
        # else:
        print (selectResultList[0][0])
        if (selectResultList[0][0] == None):
            USER_ID = 0
        else:
            USER_ID = selectResultList[0][0] + 1
    else:
        # 确定 SUPPLIER_ID
        CURSOR.execute('SELECT supplier_id FROM ecs_supplier WHERE supplier_name = %s', (SUPPLIER_NAME))
        selectResultList = CURSOR.fetchall()
        SUPPLIER_ID = selectResultList[0][0]

global URL_MMP
URL_MMP = 'http://yy.xx2018.cn/使用说明.txt'

#检查商品重复
def CheckGoodsRepeat():
    global CURSOR
    rowNums = CURSOR.execute('SELECT goods_sn FROM ecs_goods WHERE goods_sn = %s', (GOODS_SN))
    if rowNums:
        return True
    #??商品查重有问题 不能用名字查询 一个bytes 一个 str
    rowNums = CURSOR.execute('SELECT goods_name FROM ecs_goods WHERE goods_name = %s',(GOODS_NAME))
    if rowNums:
        return True # 重复
    return False # 没有重复

#获取所需要的所有信息
def getAllInfo():
    return

#检查店铺重复  店铺是否存在
def CheckSupplierRepeat():
    global CURSOR
    rowNums = CURSOR.execute('SELECT supplier_name FROM ecs_supplier WHERE supplier_name = %s',(SUPPLIER_NAME))
    # print('店铺查询的总条数' + str(rowNums))
    if rowNums:
        return True
    return False

#增加商品
def AddGoods():
    global GOODS_THUMB #-> 商品缩略图
    global GOODS_IMG  # -> 商品图
    global ORGINAL_IMG  #-> 原始图像
    global GOODS_ID
    global CURSOR
    if len(IMGLIST_C) > 0:
        GOODS_THUMB = IMGLIST_C[0][0] # -> 商品缩略图
    else:
        GOODS_THUMB = ''
    GOODS_IMG = ''# -> 商品图
    ORGINAL_IMG = '' # -> 原始图像

    sql = '''INSERT INTO `ecs_goods` VALUES ('', '2', %s, %s, '+', '2', '0', '', '9999', '0.000', '0.00',
     '0.00', '0.00', '0', '0', '0', '0', '0', '0', '1', '服装,服饰', '服装服饰批发，库存尾货大全', %s,  %s, %s, %s , '1',
       '', '1', '1', '0', '0', %s, '100', '0', '1', '1', '1', '0', '10.0', '0', %s,
       '2', '', '-1', '-1', '', %s, '1', '', '', '0', '0.00', '', '0')'''
    CURSOR.execute(sql, (GOODS_SN, GOODS_NAME, GOODS_DESC,GOODS_THUMB,GOODS_IMG,ORGINAL_IMG,ADD_TIME,ADD_TIME,SUPPLIER_ID))
    #获取GOODS_ID
    CURSOR.execute('SELECT MAX(goods_id) FROM ecs_goods')
    goodList = CURSOR.fetchall()
    GOODS_ID = goodList[0][0]



#创建店铺
def CreateSupplier():
    global CURSOR
    # CURSOR.execute('''INSERT INTO `ecs_supplier` VALUES (%s, %s, %s, '3', '2', %s, '1', '10', '145', '1195', '冰河路',
    #           '18620241959', 'mmp@mmp.com', '', '', '', '', '', '', '', '', '', '', '',
    #           '', '0.00', '0.00', '0', '2', '', '', '1', %s, '3', '123456', '18620241959',
    #            '', '', '', '', '', '123456', '123456', '123456', '123456', '', '', '', '', '',
    #             '', '', '', '0.00', '', '', '', '')''',(SUPPLIER_ID,USER_ID,SUPPLIER_NAME,SUPPLIER_NAME,ADD_TIME))
    CURSOR.execute('''INSERT INTO `ecs_supplier` VALUES ('', %s, %s, '3', '2', %s, '1', '10', '145', '1195', '冰河路', 
                 '18620241959', 'mmp@mmp.com', '', '', '', '', '', '', '', '', '', '', '', 
                 '', '0.00', '0.00', '0', '2', '', '', '1', %s, '3', '123456', '18620241959',
                  '', '', '', '', '', '123456', '123456', '123456', '123456', '', '', '', '', '',
                   '', '', '', '0.00', '', '', '', '')''',
                   ( USER_ID, SUPPLIER_NAME, SUPPLIER_NAME, ADD_TIME))
#绑定会员与商店
def BindUserSupplier():
    global CURSOR
    sql = '''INSERT INTO `ecs_supplier_admin_user` VALUES ('', %s, %s, 'xxx@xxx.com','', 'e10adc3949ba59abbe56e057f20f883e', '', '1437497970', '1443601087', '110.211.206.143', 'all','', '', '0', %s, '', '0', '1')'''
    CURSOR.execute(sql,(USER_ID,USER_NAME,SUPPLIER_ID))

#装修店铺
def DecorationSupplier():
    global CURSOR
    mySqlLists = ["INSERT INTO `ecs_supplier_shop_config` VALUES ('1', '0', 'shop_info', 'group', '', '', '', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('2', '0', 'hidden', 'hidden', '', '', '', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('8', '0', 'sms', 'group', '', '', '', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('103', '1', 'shop_desc', 'hidden', '', '', '商家店铺描述', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('104', '1', 'shop_keywords', 'text', '', '', '服装', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('105', '1', 'shop_country', 'manual', '', '', '1', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('106', '1', 'shop_province', 'manual', '', '', '2', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('107', '1', 'shop_city', 'manual', '', '', '52', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('108', '1', 'shop_address', 'text', '', '', '西城区', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('109', '1', 'qq', 'text', '', '', '2602447159', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('110', '1', 'ww', 'text', '', '', '18620241959', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('111', '1', 'skype', 'hidden', '', '', '', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('112', '1', 'ym', 'hidden', '', '', '', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('113', '1', 'msn', 'hidden', '', '', '', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('114', '1', 'service_email', 'text', '', '', '', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('115', '1', 'service_phone', 'text', '', '', '18620241959', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('116', '1', 'shop_closed', 'select', '0,1', '', '0', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('117', '1', 'close_comment', 'hidden', '', '', '', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('118', '1', 'shop_logo', 'file', '', '../themes/{$template}/images/', '/data/supplier/logo/logo_supplier5.jpg', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('119', '1', 'licensed', 'hidden', '0,1', '', '1', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('120', '1', 'user_notice', 'hidden', '', '', '用户中心公告！', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('121', '1', 'shop_notice', 'textarea', '', '', '商家店铺介绍:欢迎光临,我们的宗旨：诚信经营、服务客户！\r\n<MARQUEE onmouseover=this.stop() onmouseout=this.start() \r\nscrollAmount=3><U><FONT color=red>\r\n<P>咨询电话: 18620241959</P></FONT></U></MARQUEE>', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('122', '1', 'shop_reg_closed', 'hidden', '1,0', '', '0', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('123', '1', 'shop_index_num', 'textarea', '', '', '5\r\n4\r\n4', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('124', '1', 'shop_search_price', 'textarea', '', '', '0-1000元\r\n1000-2000元\r\n2000-4000元', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('125', '1', 'close_comment', 'textarea', '', '', '该店铺正在装修', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('201', '2', 'shop_header_color', 'hidden', '', '', '#FF7197', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('202', '2', 'shop_header_text', 'hidden', '', '', '<p style=\"text-align: center;\"><img src=\"bdimages/upload1/20150722/1437533899487593.gif\" title=\"TB2qKLRdFXXXXaRXXXXXXXXXXXX_!!94395476.gif\"/></p>', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('203', '2', 'template', 'hidden', '', '', 'dianpu6', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('204', '2', 'stylename', 'hidden', '', '', '', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('205', '2', 'flash_theme', 'hidden', '', '', 'leilei5', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('801', '8', 'sms_shop_mobile', 'text', '', '', '', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('802', '8', 'sms_order_placed', 'select', '1,0', '', '0', '0', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('803', '8', 'sms_order_payed', 'select', '1,0', '', '0', '1', %s)",
"INSERT INTO `ecs_supplier_shop_config` VALUES ('804', '8', 'sms_order_shipped', 'select', '1,0', '', '0', '1', %s)"]
    for sql in mySqlLists:
        CURSOR.execute(sql,(SUPPLIER_ID))
    CURSOR.execute("INSERT INTO `ecs_supplier_shop_config` VALUES ('101', '1', 'shop_name', 'text', '', '', %s, '1', %s)",(SUPPLIER_NAME,SUPPLIER_ID))
    CURSOR.execute("INSERT INTO `ecs_supplier_shop_config` VALUES ('102', '1', 'shop_title', 'text', '', '', %s, '1', %s)",
        (SUPPLIER_NAME, SUPPLIER_ID))

#添加店铺分类 并 确定CAT_ID
def AddSupplierCategory():
    global CURSOR
    global CAT_ID
    #判断该店铺是否含有分类
    rowNums = CURSOR.execute('SELECT cat_id FROM ecs_supplier_category WHERE supplier_id = %s',(SUPPLIER_ID))
    if rowNums:
        catList = CURSOR.fetchall()
        CAT_ID = catList[0][0]
    else:
        # 没有则创建一个分类
        sql = '''INSERT INTO `ecs_supplier_category` VALUES ('', '服装', '', '服装服饰', '0', '50', '', '',
             '1', '', '1', '0', '', %s, '1', '', '', '8')'''
        CURSOR.execute(sql, (SUPPLIER_ID))
        #查找cat_id
        CURSOR.execute('SELECT cat_id FROM ecs_supplier_category WHERE supplier_id = %s', (SUPPLIER_ID))
        catList = CURSOR.fetchall()
        CAT_ID = catList[0][0]

# 绑定分类与商品
def BindCatGoods():
    global CURSOR
    sql = '''INSERT INTO `ecs_supplier_goods_cat` VALUES (%s, %s, %s)'''
    CURSOR.execute(sql, (GOODS_ID, CAT_ID, SUPPLIER_ID))


# 添加图片
def AddGoodsImg():
    global CURSOR
    for img_url in IMGLIST_C:
        CURSOR.execute("INSERT INTO `ecs_goods_gallery` VALUES ('', %s, %s, '', %s, %s, '0', '0', '0')",(GOODS_ID,img_url[0],img_url[0],img_url[0]))

#查询客户的数据库信息
def FindDBInfo():
    global CONN_C  # 数据库连接 客户
    global CURSOR_C  # 数据库游标 客户
    global HOST_C  # 主机地址
    global USER_C  # 用户名
    global PORT_C  # 端口
    global PASSWD_C  # 用户密码
    global DB_C  # 连接数据库
    global INFOLIST_C  # 客户数据库 的信息列表

    try:
        CONN_C = pymysql.connect(host='42.51.41.149', port=3306, user='root', passwd='qycloud', db='sns', charset='utf8')
        # 获取游标
        global CURSOR_C
        CURSOR_C = CONN_C.cursor()

        rowNums = CURSOR_C.execute('SELECT sns_id,timestamp,content,author_name,author_id,media_count FROM tween_')
        print('查询对象数据库 商品数据  ' + str(rowNums) + '  条')
        INFOLIST_C = CURSOR_C.fetchall()

    except pymysql.OperationalError:
        #连接失败
        ErrorInfo(2001)
        return False
    except pymysql.ProgrammingError:
        #查询的表不存在
        ErrorInfo(2002)
        return False
    else:
        # 连接成功

        SuccessInfo(400)
    return True

def FindImgInfo():
    global CURSOR_C  # 数据库游标 客户
    global IMGLIST_C
    rowNums = CURSOR_C.execute('SELECT url FROM media_ WHERE sns_id = %s',(GOODS_SN))
    print('查询对象数据库 商品数据  ' + str(rowNums) + '  条')
    IMGLIST_C = CURSOR_C.fetchall()

#错误输出信息
def ErrorInfo(index):
    if index == 1001:
        print("code 1001: 连接数据库失败，请检查您的主机地址和账号密码")
    elif index == 2001:
        print("code 2001: 对象数据库连接失败，请检查您的网络或主机")
    elif index == 2002:
        print("code 2002: 对象数据库表不存在，可联系开发人员进行修改")

#成功时输出信息
def SuccessInfo(index):
    if (index == 200):
        print("code 200: 数据库连接成功")
    elif index == 400:
        print("code 400: 对象数据库连接成功")



