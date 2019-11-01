## leanring form site http://c.biancheng.net/view/2011.html  Thanks!
## Use http://oa.corp-ci.com/admin.php as example
## this site is company's LAN site, which means 403 when you try it by yourself
## we are going to analyze our daily attendence record


import requests
import json
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--cookie', required=True, type=str)
parser.add_argument('--begin', required=True, type=str)
parser.add_argument('--end', required=True, type=str)

def getAttendenceList(cookie,begin,end):
    url = 'http://oa.corp-ci.com/oa.php/attendance/getSinglePunchList/'+begin+'/'+end
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
              'Connection': 'keep-alive',
              'Cookie': cookie,
              'Host': 'oa.corp-ci.com',
              'Referer': 'http://oa.corp-ci.com/oa.php/attendance/getSinglePunchList/2019-10-01/2019-11-01',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36}'}
    response = requests.get(url, headers=header)
    return response

def toJson(text):
    return json.loads(text)

def getOvertime(text):
    result=[]
    soup=BeautifulSoup(text,'lxml')
    data=soup.find_all('tr')
    filename = "attendence.txt"
    with open(filename,'w') as f:
        for i in range(1,len(data)):
            unit=[]
            ## date
            date = soup.select('#print_area > div.punch-box.wrap > div.system-main > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(1)')[0].text
            unit.append(date)
            ## begin
            begin = soup.select('#print_area > div.punch-box.wrap > div.system-main > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(2)')[0].text
            unit.append(begin)
            ## end
            end = soup.select('#print_area > div.punch-box.wrap > div.system-main > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(5)')[0].text
            unit.append(end)
            hour=end.split(":")[0]
            if len(hour)>0 and int(hour) >= 20 :
                f.write("\t".join(unit))
                f.write("\n")
            ## total
            total = soup.select('#print_area > div.punch-box.wrap > div.system-main > table > tbody > tr:nth-of-type('+str(i)+') > td:nth-of-type(6)')[0].text
            unit.append(total)
            result.append(unit)
            #print(unit)
            #f.write("\t".join(unit))
            #f.write("\n")
    return result

#cookie='QwlQt_adminid=1537; QwlQt_adminname=wangyongjia%40corp-ci.com; QwlQt_adminrealname=%E7%8E%8B%E6%B0%B8%E4%BD%B3; QwlQt_adminrealhash=593afd892d47a6b1; QwlQt_adminhash=593afd892d47a6b1; openemail=wangyongjia%40corp-ci.com; openhash=wwFp6bsRE9tzw; openadminname=wangyongjia; openpassword=cf0d8273d15586d019e96665752b4b97; _pk_id.3.493b=bcd218937192ac39.1554865512.3.1561611775.1557109478.; openname=wangyongjia; openid=1537'
#attendence = getAttendenceList(cookie,'2019-10-01','2019-11-01').text
cookie = parser.parse_args().cookie
begin = parser.parse_args().begin
end = parser.parse_args().end
attendence = getAttendenceList(cookie,begin,end).text
getOvertime(attendence)
    
