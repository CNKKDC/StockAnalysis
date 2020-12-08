import pymysql

class Dao:

    URL = "127.0.0.1"
    USERNAME = "root"
    PASSWORD = "liu21436587"
    DATABASE = "fund"

    def __init__(self):
        self.db = pymysql.connect(self.URL, self.USERNAME, self.PASSWORD, self.DATABASE)
        self.cursor = self.db.cursor()

    def create_fund_company_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS company")
        self.cursor.execute("CREATE TABLE company (company_id CHAR(8) NOT NULL PRIMARY KEY, company_name CHAR(128) NOT NULL)")

    def insert_company(self, companyInfo):
        try:
            self.cursor.execute("INSERT INTO company (company_id, company_name) VALUES ('%s','%s')" % companyInfo)
            self.db.commit()
        except:
            self.db.rollback()

    def delete_company(self, companyId):
        try:
            self.cursor.execute("DELETE FROM company WHERE company_id = %s" % companyId)
            self.db.commit()
        except:
            self.db.rollback()

    def get_company(self, companyId="0"):
        sql = ""
        if(companyId == "0"):
            sql = "SELECT * FROM company"
        else:
            sql = "SELECT * FROM company WHERE company_id = %s" % companyId
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except:
            print("Error: unable to fetch data")

    def get_company_num(self):
        sql = "SELECT COUNT(company_id) FROM company"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results[0][0]
        except:
            print("Error: unable to fetch data")

    def create_fund_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS fund_list")
        self.cursor.execute("CREATE TABLE fund_list (fund_id CHAR(16) NOT NULL PRIMARY KEY, fund_name CHAR(128) NOT NULL, fund_rate_for_current_year double , company_id CHAR(8) NOT NULL)")

    def insert_fund(self, fund_info):
        try:
            self.cursor.execute("INSERT INTO fund_list (fund_id, fund_name,fund_rate_for_current_year, company_id) VALUES ('%s','%s', %s, %s)" % fund_info)
            self.db.commit()
        except:
            self.db.rollback()

    def get_fund_num(self):
        sql = "SELECT COUNT(fund_id) FROM fund_list"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results[0][0]
        except:
            print("Error: unable to fetch data")

    def get_fund(self, fundId="0"):
        sql = ""
        if(fundId == "0"):
            sql = "SELECT * FROM fund_list"
        else:
            sql = "SELECT * FROM fund_list WHERE company_id = %s" % fundId
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except:
            print("Error: unable to fetch data")

    def get_no_fund_company(self):
        sql = "SELECT * FROM company WHERE company_id NOT IN(SELECT company_id FROM fund_list GROUP BY company_id)"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except:
            print("Error: unable to fetch data")

    def get_no_rate_fund(self):
        sql = "SELECT * FROM fund_list WHERE fund_rate_for_current_year IS NULL"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except:
            print("Error: unable to fetch data")


    def __del__(self):
        self.db.close()
