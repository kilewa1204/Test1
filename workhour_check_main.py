import time,datetime,random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from send_mail import *
def date_range(beginDate,endDate):
    dates=[]
    dt = datetime.datetime.strptime(beginDate,"%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates

def get_random(num):
    while True:
        base=int(100/num)
        _sum=0
        lst=[]
        for x in range(num):
            if x==num-1:
                lst.append(100-_sum)
            else:
                lst.append(random.randint(base-10,base+10))
                _sum=_sum+lst[-1]
        if sum(i<=0 for i in lst)==0 and (max(lst)-min(lst))<base:
            return lst
def workhour_main(date_times,users,pws):
    #options = Options()
    #options.add_argument("--disable-notifications")
    #browser = webdriver.Chrome('./chromedriver', chrome_options=options)
    try:
        browser = webdriver.Chrome('./chromedriver')
    except:
        browser = webdriver.Chrome(executable_path=r"D:\time_check_in\chromedriver.exe")
    for x in range(len(users)):
        user=users[x]
        pw=pws[x]
        browser.get("http://mems.miramems.com/index.html")
        browser.maximize_window()
        browser.implicitly_wait(30)
        browser.find_element(By.CSS_SELECTOR,"#username-inputEl").send_keys(user)#使用者輸入
        browser.find_element(By.CSS_SELECTOR,"#password-inputEl").send_keys(pw)#密碼輸入
        browser.find_element(By.ID,"panel-1014-innerCt").click()#登陸送出
        browser.implicitly_wait(60)
        browser.find_element(By.CSS_SELECTOR,"#panel-1035-body").click()#研發工時按鍵
        time.sleep(1)
        browser.implicitly_wait(30)
        browser.find_element(By.CSS_SELECTOR,"#addTimes_id").click()#添加工時按鍵
        time.sleep(1)
        browser.implicitly_wait(30)
        for date_time in date_times:
            browser.find_element(By.CSS_SELECTOR,'#addDateT_id-inputEl').clear()
            time.sleep(0.5)
            browser.find_element(By.CSS_SELECTOR,'#addDateT_id-inputEl').send_keys(date_time)
            time.sleep(1)
            browser.implicitly_wait(30)
            if "100" not in browser.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[4]/div/table/tfoot/tr/td[3]").text:
                while True:
                    try:
                        table=browser.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[4]/div/table/tbody")#找出計畫數量並求出計畫工時
                        browser.implicitly_wait(30)
                        num=len(table.find_elements(By.TAG_NAME,"tr"))
                        random_lst=get_random(num)
                        break
                    except:
                        print("get_table_error")
                        time.sleep(1)
                for x in range(num):
                    while True:
                        try:
                            browser.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[4]/div/table/tbody/tr[%d]/td[3]/div'%(x+1)).click()#工時輸入位置
                            time.sleep(1)
                            browser.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[6]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/input").clear()
                            browser.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[6]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/input").send_keys(str(random_lst[x]))#輸入工時數值
                            browser.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[6]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/input").send_keys(Keys.ENTER)
                            time.sleep(0.5)
                            browser.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div[4]/div/table/tbody/tr[%d]/td[5]/div'%(x+1)).click()#提交工時數值
                            time.sleep(1)
                            browser.implicitly_wait(30)
                            break
                        except:
                            time.sleep(1)
                #browser.find_element(By.CSS_SELECTOR,"#batchUpdateTimes_id-btnEl").click()#一鍵提交
                print(date_time+" Finish")
            else:
                print(date_time+"总工时：100")
    browser.close()
    browser.quit()
if __name__ == '__main__':
    date_list = [(datetime.date.today() + datetime.timedelta(-1)).strftime("%Y-%m-%d"),]#yesterday
    #date_list = ["2023-05-14",]
    #date_list = date_range("2023-01-30","2023-02-01")
    users=['kilewa','clcho','mason']
    pws=['000000','10260321','000000']
    try:
        workhour_main(date_list,users,pws)
    except:
        login_id='kwang@miradia.com'
        login_pw='0911Abcd'
        sender=r'kwang@miradia.com'
        recipients= r"kwang@miradia.com,"#字串物件,多人以逗號分隔
        subject=r"Workhour_Check_Program_Error"
        message='此信件為系統回覆,請勿回覆此信件'
        attach_files=[]
        send_email(sender,recipients,subject,message,attach_files,login_id,login_pw)