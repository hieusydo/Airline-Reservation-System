from flask import Flask, render_template, request, session, redirect, url_for
import pymysql.cursors

from appdef import *

#Make sure that the user is actually staff before performing any operations
def authenticateStaff():
    username = ""
    try:
        #could be that there is no user, make sure
        username = session['username']
    except:
        return False
    
    cursor = conn.cursor()
    query = 'select * from airline_staff where username=%s'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    if(data):
        return True
    else:
        #Logout before returning error message
        session.pop('username')
        return False

@app.route('/staffHome')
def staffHome():
    if authenticateStaff():
        username = session['username']
        message = request.args.get('message')
        
        return render_template('staff.html', username=username, message=message)
    else:
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))

@app.route('/staffHome/changeFlight')
def changeFlightStatusPage():
    if authenticateStaff():
        error = request.args.get('error')
        return render_template('changeFlight.html', error=error)
    else:
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))

@app.route('/staffHome/changeFlight/Auth', methods=['POST'])
def changeFlightStatus():
    if not authenticateStaff():
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))
    
    username = session['username']
    
    flightnum = request.form['flightnum']
    status = request.form['status']
    if not status:
        error = 'Did not select new status'
        return redirect(url_for('changeFlightStatusPage', error=error))
    
    cursor = conn.cursor()
    query = 'update flight set status=%s where flight_num=%s'
    cursor.execute(query, (status, flightnum))
    conn.commit()
    cursor.close()
    
    return redirect(url_for('staffHome', message="Operation Successful"))
    
@app.route('/staffHome/addAirport')
def addAirportPage():
    if authenticateStaff():
        error = request.args.get('error')
        return render_template('addAirport.html', error=error)
    else:
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))

@app.route('/staffHome/addAirport/Auth', methods=['POST'])
def addAirport():
    if not authenticateStaff():
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))
    
    username = session['username']
    
    name = request.form['name']
    city = request.form['city']
    
    cursor = conn.cursor()
    query = 'insert into airport values (%s, %s)'
    cursor.execute(query, (name, city))
    conn.commit()
    cursor.close()
    
    return redirect(url_for('staffHome', message="Operation Successful"))