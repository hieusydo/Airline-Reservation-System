from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

from appdef import app, conn

@app.route('/customerHome')
def customerHome():
  username = session['username']
  cursor = conn.cursor();
  query = 'SELECT purchases.ticket_id, ticket.airline_name, ticket.flight_num, departure_airport, departure_time, arrival_airport, arrival_time \
  FROM purchases, ticket, flight \
  WHERE purchases.ticket_id = ticket.ticket_id \
  AND ticket.airline_name = flight.airline_name \
  AND ticket.flight_num = flight.flight_num \
  AND customer_email = %s AND departure_time > curdate()'
  cursor.execute(query, (username))
  data = cursor.fetchall()
  cursor.close()  
  return render_template('customer.html', username=username, posts=data)    

@app.route('/searchPageCustomer')
def searchPageCustomer():
  return render_template('searchCustomer.html')

@app.route('/searchCustomer', methods=['POST'])
def searchCustomer():
  username = session['username']
  cursor = conn.cursor()
  fromcity = request.form['fromcity']
  fromairport = request.form['fromairport']
  fromdate = request.form['fromdate']
  tocity = request.form['tocity']
  toairport = request.form['toairport']
  todate = request.form['todate']
  query = 'SELECT * FROM flight, airport, purchases, ticket \
          WHERE airport.airport_name=flight.departure_airport \
          AND flight.flight_num = ticket.flight_num AND flight.airline_name = ticket.airline_name\
          AND ticket.ticket_id = purchases.ticket_id\
          AND purchases.customer_email = %s\
          AND airport.airport_city = %s \
          AND airport.airport_name = %s \
          # AND flight.status = "Upcoming"\
          AND %s BETWEEN DATE_SUB(flight.departure_time, INTERVAL 2 DAY) AND DATE_ADD(flight.departure_time, INTERVAL 2 DAY) \
          AND %s BETWEEN DATE_SUB(flight.arrival_time, INTERVAL 2 DAY) AND DATE_ADD(flight.arrival_time, INTERVAL 2 DAY) \
          AND (flight.airline_name, flight.flight_num) in \
            (SELECT flight.airline_name, flight.flight_num FROM flight, airport \
            WHERE airport.airport_name=flight.arrival_airport \
            AND airport.airport_city = %s \
            AND airport.airport_name = %s)'
  cursor.execute(query, (username, fromcity, fromairport, fromdate, todate, tocity, toairport))
  data = cursor.fetchall()
  cursor.close()
  error = None
  if(data):
    return render_template('searchCustomer.html', results=data)
  else:
    #returns an error message to the html page
    error = 'No results found'
    return render_template('searchCustomer.html', error=error)  