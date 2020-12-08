import requests,bs4,re,view,BackupIO
import Dao

FUND_COMPANY_LIST_URL = "http://fund.eastmoney.com/company/default.html"
FUND_LIST_URL = "http://fund.eastmoney.com/Company/home/KFSFundNet?gsid={{companyId}}"
FUND_HOLD_URL = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={{fundId}}&topline=3&year=&month="
FUND_RATE_URL = "http://fund.eastmoney.com/pingzhongdata/{{fundId}}.js"
STOCK_FUND = "股票型"
STOCK_INDEX_FUND = "股票指数"
PURCHASABLE = "开放申购"

class Fund:

    fundNum = 0
    companyList=[]

    def __init__(self):
        self.mysql = Dao.Dao()

    def insertionSort(self, nums):
        for i in range(len(nums) - 1):
            curNum, preIndex = nums[i + 1], i
            while preIndex >= 0 and curNum["mark"] > nums[preIndex]["mark"]:
                nums[preIndex + 1] = nums[preIndex]
                preIndex -= 1
            nums[preIndex + 1] = curNum
        return nums

    def get_company_list(self):
        self.mysql.create_fund_company_table()
        r = requests.get(FUND_COMPANY_LIST_URL)
        r.encoding = "utf-8"
        all_company = bs4.BeautifulSoup(r.text, "lxml").find("div", "sencond-block").find_all("a")
        postion = 1
        allNum = len(all_company)
        for i in all_company:
            print("\r\t\t正在获取证券公司 : %6.2f%%\t%s" % (postion / allNum * 100, i.string) , end="")
            self.mysql.insert_company(companyInfo = (re.search('\d{8}', i['href']).group(0), i.string))
            postion += 1

    def get_company_fund_list(self):
        self.mysql.create_fund_table()
        num = self.mysql.get_company_num()
        companyPostion = 0
        for i in self.mysql.get_company():
            companyPostion += 1
            r = requests.get( FUND_LIST_URL.replace("{{companyId}}", i[0]) )
            r.encoding = "utf-8"
            all_fund = bs4.BeautifulSoup(r.text, "lxml").find("tbody").find_all("tr")
            all_fund_num = len(all_fund)
            fundPostion = 0
            for j in all_fund:
                fundPostion += 1
                col = j.find_all("td")
                if( str(col[0].string) == "暂无数据"):
                    break
                if( ( (str(col[2].string) == STOCK_FUND) | (str(col[2].string) == STOCK_INDEX_FUND) ) & (str(col[11].string) == PURCHASABLE) ):
                    fund_name = col[0].find("a", "name").string
                    fund_id = col[0].find("a", "code").string
                    print("\r\t\t正在获取所有开放申购的股票/指数型基金 : %5.2f%%\t%s" % ((100 / num) * companyPostion + 100 / num / all_fund_num * fundPostion, fund_name) , end="")
                    ri = requests.get( FUND_RATE_URL.replace("{{fundId}}", fund_id) )
                    ri.encoding = 'utf-8'
                    temp = ri.text[(ri.text.find("var syl_1n=\"") + len("var syl_1n=\"")) :]
                    temp = temp[0 : temp.find("\"")]
                    # print(temp)
                    if (temp != ""):
                        self.mysql.insert_fund( (fund_id,  fund_name, temp, i[0]) )
        print("\r\t\t正在删除没有开放申购的股票/指数型基金的公司...\t\t\t\t\t\t\t\t\t", end="")
        for i in self.mysql.get_no_fund_company():
            self.mysql.delete_company(i[0])
        print("\r    ")

    def result_already_have(self, id):
        postion = 0
        for i in self.result:
            if( i["id"] == id):
                return postion
            postion += 1
        return -1

    def analyse_data(self):
        self.result = []
        p = self.mysql.get_fund_num()
        poccess = 1
        for i in self.mysql.get_fund():
            ple = 1
            mark = 1
            print("\r\t\t正在收集分析持仓比例以及基金近一年收益 : %5.2f%%" % (poccess / p * 100), end="")
            if(i[2] > 100):
                ple = 2
            elif(i[2] > 50):
                ple = 1.5
            elif(i[2] >20):
                ple = 0.2
            elif(i[2] < 0):
                ple = -1
            else:
                ple = 0
            tbody = None
            while(True):
                r = requests.get(FUND_HOLD_URL.replace("{{fundId}}", i[0]))
                r.encoding = 'utf-8'
                tbody = bs4.BeautifulSoup(r.text, "lxml").find("tbody")
                if(tbody != None):
                    break
            tr = tbody.find_all("tr")
            for j in tr:
                td = j.find_all("td")
                id = td[1].get_text().strip()
                name = td[2].get_text().strip()
                postion = self.result_already_have(id)
                if(postion != -1):
                    self.result[postion]["mark"] += ple * mark
                    self.result[postion]["count"] += 1
                else:
                    self.result.append({"id": id, "name": name, "mark": ple * mark, "count": 1})
            poccess += 1
        print("\r\t\t整理中...", end="")
        self.insertionSort(self.result)

if __name__ == '__main__':
    fund = Fund()
    view = view.view()
    back = BackupIO.backup()
    while(True):
        view.show_menu()
        choose = input("\t\t请输入选项 : ")
        if (choose == "n"):
            while(True):
                view.show_get_info()
                nChoose = input("\t\t请输入选项 : ")
                if(nChoose == "c"):
                    fund.get_company_list()
                elif(nChoose == "f"):
                    fund.get_company_fund_list()
                elif(nChoose == "q"):
                    break
                else:
                    print("\t\t\t\t\t\t\t\t\t请输入正确的选项 ! ")
                    continue
        elif (choose == "l"):
            while(True):
                view.show_opp()
                opChoose = input("\t\t请输入选项 : ")
                if (opChoose == "c"):
                    view.show_company()
                elif (opChoose == "f"):
                    view.show_fund()
                elif (opChoose == "a"):
                    fund.analyse_data()
                    view.show_analyse(int(input("\r\t\t请输入显示条目 : ")), fund.result)
                elif (opChoose == "i"):
                    print("\t\t请选择基金公司备份文件...",end="")
                    if(back.excel2mysql_company() == -1):
                        print("\r\t\t保留基金公司原设置")
                    else:
                        print("\r\t\t基金公司导入成功")
                    print("\t\t请选择基金列表备份文件...", end="")
                    if(back.excel2mysql_fund_list() == -1):
                        print("\r\t\t保留基金列表原设置")
                    else:
                        print("\r\t\t基金列表导入成功")
                elif (opChoose == "e"):
                    view.show_export()
                    exChoose = input("\t\t请输入选项 : ")
                    if(exChoose == "c"):
                        back.mysql2excel("company")
                    elif(exChoose == "f"):
                        back.mysql2excel("fund_list")
                    elif(exChoose == "q"):
                        print("",end="")
                    else:
                        print("\t\t\t\t\t\t\t\t\t输入错误 ! ")
                elif (opChoose == "q"):
                    break
                else:
                    print("\t\t\t\t\t\t\t\t\t请输入正确的选项 ! ")
                    continue
        elif (choose == "q"):
            exit()
        else:
            print("\t\t\t\t\t\t\t\t\t请输入正确的选项 ! ")
            continue
