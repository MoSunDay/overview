#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql as MySQLdb
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email(receivere,title,content):
    sender = 'xxx'
    #receiveres = ['xxx','xxx']
    receiveres = []
    receiveres.append(receivere)
    subject = title
    username = 'xxx'
    password = 'xxx'

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = Header("xxx", 'utf-8')
    msg['To'] =  Header("xxx", 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    smtp = smtplib.SMTP()
    smtp.connect('smtp.ym.163.com')
    smtp.login(username, password)
    for receiver in receiveres:
        smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

if __name__ == '__main__':
    delete_table = ['cpu_status', 'io_status', 'network_status', 'tcp_status', 'mem_status']
    timestamp = (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    delete_num = 0
    try:
        con = MySQLdb.connect('xxx', 'xxx', 'xxx', 'xxx')
        cur = con.cursor()
        for table in delete_table:
            sql = "delete from {0} WHERE time_now < \"{1}\"".format(table, timestamp)
            data = cur.execute(sql)
            con.commit()
            delete_num += data
    except Exception as information:
        print("Exception: at delete data :{0}".format(information))
    finally:
        cur.close()
        con.close()

    send_email("xxx", "xxx", "xxx delete:{0}".format(delete_num))

