from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors
import time

from appdef import app, conn

@app.route('/search')
def searchpage():
    error = request.args.get('error')
    return render_template('search.html', error=error)

@app.route('/searchFlights/city', methods=['POST'])
def searchForCity():
    cursor = conn.cursor()
    searchtext = request.form['citysearchbox']
    query = 'select * from flight,airport where (airport.airport_name=flight.departure_airport or airport.airport_name=flight.arrival_airport) and airport.airport_city=%s and status="upcoming"'
    cursor.execute(query, (searchtext))
    data = cursor.fetchall()
    cursor.close()
    error = None
    if(data):
        return render_template('searchFlights.html', results=data)
    else:
        #returns an error message to the html page
        error = 'No results found'
        return redirect(url_for('searchpage', error=error))

@app.route('/searchFlights/airport', methods=['POST'])
def searchForAirport():
    cursor = conn.cursor()
    searchtext = request.form['airportsearchbox']
    query = 'select * from flight where (departure_airport = %s or arrival_airport = %s) and status="upcoming"'
    cursor.execute(query, (searchtext, searchtext))
    data = cursor.fetchall()
    cursor.close()
    error = None
    if(data):
        return render_template('searchFlights.html', results=data)
    else:
        #returns an error message to the html page
        error = 'No results found'
        return redirect(url_for('searchpage', error=error))

@app.route('/searchFlights/date', methods=['POST'])
def searchForDate():
    cursor = conn.cursor()
    searchtext = request.form['datesearchbox']
    try:
        valid_date = time.strptime(searchtext, '%Y/%m/%d')
    except ValueError:
        error = 'Invalid date entered'
        return redirect(url_for('searchpage', error=error))
    
    query = 'select * from flight where (date(departure_time) = %s or date(arrival_time) = %s) and status="upcoming"'
    cursor.execute(query, (searchtext, searchtext))
    data = cursor.fetchall()
    cursor.close()
    error = None
    if(data):
        return render_template('searchFlights.html', results=data)
    else:
        #returns an error message to the html page
        error = 'No results found'
        return redirect(url_for('searchpage', error=error))