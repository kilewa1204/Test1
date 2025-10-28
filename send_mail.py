import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime,os


def send_email(sender,recipients,subject,message,attach_files,login_id,login_pw):
    content  = MIMEMultipart()#建立MIMEMultipart物件
    content['From']=sender#寄件者
    content['To']=recipients#收件者
    content['Subject']=subject#郵件標題
    content.attach(MIMEText(message, 'plain'))#郵件內容
    if len(attach_files)!=0:
        for attach_file in attach_files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(attach_file, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(attach_file))
            content.attach(part)
    try:
        s = smtplib.SMTP(host='smtp.office365.com', port=587)
        s.starttls()
        s.login(login_id,login_pw)
        s.send_message(content)
        del content
        s.quit()
    except Exception as e:
        print("Error message: ", e)


if __name__ == "__main__":
    login_id='kwang@miradia.com'
    login_pw='0911Abcd'
    sender=r'kwang@miradia.com'
    recipients= r"kwang@miradia.com,"#字串物件,多人以逗號分隔
    subject=r"Die Tracking State(%s)"%(datetime.datetime.now().strftime("%Y%m%d"))
    message='此信件為系統回覆,請勿回覆此信件'
    attach_files=[r"D:\01_Office\Die_Tracking\20220827233001.txt",r"D:\01_Office\Die_Tracking\222.txt"]
    send_email(sender,recipients,subject,message,attach_files,login_id,login_pw)
    