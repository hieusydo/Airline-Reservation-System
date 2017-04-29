from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors
import time

from appdef import *

@app.route('/search')
def searchpage():
    error = request.args.get('error')
    return render_template('search.html', error=error)

@app.route('/searchFlights/city', methods=['POST'])
def searchForCity():
    cursor = conn.cursor()
    searchtext = request.form['citysearchbox']
    query = 'select * from flight,airport where (airport.airport_name=flight.departure_airport or airport.airport_name=flight.arrival_airport) and airport.airport_city=%s and (departure_time >= curtime() or arrival_time >= curtime())'
    cursor.execute(query, (searchtext))
    data = cursor.fetchall()
    cursor.close()
    error = None
    if data:
        return render_template('searchFlights.html', results=data)
    else:
        #returns an error message to the html page
        error = 'No results found'
        return redirect(url_for('searchpage', error=error))

@app.route('/searchFlights/airport', methods=['POST'])
def searchForAirport():
    cursor = conn.cursor()
    searchtext = request.form['airportsearchbox']
    query = 'select * from flight where (departure_airport = %s or arrival_airport = %s) and (departure_time >= curtime() or arrival_time >= curtime())'
    cursor.execute(query, (searchtext, searchtext))
    data = cursor.fetchall()
    cursor.close()
    error = None
    if data:
        return render_template('searchFlights.html', results=data)
    else:
        #returns an error message to the html page
        error = 'No results found'
        return redirect(url_for('searchpage', error=error))

@app.route('/searchFlights/date', methods=['POST'])
def searchForDate():
    begintime = request.form['begintime']
    endtime = request.form['endtime']
    
    if not validateDates(begintime, endtime):
        error = 'Invalid date range'
        return redirect(url_for('searchpage', error=error))
    
    cursor = conn.cursor()
    query = 'select * from flight where ((departure_time between %s and %s) or (arrival_time between %s and %s)) and (departure_time >= curtime() or arrival_time >= curtime())'
    cursor.execute(query, (begintime, endtime, begintime, endtime))
    data = cursor.fetchall()
    cursor.close()
    error = None
    if data:
        return render_template('searchFlights.html', results=data)
    else:
        #returns an error message to the html page
        error = 'No results found'
        return redirect(url_for('searchpage', error=error))