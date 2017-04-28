from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import string, sys, random

from appdef import app, conn

@app.route('/purchasePageCustomer')
def purchasePage():
  return render_template('purchaseCustomer.html')

@app.route('/purchasePageAgent')
def purchasePageAgent():
  return render_template('purchaseAgent.html')

@app.route('/searchPurchaseCustomer', methods=['POST'])
def searchPurchaseCustomer():
  cursor = conn.cursor()
  fromcity = request.form['fromcity']
  fromairport = request.form['fromairport']
  fromdate = request.form['fromdate']
  tocity = request.form['tocity']
  toairport = request.form['toairport']
  todate = request.form['todate']
  query = 'SELECT distinct f.airline_name, f.flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, airplane_id \
          FROM flight as f, airport \
          WHERE airport.airport_name=f.departure_airport \
          AND airport.airport_city = %s \
          AND airport.airport_name = %s \
          AND %s BETWEEN DATE_SUB(f.departure_time, INTERVAL 2 DAY) AND DATE_ADD(f.departure_time, INTERVAL 2 DAY)\
          AND %s BETWEEN DATE_SUB(f.arrival_time, INTERVAL 2 DAY) AND DATE_ADD(f.arrival_time, INTERVAL 2 DAY)\
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
  cursor.execute(query, (fromcity, fromairport, fromdate, todate, tocity, toairport))
  # print cursor._executed
  data = cursor.fetchall()
  cursor.close()
  error = None
  if(data):
    return render_template('purchaseCustomer.html', results=data)
  else:
    #returns an error message to the html page
    error = 'No results found'
    return render_template('purchaseCustomer.html', searchError=error) 

# Thought it works, not really...
# def _genTix(ticketCount, airline_name, flight_num):
#   pre = [str(flight_num), str(ticketCount+1)]
#   di = dict(zip(string.letters,[ord(c)%32 for c in string.letters])) # taken from http://stackoverflow.com/a/4535403
#   for c in airline_name:
#     pre.append(str(di[c]))
#   return ''.join(pre)

def _genTix():
  cursor = conn.cursor()
  cand = random.randint(1, 2147483647)
  query = 'SELECT ticket_id FROM ticket'
  cursor.execute(query)
  allTix = cursor.fetchall()
  cursor.close()
  while cand in allTix:
    cand = random.randint(1, 2147483647)
  return cand

@app.route('/purchaseCustomer', methods=['POST'])
def purchaseCustomer():
  username = session['username']
  cursor = conn.cursor()
  airline_name = request.form['airline_name']
  flight_num = request.form['flight_num']
  # Find the number of tickets to generate the next ticket_id
  queryCount = 'SELECT COUNT(*) as count FROM ticket \
                WHERE ticket.airline_name = %s AND ticket.flight_num = %s'
  cursor.execute(queryCount, (airline_name, flight_num))
  ticketCount = cursor.fetchone()
  ticketCountVal = 0
  if ticketCount != None:
    ticketCountVal = ticketCount['count']
  # ticket_id = _genTix(ticketCountVal, airline_name.strip().replace(' ', ''), flight_num)
  ticket_id = _genTix()
  # print("WHAT FUCKING NUMBER: ", ticket_id)
  # Create the new ticket
  queryNewTicket = 'INSERT INTO ticket VALUES(%s, %s, %s)'
  cursor.execute(queryNewTicket, (ticket_id, airline_name, flight_num))
  # Finalize the purchase
  queryPurchase = 'INSERT INTO purchases VALUES(%s, %s, %s, CURDATE())'
  cursor.execute(queryPurchase, (ticket_id, username, None))
  data = cursor.fetchone()
  conn.commit()
  cursor.close()
  return render_template('purchaseCustomer.html')     

@app.route('/searchPurchaseAgent', methods=['POST'])
def searchPurchaseAgent():
  cursor = conn.cursor()
  fromcity = request.form['fromcity']
  fromairport = request.form['fromairport']
  fromdate = request.form['fromdate']
  tocity = request.form['tocity']
  toairport = request.form['toairport']
  todate = request.form['todate']
  query = 'SELECT distinct f.airline_name, f.flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, airplane_id \
          FROM flight as f, airport \
          WHERE airport.airport_name=f.departure_airport \
          AND airport.airport_city = %s \
          AND airport.airport_name = %s \
          AND %s BETWEEN DATE_SUB(f.departure_time, INTERVAL 2 DAY) AND DATE_ADD(f.departure_time, INTERVAL 2 DAY)\
          AND %s BETWEEN DATE_SUB(f.arrival_time, INTERVAL 2 DAY) AND DATE_ADD(f.arrival_time, INTERVAL 2 DAY)\
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

  cursor.execute(query, (fromcity, fromairport, fromdate, todate, tocity, toairport))
  # print cursor._executed
  data = cursor.fetchall()
  cursor.close()
  error = None
  if(data):
    print(data)
    return render_template('purchaseAgent.html', results=data)
  else:
    #returns an error message to the html page
    error = 'No results found'
    return render_template('purchaseAgent.html', searchError=error) 

@app.route('/purchaseAgent', methods=['POST'])
def purchaseAgent():
  username = session['username']
  customer_email = request.form['customer_email']
  cursor = conn.cursor()
  airline_name = request.form['airline_name']
  flight_num = request.form['flight_num']
  # Find the number of tickets to generate the next ticket_id
  queryCount = 'SELECT COUNT(*) as count FROM ticket \
                WHERE ticket.airline_name = %s AND ticket.flight_num = %s'
  cursor.execute(queryCount, (airline_name, flight_num))
  ticketCount = cursor.fetchone()
  ticketCountVal = 0
  if ticketCount != None:
    ticketCountVal = ticketCount['count']  
  # ticket_id = _genTix(ticketCountVal, airline_name.strip().replace(' ', ''), flight_num)
  ticket_id = _genTix()
  # Create the new ticket
  queryNewTicket = 'INSERT INTO ticket VALUES(%s, %s, %s)'
  cursor.execute(queryNewTicket, (ticket_id, airline_name, flight_num))
  # Get booking_agent_id
  queryGetID = 'SELECT booking_agent_id FROM booking_agent WHERE email=%s'
  cursor.execute(queryGetID, username)
  agentID = cursor.fetchone() # returns a dict 
  # Finalize the purchase
  queryPurchase = 'INSERT INTO purchases VALUES(%s, %s, %s, CURDATE())'
  cursor.execute(queryPurchase, (ticket_id, customer_email, agentID['booking_agent_id']))
  data = cursor.fetchone()
  conn.commit()
  cursor.close()
  error = None
  if(data):
    return render_template('agent.html', results=data)
  else:
    #returns an error message to the html page
    error = 'Cannot complete purchase'
    return render_template('purchaseAgent.html', error=error)        