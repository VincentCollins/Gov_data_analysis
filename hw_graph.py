import matplotlib.pyplot as plt
import numpy as np
from dataAnalysis.hw_spider import *
import os
import json
class graphing():
    def __init__(self):
        #存储数据库中数据的变量，每一个index代表一个数据表
        self.data = {'OVERALL':{},'FOOD':{},'CLOTHING':{},'ACCOMODATION':{},'TRANSPORTATION':{},'EDU_ENTERTAINMENT':{},
                     'TOTALPOP':{},'MALEPOP':{},'FEMALEPOP':{},
                     'POP_0to14':{},'POP_15to64':{},'POP_65plus':{},
                     'GDP':{},'ASCEND_PI':{},'ASCEND_SI':{},'ASCEND_TI':{}}


    def spider_and_save(self):#调用爬虫函数，建立数据库
        self.Spider = my_spider()
        self.Spider.main_func()#到此为止已经在数据库中存入所需数据
        pass

    def load_database(self,database):#将数据库中数据录入变量中
        self.my_sq = sqlite3.connect(database)
        self.cursor = self.my_sq.cursor()
        for self.tag in self.data:
            self.items = self.cursor.execute("SELECT year,value from %s" % self.tag)
            for self.item in self.items:
                self.data[self.tag][str(self.item[0])] = self.item[1]

    def create_axis(self,tag):#基于前述的数据字典，将所有数据提取出来，生成numpy需要的array类型
        value = []
        year = []
        for i, item in enumerate(self.data[tag]):
            year.append(int(item))
            value.append(self.data[tag][item])
        return np.array(year),np.array(value)

    def graph0(self):
        # 2000年农村人均消费关于消费类型的分布 饼状图
        labels = ['FOOD','CLOTHING','ACCOMODATION','TRANSPORTATION','EDU_ENTERTAINMENT','OTHERS']
        sizes = []
        explode = [0]
        for i in labels[0:-1]:
            sizes.append(self.data[i]['2000']/self.data['OVERALL']['2000'])
            explode.append(0)
        sizes.append(1-sum(sizes))
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=150)
        plt.title('Cost in diffrent aspects of rural population in 2000')
        plt.savefig('fig7.png', bbox_inches='tight')
        plt.show()

        # 各年龄段占比变化图
        x, y0 = self.create_axis('OVERALL')
        x, y1 = self.create_axis('FOOD')  # 长度跟其他三个不一样！需要截取
        x, y2 = self.create_axis('CLOTHING')
        x, y3 = self.create_axis('ACCOMODATION')
        x, y4 = self.create_axis('TRANSPORTATION')
        plt.plot(x, y1/y0, label='Food')
        plt.plot(x, y2/y0, label='Clothing')
        plt.plot(x, y3/y0, label='Accomodation')
        plt.plot(x, y4/y0, label='Transportation')
        plt.xticks(np.arange(1999, 2013, 1), rotation=60)
        plt.xlabel('Graph. Average cost in four main aspects in rural area vs Year', fontsize=14)
        plt.ylabel('Percentege for several kinds of cost',fontsize=12)
        plt.legend(loc='center left')
        plt.savefig('fig8.png', bbox_inches='tight')
        plt.show()

    def graph1(self):
        # 总人口条形图
        x,y = self.create_axis('TOTALPOP')
        plt.bar(x,y,align='edge',width=0.5,color='darkorange')
        plt.xticks(np.arange(1999,2019,1),rotation=60)
        plt.yticks(np.arange(0,160000,20000))
        plt.xlabel('Graph. Total population vs Year',fontsize=14)
        plt.ylabel('Total population/10^4')
        plt.savefig('fig1.png',bbox_inches = 'tight')
        plt.show()

        #男女性总人口条形图
        x, y1 = self.create_axis('MALEPOP')
        x, y2 = self.create_axis('FEMALEPOP')
        plt.plot(x, y1/(y1 + y2),label='MALE')
        plt.plot(x, y2/(y1 + y2), label='FEMALE')
        plt.xticks(np.arange(1999,2019,1),rotation=60)
        plt.xlabel('Graph. Percentege of population of F&M vs Year', fontsize=14)
        plt.ylabel('Percentege of population')
        plt.legend(loc='center left')
        plt.savefig('fig2.png', bbox_inches='tight')
        plt.show()


    def graph2(self):
        #提取出所需的几个16年数据
        num0 = self.data['TOTALPOP']['2016']
        num1 = self.data['POP_0to14']['2016']
        num2 = self.data['POP_15to64']['2016']
        num3 = self.data['POP_65plus']['2016']

        #2016年各年龄段占比 饼状图
        labels = ['0~14 years old','15~64 years old','over 65 years old']
        sizes = [num1/num0,num2/num0,num3/num0]
        explode = [0,0.1,0]
        plt.pie(sizes, explode=explode,labels= labels,autopct='%1.1f%%',shadow=False,startangle=150)
        plt.title('population propotion for three ranges of age in 2016')
        plt.savefig('fig3.png', bbox_inches='tight')
        plt.show()

        #各年龄段占比变化图
        x, y = self.create_axis('TOTALPOP')#长度跟其他三个不一样
        x, y1 = self.create_axis('POP_0to14')
        x, y2 = self.create_axis('POP_15to64')
        x, y3 = self.create_axis('POP_65plus')
        y1=np.divide(y1,y[0:-1])
        y2=np.divide(y2,y[0:-1])
        y3=np.divide(y3,y[0:-1])
        plt.plot(x, y1, label='0~14(age)')
        plt.plot(x, y2, label='15~64(age)')
        plt.plot(x, y3, label='>65(age)')
        plt.xticks(np.arange(1999, 2018, 1), rotation=60)
        plt.xlabel('Graph. population propotion of three ranges of age vs Year', fontsize=14)
        plt.ylabel('Population propotion')
        plt.legend(loc='center right')
        plt.savefig('fig4.png', bbox_inches='tight')
        plt.show()

    def graph3(self):
        #GDP变化折线图
        x, y = self.create_axis('GDP')
        plt.plot(x, y, label='GDP')
        plt.xticks(np.arange(1999, 2019, 1), rotation=60)
        plt.xlabel('Graph. GDP vs Year', fontsize=14)
        plt.ylabel('GDP/10^8yuan')
        plt.legend(loc='center left')
        plt.savefig('fig5.png', bbox_inches='tight')
        plt.show()

        #三类产业逐年变化条形图
        x, y1 = self.create_axis('ASCEND_PI')
        x, y2 = self.create_axis('ASCEND_SI')
        x, y3 = self.create_axis('ASCEND_TI')
        plt.bar(x[0:10], y1[0:10], align='edge',width=0.2,label='Primary     industry')
        plt.bar(np.add(x,0.2)[0:10], y2[0:10], align='edge',width=0.2,label='Secondary industry')
        plt.bar(np.add(x,0.4)[0:10], y3[0:10], align='edge',width=0.2,label='Tertiary     industry')
        plt.xticks(np.arange(2009, 2019, 1), rotation=60)
        plt.yticks(np.arange(0, 490000, 50000))
        plt.xlabel('Graph. Ascendence of three types of industry vs Year', fontsize=14)
        plt.ylabel('Ascendence/10^8')
        plt.legend(loc='upper left')
        plt.savefig('fig6.png', bbox_inches='tight')
        plt.show()





if __name__ =="__main__":
    Graph = graphing()
    if not os.path.exists('myjson.json'):#测试阶段的函数，用json文件临时存储变量信息；避免每次都要运行爬虫
        Graph.spider_and_save()
        Graph.load_database('mydb.db')
        with open('myjson.json','w') as load_f:
            json.dump(Graph.data,load_f)
        load_f.close()

    else:
        with open('myjson.json','r') as load_f:
            Graph.data = json.load(load_f)
        load_f.close()

    Graph.graph0()
    Graph.graph1()
    Graph.graph2()
    Graph.graph3()
