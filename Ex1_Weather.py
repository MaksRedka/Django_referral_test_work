import csv
from datetime import datetime
from datetime import timedelta

file_name = "34300.01.01.2016.01.01.2017.1.0.0.ru"
arr = []

with open(file_name + '.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    
    for row in spamreader:
        arr.append(row)

arr = arr[6:] #remove rows with comments

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def calcWeather(data_arr, date_format, feature, min_max=max):
    cur_date = None
    statistic = {}
    
    for index_row, row in enumerate(data_arr):
        if  index_row != 0:
            cur_date = datetime.strptime(row[0], '%d.%m.%Y %H:%M')

        if cur_date is not None:
            el = row[data_arr[0].index(feature)]

            if date_format == "day" or date_format == "week":
                date = "{}.{}.{}".format(cur_date.day, cur_date.month, cur_date.year)
            elif date_format == "month":
                date = "{}.{}".format(cur_date.month, cur_date.year)

            if index_row > 0 and el != None:
                exist = statistic.get(date)

                if exist is None and isfloat(el):
                    statistic[date] = [float(el), 1] # [speed, count]
                else:
                    data = statistic.get(date)
                    if data is not None and el != None and isfloat(el):
                        data[0] += float(el)
                        data[1] += 1
                        statistic[date] = data
    
    if date_format == "month" or date_format == "day":  
        try:
            weather = min_max(statistic.values())
            month = list(statistic.keys())[list(statistic.values()).index(weather)]
            return [month, weather[0] / weather[1]]
        except:
            print("Oppps, min_max is not callable")    
    else:
        week_statistic = {}
        reversed_statistic = dict(reversed(list(statistic.items())))
        start_date = list(reversed_statistic.keys())[0]
        end_date = list(reversed_statistic.keys())[-1]
        cur_date_obj = datetime.strptime(start_date, '%d.%m.%Y')
        end_date_obj = datetime.strptime(end_date, '%d.%m.%Y')

        week_beginning = ""
        week_end = ""
        counter = 0
        summery = 0

        while cur_date_obj.strftime('%d.%m.%Y') != end_date_obj.strftime('%d.%m.%Y'):
            counter += 1
            precipitation = statistic.get(cur_date_obj.strftime('%#d.%#m.%#Y'))

            if precipitation is not None:
                summery += precipitation[0]
                
            if counter == 1:
                week_beginning = cur_date_obj.strftime('%d.%m.%Y')                    
            elif counter == 7:
                week_end = cur_date_obj.strftime('%d.%m.%Y')
                counter = 0
                week_statistic[week_beginning + " - " + week_end] = summery
                summery = 0 
            cur_date_obj += timedelta(days=1)

        try:
            min_max_precipitation = min_max(week_statistic.values())
            week = list(week_statistic.keys())[list(week_statistic.values()).index(min_max_precipitation)]
            return [week, min_max_precipitation]
        except:
            print("Oppps, min_max is not callable") 


wind = calcWeather(arr, "month","Ff", max)
print("The most windy month", wind)

min_temp_month = calcWeather(arr, "month", "T", min)
print("The coldes month", min_temp_month)

min_temp_day = calcWeather(arr, "day", "T", min)
print("The coldes day", min_temp_day)

max_temp_month = calcWeather(arr, "month", "T", max)
print("The hotest month", max_temp_month)

max_temp_day = calcWeather(arr, "day", "T", max)
print("The hotest day", max_temp_day)

max_amount_of_rains = calcWeather(arr, "week", "RRR", max)
print("Max amount of rains", max_amount_of_rains)