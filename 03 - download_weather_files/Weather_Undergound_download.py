##########################################################################################
#   Script for the Download of historic data of weatherstation from Weatherundergound    #
#  The request info are the ID of the Station and the start and end date of the series   #
#    Developed by Lorenzo Bottaccioli    for info lorenzo.bottaccioli@polito.it   #
##########################################################################################
#   Script for the Download of historic data of weatherstation from Weatherundergound    #
#  The request info are the ID of the Station and the start and end date of the series   #
#    Developed by Lorenzo Bottaccioli    for info lorenzo.bottaccioli@polito.it   #
##########################################################################################

#import datetime, datetime
import datetime 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

    
start='2017-01-01' ###YYYY-MM-DD
end='2020-12-31'
PWS="ITORREPE3" # 'IEMILIAR178'-> Bologna / 'IPIEMONT220'-> Torino / 'ICINIS1'->Palermo / 'INAPLE20' ->  Napoli


def main(PWS,start,end):
    start_date=datetime.datetime.strptime(start,'%Y-%m-%d')
    end_date= datetime.datetime.strptime(end,'%Y-%m-%d')
    delta = datetime.timedelta(days=1)
    cur_date=start_date
    url = "https://www.wunderground.com/weatherstation/WXDailyHistory.asp"

    

    lookup_url = "http://www.wunderground.com/dashboard/pws/{}/table/{}-{}-{}/{}-{}-{}/daily"
    headers = {
        'cache-control': "no-cache",
        'postman-token': "72eed757-662e-d840-6ec2-4c0da5caaff9"
        }
    fields=['Date_Time','Temperature_C','Dew_Point_C','Humidity','Wind','Speed_m/s','Gust_m/s','Pressure_Pa','Precip_Rate_mm','Precip_Accum_mm','UV','Solar_W/m2']

    arr=["North","NNE","NE","ENE","East","ESE", "SE", "SSE","South","SSW","SW","WSW","West","WNW","NW","NNW"]    

    values={}
    df=pd.DataFrame(columns=fields)
    while cur_date <= end_date:
        print (cur_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))   
        url = lookup_url.format(PWS, cur_date.year,cur_date.month, cur_date.day, cur_date.year,cur_date.month, cur_date.day)
        response = requests.request("GET", url, headers=headers)
        soup = BeautifulSoup(response.text, features="html.parser")    
        # fp = open("output1.html", "w", encoding="utf-8")
        # fp.write(str(soup))
        # fp.close()
        for row in soup.findAll('tr'):
            if len(row.findAll('td')) == 12:
                for i,col in enumerate(row.findAll('td')):
                    if fields[i]=='Date_Time':
                        a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
                        # print(a)
                        in_time = datetime.datetime.strptime(a, "%I:%M %p")
                        out_time = datetime.datetime.strftime(in_time, "%H:%M")
                        out_time = datetime.datetime.strptime(out_time,  "%H:%M").time()
                        
                        tmp = datetime.datetime.date(cur_date)
                        tmp1 = datetime.datetime.combine(tmp,out_time)
                        # values[fields[i]] = cur_date.strftime('%Y-%m-%d')+' '+a
                        values[fields[i]] = tmp1
                    elif fields[i] in ['Temperature_C','Dew_Point_C']:
                        
                        a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
                        
                        try:
                            if a[-1]=='F':
                                a=float(a[:-2])
                                values[fields[i]] = (a - 32) * 5/9
                            else:
                                a=float(a[:-2])
                                values[fields[i]] = a
                        except:
                            print('problem with the data')
                    # elif fields[i] in ['Precip_Rate_mm', 'Precip_Accum_mm']:
                    #     a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
                    #     if a[-2:] == 'in':
                    #         a=float(a[:-3])
                    #         values[fields[i]] = a * 25.4
                    #     else:
                    #         a=float(a[:-3])
                    #         values[fields[i]] = a
                    # elif fields[i] == 'Pressure_Pa':
                    #     a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
                    #     if a[-2:] == 'in':
                    #         a=float(a[:-3])
                    #         values[fields[i]] = a * 3386 #from in of mercury to pascal
                    #     else:
                    #         a=float(a[:-3])
                    #         values[fields[i]] = a
                    # elif fields[i] in ['Speed_m/s', 'Gust_m/s']:
                    #     a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
                        
                    #     if a[-3:] == 'mph':
                    #         a=float(a[:-4])
                    #         values[fields[i]] = a / 2.237 #from mph to m/s
                    #     else:
                    #         a=float(a[:-4])
                    #         values[fields[i]] = a
                    # elif fields[i] == 'Humidity':
                    #     a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
                
                    #     a=float(a[:-2])
                    #     values[fields[i]] = a
                    # elif fields[i] == 'Solar_W/m2':
                    #     a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
                    #     a=float(a[:-5])
                    #     values[fields[i]] = a
                    # elif fields[i] == 'Wind':
                    #     a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
                    #     try:
                    #         a=arr.index(a)*22.5
                    #         values[fields[i]] = a
                    #     except:
                    #         values[fields[i]]=0
                    else:
                        a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
                        values[fields[i]] = a
                df=df.append(values,ignore_index=True)

        cur_date+=delta
    city = 'Torre_Pellice'
    df.to_csv(city+'_from_'+start+'_to_'+end,index=False)
if __name__ == "__main__":           
   
    main(PWS,start,end)

