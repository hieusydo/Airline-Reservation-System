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