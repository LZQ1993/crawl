import requests
import json

import mysqlDao


class Car(object):
    def __init__(self):
        self.ms = mysqlDao.MysqlDao()
        self.session = requests.session()
        self.url = "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml"
        # 其中: 第三行  "resultPagination.start": "48",
        # resultPagination.start等于48时, 代表从全部搜索结果的第48条取,显示从49-60的12条,
        # 等于0时 是从第0条(就是第一条)开始取,显示前12条
        # 到写代码时, 可以通过data2post['resultPagination.start']=60(或别的)来改变取值, 增加12来抓后面的12条数据
        self.data = {
            "resultPagination.limit": "12",
            "resultPagination.sumLimit": "10",
            "resultPagination.start": "0",
            "resultPagination.totalCount": "488",
            "searchCondition.sortFields": "-APD,+PD",
            "searchCondition.searchType": "Sino_foreign",
            "searchCondition.originalLanguage": "",
            "searchCondition.extendInfo['MODE']": "MODE_TABLE",
            "searchCondition.extendInfo['STRATEGY']": "STRATEGY_CALCULATE",
            "searchCondition.searchExp": "((IPC分类号=(B60K1/04) AND 关键词=(新能源汽车 碰撞)))",
            "searchCondition.executableSearchExp": "VDB:((ICST='B60K1/04' AND (KW_CPP='新能源汽车' OR KW_CPP='碰撞')))",
            "searchCondition.dbId": "",
            "searchCondition.literatureSF": "((IPC分类号=(B60K1 // 04) AND 关键词 = (新能源汽车 碰撞)))",
            "searchCondition.targetLanguage": "",
            "searchCondition.resultMode": "SEARCH_MODE",
            "searchCondition.strategy": "",
            "searchCondition.searchKeywords": "[碰][ ]{0,}[撞][ ]{0,},[新][ ]{0,}[能][ ]{0,}[源][ ]{0,}[汽][ ]{0,}[车][ ]{0,},[B][ ]{0,}[6][ ]{0,}[0][ ]{0,}[K][ ]{0,}[1][ ]{0,}[/][ ]{0,}[0][ ]{0,}[4][ ]{0,}",
        }
        self.headers = {
            'Accept': 'application/json, text/javascript,*/*;q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '1432',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.pss-system.gov.cn',
            'Origin': 'http://www.pss-system.gov.cn',
            'Referer': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }

        co1 = "WEE_SID=ujxKyDIb6MhgtEuomVAjb6-_z3vR8ZDGuFYVF6wr7qYlut9xvbZe!-1694136728!1229548724!1534557958683;"
        co2 = "IS_LOGIN=true; wee_username=QWVyaWMwMDc%3D; wee_password=TFpRMTM1OTE5OTAyMjFMWg%3D%3D;"
        co3 = "JSESSIONID=ujxKyDIb6MhgtEuomVAjb6-_z3vR8ZDGuFYVF6wr7qYlut9xvbZe!-1694136728!1229548724;"
        co4 = "hibext_instdsigdipv2=1; _ga=GA1.3.1678005571.1530947667; _gid=GA1.3.748374959.1530947667"
        cookie = co1 + co2 + co3 + co4
        self.headers['Cookie'] = cookie

    def patent(self):
        # searchExp,literatureSF,resultMode,searchKeywords = self.loadData();
        for i in range(0,41):
            self.data['resultPagination.start'] = str(i*12)
            response = self.session.post(url=self.url, data=self.data, headers=self.headers).content
            response = response.decode('utf-8')
            jsonstr2dict = json.loads(response)
            self.addData(jsonstr2dict)
        self.ms.close()

    def loadData(self):
        searchExp = {
            "H01M10/50":"",
            "B60K1/04": "",
            "H01M2/10": "",
            "H01M12": "",
            "B60k11": "",
            "B60L11/18": "",
        }
        literatureSF = {
             "H01M10/50":"",
        }
        resultMode = {
            "H01M10/50": "",
        }
        searchKeywords = {
             "H01M10/50":"",
        }
        return searchExp,literatureSF,resultMode,searchKeywords
    def addData(self,dict):
        data = dict['searchResultDTO']['searchResultRecord']
        for i in range(0,len(data)):
            inventInfo = data[i]['fieldMap']
            inventName = str(inventInfo['TIVIEW'])
            applyNum = str(inventInfo['APO'])
            applyDate = str(inventInfo['APD_VALUE'])
            publicNum = str(inventInfo['PN'])
            publicDate = str(inventInfo['IC'])
            IPCnum = str(inventInfo['PD'])
            applyPeople = str(inventInfo['PAVIEW'])
            inventPeople = str(inventInfo['INVIEW'])
            sql = "insert into carInfo(inventName,applyNum,applyDate,publicNum,publicDate,IPCnum,applyPeople,inventPeople) VALUES ('" + inventName + "','" + applyNum + "','" + applyDate + "','" + publicNum + "','" + publicDate + "','" + IPCnum + "','" + applyPeople + "','" + inventPeople + "')"
            self.ms.add(sql)

if __name__ == "__main__":
    car = Car()
    car.patent()