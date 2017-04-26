from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

from appdef import app, conn

@app.route('/purchasePage')
def purchasePage():
  return render_template('purchase.html')

@app.route('/searchPurchase', methods=['POST'])
def searchPurchase():
  username = session['username']
  cursor = conn.cursor()
  fromcity = request.form['fromcity']
  fromairport = request.form['fromairport']
  fromdate = request.form['fromdate']
  tocity = request.form['tocity']
  toairport = request.form['toairport']
  todate = request.form['todate']
  query = 'SELECT * FROM flight as f, airport, purchases, ticket \
          WHERE airport.airport_name=f.departure_airport \
          AND f.flight_num = ticket.flight_num AND f.airline_name = ticket.airline_name\
          AND ticket.ticket_id = purchases.ticket_id\
          AND purchases.customer_email = %s\
          AND airport.airport_city = %s \
          AND airport.airport_name = %s \
          AND f.departure_time BETWEEN %s AND %s \
          AND (f.airline_name, f.flight_num) in \
            (SELECT flight.airline_name, flight.flight_num FROM flight, airport \
            WHERE airport.airport_name=flight.arrival_airport \
            AND airport.airport_city = %s \
            AND airport.airport_name = %s) \
          AND (SELECT DISTINCT seats \
              FROM flight, airplane \
              WHERE flight.airplane_id = airplane.airplane_id AND flight.airline_name = airplane.airline_name \
              AND flight.airline_name = f.airline_name AND flight.flight_num = f.flight_num) \
              >= (SELECT COUNT(*) \
              FROM ticket \
              WHERE ticket.airline_name = f.airline_name AND ticket.flight_num = f.flight_num)'
  cursor.execute(query, (username, fromcity, fromairport, fromdate, todate, tocity, toairport))
  data = cursor.fetchall()
  cursor.close()
  error = None
  if(data):
    return render_template('purchase.html', results=data)
  else:
    #returns an error message to the html page
    error = 'No results found'
    return render_template('purchase.html', error=error) 

@app.route('/purchase', methods=['POST'])
def purchase():
  username = session['username']
  cursor = conn.cursor()
  airline_name = request.form['airline_name']
  flight_num = request.form['flight_num']
  # Find the number of tickets to generate the next ticket_id
  queryCount = 'SELECT COUNT(*) as count FROM ticket \
                WHERE ticket.airline_name = %s AND ticket.flight_num = %s'
  cursor.execute(queryCount, (airline_name, flight_num))
  ticketCount = cursor.fetchone()
  ticket_id = ticketCount['count'] + 1
  # Create the new ticket
  queryNewTicket = 'INSERT INTO ticket VALUES(%s, %s, %s)'
  cursor.execute(queryNewTicket, (ticket_id, airline_name, flight_num))
  # Finalize the purchase
  queryPurchase = 'INSERT INTO purchases VALUES(%s, %s, %s, CURDATE())'
  cursor.execute(queryPurchase, (ticket_id, username, 'null'))
  data = cursor.fetchone()
  conn.commit()
  cursor.close()
  error = None
  if(data):
    return render_template('customer.html', results=data)
  else:
    #returns an error message to the html page
    error = 'Cannot complete purchase'
    return render_template('purchase.html', error=error)     