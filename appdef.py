from flask import Flask, render_template, request
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
# For MAMP on Mac, add the port or unix_socket AND pwd = "root"
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='airline-booking',
                       port=3306,
                       # unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/error')
def errorpage():
    error = request.args.get('error')
    return render_template('error.html', error=error)