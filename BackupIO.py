import Dao,xlwt,xlrd,tkinter
from tkinter.filedialog import (askopenfilename, asksaveasfilename)

class backup:

    def __init__(self):
        self.mysql = Dao.Dao();

    def mysql2excel(self, table):
        print("\t\t收集数据中...", end="")
        self.mysql.cursor.execute("select * from %s" % table)
        data_list = self.mysql.cursor.fetchall()
        excel = xlwt.Workbook()
        sheet = excel.add_sheet("sheet1")
        row_number = len(data_list)
        column_number = len(self.mysql.cursor.description)
        for i in range(column_number):
            sheet.write(0,i,self.mysql.cursor.description[i][0])
        for i in range(row_number):
            for j in range(column_number):
                sheet.write(i+1,j,data_list[i][j])
        root = tkinter.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        options = {}
        options['filetypes'] = [('Excel', '.xls')]
        options['initialfile'] = "mysql_{}_backup.xls".format(table)
        dir = asksaveasfilename(**options)
        if(dir == ""):
            return
        excel.save(dir)

    def excel2mysql_fund_list(self):
        root = tkinter.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        options = {}
        options['filetypes'] = [('Excel', '.xls')]
        options['initialfile'] = "mysql_fund_list_backup.xls"
        dir = askopenfilename(**options)
        if(dir == ""):
            return -1
        print("\r\t\t收集导入中...", end="")
        excel = xlrd.open_workbook(dir)
        sheet = excel.sheet_by_index(0)
        row_number = sheet.nrows
        column_number = sheet.ncols
        field_list = sheet.row_values(0)
        data_list = []
        for i in range(1, row_number):
            data_list.append(sheet.row_values(i))
        self.mysql.create_fund_table()
        for data in data_list:
            self.mysql.insert_fund((data[0],data[1],data[2],data[3]))
        return 0

    def excel2mysql_company(self):
        root = tkinter.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        options = {}
        options['filetypes'] = [('Excel', '.xls')]
        options['initialfile'] = "mysql_company_backup.xls"
        dir = askopenfilename(**options)
        if(dir == ""):
            return -1
        print("\r\t\t收集导入中...", end="")
        excel = xlrd.open_workbook(dir)
        sheet = excel.sheet_by_index(0)
        row_number = sheet.nrows
        data_list = []
        for i in range(1, row_number):
            data_list.append(sheet.row_values(i))
        self.mysql.create_fund_company_table()
        for data in data_list:
            self.mysql.insert_company((data[0],data[1]))
        return 0

    def __del__(self):
        del self.mysql