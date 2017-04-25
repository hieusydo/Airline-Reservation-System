from flask import Flask, render_template, request
import pymysql.cursors

from appdef import app, conn

#Make sure that the user is actually staff before performing any operations
def authenticateStaff():
    username = session['username']
    cursor = conn.cursor()
    query = 'select * from airline_staff where username=%s'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    if(data):
        return True
    else:
        return False

@app.route('/staffHome')
def staffHome():
    if authenticateStaff():
        return render_template('staff.html')
    else
        error = 'Invalid Credentials'
        return render_template('/', error=error)

