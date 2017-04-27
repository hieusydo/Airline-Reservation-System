from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

from appdef import app, conn

@app.route('/agentHome')
def agentHome():
  username = session['username']
  cursor = conn.cursor();
  query = 'SELECT * \
  FROM purchases, ticket, flight, booking_agent \
  WHERE purchases.ticket_id = ticket.ticket_id \
  AND ticket.airline_name = flight.airline_name \
  AND ticket.flight_num = flight.flight_num \
  AND booking_agent.email = %s AND booking_agent.booking_agent_id = purchases.booking_agent_id \
  AND departure_time > curdate()'
  cursor.execute(query, (username))
  data = cursor.fetchall()
  cursor.close()  
  return render_template('agent.html', username=username, posts=data)      