import time,Dao

class view:

    def __init__(self):
        self.dao =  Dao.Dao()

    def str_dou_count(self,str):
        count = 0
        for s in str:
            if '\u4e00' <= s <= '\u9fff':
                count += 1
        return count

    def press_to_continue(self):
        key = input("\t\t\t\t\t\t\t\t\t键入Enter以继续...")

    def show_title(self):
        print("\n")
        print("+-----------------------------------------------------------------------------------+")
        print("|\tPower By 刘禹辰\t\tStudent Number 1814010603\t\tSystem Name 股票分析工具v1.0\t|")
        print("|\t\t\t\t\t\t\t\t适用群体\t\t中长线股民\t\t\t\t\t\t\t\t|")
        print("|\t\t\t\t\t\t" + time.strftime("%Z %Y年%m月%d日 %H时%M分%S秒") + "\t\t\t\t\t\t|")

    def show_menu(self):
        self.show_title()
        print("+===================================================================================+")
        print("|\t\t\t\t\t\t\t\t\t\t主菜单\t\t\t\t\t\t\t\t\t\t|")
        print("+-----------------------------------------------------------------------------------+")
        print("|\t\tn\t从网络获取数据\t\t|\t\tl\t使用现有数据\t\t|\t\tq\t退出\t\t|")
        print("+-----------------------------------------------------------------------------------+")

    def show_opp(self):
        self.show_title()
        print("+===================================================================================+")
        print("|\t\t\t\t\t\t\t\t\t\t操作\t\t\t\t\t\t\t\t\t\t|")
        print("+-----------------------------------------------------------------------------------+")
        print("|\t\t\tc\t查看所有基金公司\t\t\t|\t\t\t\tf\t查看所有基金\t\t\t\t|")
        print("|\t\t\ti\t导入现有数据\t\t\t\t|\t\t\t\te\t导出为文件\t\t\t\t|")
        print("|\t\t\ta\t分析现有基金数据\t\t\t|\t\t\t\tq\t返回上一级菜单\t\t\t|")
        print("+-----------------------------------------------------------------------------------+")

    def show_company(self):
        self.show_title()
        print("+===================================================================================+")
        print("|\t\t\t\t\t\t\t\t\t\t基金公司\t\t\t\t\t\t\t\t\t\t|")
        print("+-----------------------------------------------------------------------------------+")
        print("|\t\t公司ID\t\t\t\t公司名称\t\t\t|\t公司ID\t\t\t\t公司名称\t\t\t|")
        print("+-----------------------------------------------------------------------------------+")
        result = self.dao.get_company()
        row = 2
        num = self.dao.get_company_num()
        line = int(num / row)
        if (num % row != 0):
            line += 1
        for i in range(0,line):
            print("|\t", end="")
            for j in range(0,row):
                if(i * row + j >= num):
                    print("\t\t\t\t\t\t\t\t\t\t|", end="")
                elif (len(result[i * row + j][1]) > 5):
                    print("\t%s\t\t\t%s\t|" % (result[i * row + j][0],result[i * row + j][1]), end="")
                elif (len(result[i * row + j][1]) > 4):
                    print("\t%s\t\t\t%s\t\t|" % (result[i * row + j][0],result[i * row + j][1]), end="")
                else:
                    print("\t%s\t\t\t%s\t\t\t|" % (result[i * row + j][0],result[i * row + j][1]), end="")
            print("")
        print("+-----------------------------------------------------------------------------------+")
        self.press_to_continue()

    def show_fund(self):
        self.show_title()
        print("+===================================================================================+")
        print("|\t\t\t\t\t\t\t\t\t\t基金\t\t\t\t\t\t\t\t\t\t|")
        print("+-----------------------------------------------------------------------------------+")
        print("|\t\t基金ID\t\t\t\t基金名称\t\t\t|\t基金ID\t\t\t\t基金名称\t\t\t|")
        print("+-----------------------------------------------------------------------------------+")
        result = self.dao.get_fund()
        row = 2
        num = self.dao.get_fund_num()
        line = int(num / row)
        if (num % row != 0):
            line += 1
        for i in range(0,line):
            print("|\t", end="")
            for j in range(0,row):
                if(i * row + j >= num):
                    print("\t\t\t\t\t\t\t\t\t\t|", end="")
                else:
                    fund_name = result[i * row + j][1]
                    count = self.str_dou_count(fund_name)
                    if(count > 12):
                        print("\t%s\t%14s\t|" % (result[i * row + j][0],fund_name), end="")
                    elif(count > 7):
                        print("\t%s\t%14s\t\t|" % (result[i * row + j][0],fund_name), end="")
                    else:
                        print("\t%s\t%14s\t\t\t|" % (result[i * row + j][0],fund_name), end="")
            print("")
        print("+-----------------------------------------------------------------------------------+")
        self.press_to_continue()

    def show_analyse(self, item, result):
        if(item > len(result)):
            item = len(result)
        self.show_title()
        print("+===================================================================================+")
        print("|\t\t\t\t\t\t\t\t\t\t分析结果\t\t\t\t\t\t\t\t\t\t|")
        print("+-----------------------------------------------------------------------------------+")
        print("|\t排名\t|\t\t\t股票名称\t\t\t|\t\t\t股票代码\t\t\t|\t持仓基金数\t|")
        print("+-----------------------------------------------------------------------------------+")
        for i in range(0, item):
            print("|\t%d\t\t|\t\t\t%s\t\t\t\t\t\t%s\t\t\t\t\t%d\t\t|" % (i + 1, result[i]["name"], result[i]["id"], result[i]["count"]) )
        print("+-----------------------------------------------------------------------------------+")
        self.press_to_continue()

    def show_export(self):
        self.show_title()
        print("+===================================================================================+")
        print("|\t\t\t\t\t\t\t\t\t\t导出\t\t\t\t\t\t\t\t\t\t|")
        print("+-----------------------------------------------------------------------------------+")
        print("|\t\tc\t导出基金公司\t\t|\t\t\tf\t导出基金\t\t\t|\t\tq\t返回\t\t|")
        print("+-----------------------------------------------------------------------------------+")

    def show_get_info(self):
        self.show_title()
        print("+===================================================================================+")
        print("|\t\t\t\t\t\t\t\t\t\t网络获取\t\t\t\t\t\t\t\t\t\t|")
        print("+-----------------------------------------------------------------------------------+")
        print("|\t\tc\t获取基金公司\t\t|\t\t\tf\t获取基金\t\t\t|\t\tq\t返回\t\t|")
        print("+-----------------------------------------------------------------------------------+")

    def __del__(self):
        del self.dao