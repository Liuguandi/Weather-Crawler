from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from  time import sleep

weather=[]
time=[]
wind=[]
maxD=[]#每日最高温度最低温度
date=[]


html=urlopen("http://tianqi.sogou.com/nanjing/")
dataWeather = BeautifulSoup(html) 


#####最高温度最低温度
def getDegree(dataWeather):    
    maxAndMin = dataWeather.find_all("div",{"class":"r-temp"})
    new_maxAndMin=str(maxAndMin[0])
    new_maxAndMin=new_maxAndMin[31:]
    
    maxD=re.split(r'[,]',new_maxAndMin)
    tempW=maxD[6]
    lengthTemp=len(tempW)
    if(maxD[6][0]=='-'):
        maxD[6]=tempW[0:3]
        if(tempW[lengthTemp-3]=='-'):
            maxD.insert(7,tempW[lengthTemp-3:])
        else:
            maxD.insert(7,tempW[lengthTemp-2:])
    else:
        maxD[6]=tempW[0:2]
        if(tempW[lengthTemp-3]=='-'):
            maxD.insert(7,tempW[lengthTemp-3:])
        else:
            maxD.insert(7,tempW[lengthTemp-2:])
    tempW=maxD[13]
    lengthTemp=len(tempW)
    if(tempW[0]=='-'):
        maxD[13]=tempW[0:3]
    else:
        maxD[13]=tempW[0:2]
    return maxD

##############天气
def getWeather(dataWeather):
    nameList = dataWeather.find_all("p",{"class":"des"})
    count = 0
    for name in nameList:
        count+=1
        weather.append(name.get_text())
        if(count==7):
            break
    return weather
        
##############日期   （今天明天昨天）
def getTime(dataWeather):
    nameList = dataWeather.find_all("p",{"class":"text"})
    count = 0
    for Time in nameList:
        count+=1
        if(count<=2):
            continue
        time.append(Time.get_text())
        if(count==9):
            break
    return time
        
##############风
def getWind(dataWeather):
    nameList = dataWeather.find_all("p",{"class":"wind"})
    count = 0
    for name in nameList:
        count+=1
        wind.append(name.get_text())
        if(count==7):
            break
    return wind


##############日历 几月几号
def getDate(dataWeather):
    nameList = dataWeather.find_all("p",{"class":"date"})
    count = 0
    for Time in nameList:
        count+=1
        date.append(Time.get_text())
        if(count==7):
            break
    return date

while True:
    maxD=getDegree(dataWeather)
    getWeather(dataWeather)
    getTime(dataWeather)
    getWind(dataWeather)
    getDate(dataWeather)
    fw=open('/home/pi/demo/crawler/weatherInformation.txt','w')
    content='七日天气'+'\n'
    for i in range(0,7):
        content+=date[i]+' '+time[i]+'  '+weather[i]+' '+wind[i]+' '+'最高温度'+maxD[i]+'度 '+'最低温度'+maxD[i+7]+'度 '+'\n'
    fw.write(content)
    fw.close()
    #print (content)
    sleep(50)
