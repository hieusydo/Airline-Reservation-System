from flask import Flask, render_template, request
import pymysql.cursors
import datetime

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
# For MAMP on Mac, add the port or unix_socket AND pwd = "root"
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root', # password for MAMP
                       # password='', # password for XAMP/linux
                       db='airline-booking',
                       # port=5000,
                       unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Check that the two dates don't overlap
def validateDates(begintime, endtime):
    begindate = datetime.datetime.strptime(begintime, '%Y-%m-%dT%H:%M:%S')
    enddate = datetime.datetime.strptime(endtime, '%Y-%m-%dT%H:%M:%S')
    return begindate <= enddate

@app.route('/error')
def errorpage():
    error = request.args.get('error')
    return render_template('error.html', error=error)