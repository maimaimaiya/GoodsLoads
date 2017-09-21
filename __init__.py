import Function as fc
def OutputInfo(index,type = 0):
    return

def main():
    # 用户输入信息 函数
    fc.InputInfo()
    # 登录数据库
    if fc.DbLogin():
        #查询客户数据库 获取对应信息 函数 FindDBInfo()#得到一个数据库商品列表 INFOLIST_C
        if fc.FindDBInfo():
            #提取出数据库已有的每一条商品信息
            for i in range(2):#range(len(fc.INFOLIST_C)):
                fc.GOODS_SN = fc.INFOLIST_C[i][0] #货品编号
                fc.ADD_TIME = fc.INFOLIST_C[i][1] #添加时间
                fc.GOODS_DESC = b'<P>' + fc.INFOLIST_C[i][2] + b'</p>' #商品详情
                fc.GOODS_NAME = fc.INFOLIST_C[i][2] #商品名称
                fc.SUPPLIER_NAME = fc.INFOLIST_C[i][3] #店铺名称
                fc.USER_NAME = fc.INFOLIST_C[i][4] #入驻商账号  入驻商备注

                #检查该商品是否重复，重复则跳过 True 则重复
                if fc.CheckGoodsRepeat():
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

                #开始添加商品
                fc.AddGoods()
                #建立店铺分类
                fc.AddSupplierCategory()
                #商品与店铺绑定
                fc.BindCatGoods()
                #开始添加图片

        #数据库数据提交 与 关闭
        fc.DbClose()
    else:
        #登录数据库失败处理
        return False
main()


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