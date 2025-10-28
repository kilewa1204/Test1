import datetime
def date_range(beginDate,endDate):
    dates=[]
    dt = datetime.datetime.strptime(beginDate,"%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates
if __name__ == "__main__":
    date_list = date_range("2022-08-01","2022-09-01")
    print(date_list)
