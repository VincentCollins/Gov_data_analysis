import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sqlite3
import os

class my_spider():
    def __init__(self):
        pass

    def html_process(self,html_text,database,tablename,maindata_type,line,end_year):#html文件处理函数，获取数据信息并建立数据表
        # 连接数据库
        self.my_sq = sqlite3.connect(database)
        self.cursor = self.my_sq.cursor()

        # 处理html文本
        self.bs = BeautifulSoup(html_text, 'lxml')
        self.rows = self.bs.select('table.public_table.table_main tbody tr')  # 获取各行的人口数据
        # 获得的list中的成员就是bs4.element.Tag类型
        self.index_row = self.bs.select('table.public_table.table_main thead tr')  # 虽然只有一行，但仍然装在list里面

        # 建立数据库
        try:
            self.cursor.execute('''DROP TABLE if exists %s'''%tablename)
            self.cursor.execute('''CREATE TABLE %s
                                        (YEAR   INT PRIMARY KEY NOT NULL,
                                         VALUE  %s              NOT NULL);
                                        '''%(tablename,maindata_type))
        except:
            pass

        #写入数据
        for self.i, self.td in enumerate(self.rows[line].contents[1:]):  # 遍历第一行数据，跳过第一行第一个表头数据
            self.year = int(self.index_row[0].contents[self.i + 1].get_text()[0:4])  # 一个年份数据
            if self.year>end_year:#有必要的话，跳过前面的数据（如跳过2018年）
                continue
            if maindata_type=='int':#关键数据是整数，比如人口
                self.value = int(self.td.get_text())
                self.cursor.execute('''INSERT INTO %s(YEAR, VALUE) VALUES('%d','%d')''' % (tablename,self.year, self.value))
            else:                   #关键数据是浮点型，比如GDP
                self.value = float(self.td.get_text())
                self.cursor.execute(
                    '''INSERT INTO %s(YEAR, VALUE) VALUES('%d','%f')''' % (tablename, self.year, self.value))
        self.my_sq.commit()
        self.my_sq.close()

    def table_print(self,tablename):#打印数据表
        self.my_sq = sqlite3.connect('mydb.db')
        self.cursor = self.my_sq.cursor()
        self.items = self.cursor.execute("SELECT YEAR,VALUE from %s"%tablename)

        for self.item in self.items:
            print("YEAR: ",self.item[0],type(self.item[0]))
            print("VALUE: ",self.item[1],type(self.item[1]),'\n')

    def task0(self,html_text):#获得及处理农村消费情况信息
        self.html_process(html_text, 'mydb.db', 'OVERALL', 'float', 0, 2012)
        self.html_process(html_text, 'mydb.db', 'FOOD', 'float', 1, 2012)
        self.html_process(html_text, 'mydb.db', 'CLOTHING', 'float', 2, 2012)
        self.html_process(html_text, 'mydb.db', 'ACCOMODATION', 'float', 3, 2012)
        self.html_process(html_text, 'mydb.db', 'TRANSPORTATION', 'float', 5, 2012)
        self.html_process(html_text, 'mydb.db', 'EDU_ENTERTAINMENT', 'float', 6, 2012)

    def task1(self,html_text):#获得及处理三个总人口数据
        self.html_process(html_text,'mydb.db','TOTALPOP','int',0,2018)
        self.html_process(html_text, 'mydb.db', 'MALEPOP', 'int', 1,2018)
        self.html_process(html_text, 'mydb.db', 'FEMALEPOP', 'int', 2,2018)

    def task2(self,html_text):#获得及处理年龄分布数据
        self.html_process(html_text, 'mydb.db', 'POP_0to14', 'int', 1,2017)
        self.html_process(html_text, 'mydb.db', 'POP_15to64', 'int', 2,2017)
        self.html_process(html_text, 'mydb.db', 'POP_65plus', 'int', 3,2017)

    def task3(self,html_text):#获得及处理GDP和三类产业数据
        self.html_process(html_text, 'mydb.db', 'GDP', 'float', 1, 2018)
        self.html_process(html_text, 'mydb.db', 'ASCEND_PI', 'float', 2, 2018)
        self.html_process(html_text, 'mydb.db', 'ASCEND_SI', 'float', 3, 2018)
        self.html_process(html_text, 'mydb.db', 'ASCEND_TI', 'float', 4, 2018)



    def spider_and_get_HTML(self,html_filename,branch1,branch2):#基于selenium模块，动态操作浏览器（执行鼠标点击操作等），并获得html文件
        if not os.path.exists('C:\\Users\Vincent Collins\\git_rep\\dataAnalysis\\%s'%html_filename):
            self.browser = webdriver.Chrome()  # 调用本地的Chrome浏览器
                                               #注意，这一行命令会打开浏览器！
            self.browser.get('http://data.stats.gov.cn/easyquery.htm?cn=C01')  # 请求页面，会打开一个浏览器窗口
            time.sleep(3)
            self.browser.find_element_by_xpath("//span[@id='treeZhiBiao_%d_span']"%branch1).click()
            time.sleep(3)
            self.browser.find_element_by_xpath("//span[@id='treeZhiBiao_%d_span']"%branch2).click()
            time.sleep(3)
            self.browser.find_element_by_xpath("//*[@class='dtHead'][@title='最近10年']").click()
            time.sleep(3)
            self.browser.find_element_by_xpath("//li[@title='最近20年']").click()
            time.sleep(3)

            self.myfile = open(html_filename, 'w')
            self.myfile.write(self.browser.page_source)
            self.myfile.close()

        self.myfile = open(html_filename,'r')
        return self.myfile.read()

    def main_func(self):#总控函数
        self.html_text = self.spider_and_get_HTML('html0.txt', 11, 46)
        self.task0(self.html_text)
        self.html_text = self.spider_and_get_HTML('html1.txt',4,30)
        self.task1(self.html_text)
        self.html_text = self.spider_and_get_HTML('html2.txt', 4, 32)
        self.task2(self.html_text)
        self.html_text = self.spider_and_get_HTML('html3.txt', 3, 30)
        self.task3(self.html_text)

if __name__ =='__main__':
    Spider = my_spider()
    Spider.main_func()

