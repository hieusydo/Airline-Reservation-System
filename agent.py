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
  AND departure_time > curdate() \
  ORDER BY customer_email'
  cursor.execute(query, (username))
  data = cursor.fetchall()

  # Get booking_agent_id
  queryGetID = 'SELECT booking_agent_id FROM booking_agent WHERE email=%s'
  cursor.execute(queryGetID, username)
  agentID = cursor.fetchone()
  # Get total commsion in the past 30 days
  queryGetCommission = 'SELECT sum(price)*.10 as totalComm FROM purchases, ticket, flight \
                        WHERE purchases.ticket_id = ticket.ticket_id \
                        AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num \
                        AND purchases.purchase_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE() \
                        AND purchases.booking_agent_id = %s'
  cursor.execute(queryGetCommission, agentID['booking_agent_id'])
  totalComm = cursor.fetchone()
  totalCommVal = 0
  if totalComm['totalComm'] != None:
    totalCommVal = totalComm['totalComm']
  # print totalComm 
  # Get total tickets in the past 30 days 
  queryGetTicketCount = 'SELECT count(*) as ticketCount FROM purchases, ticket, flight \
                        WHERE purchases.ticket_id = ticket.ticket_id \
                        AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num \
                        AND purchases.purchase_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE() \
                        AND purchases.booking_agent_id = %s'
  cursor.execute(queryGetTicketCount, agentID['booking_agent_id'])
  ticketCount = cursor.fetchone()
  ticketCountVal = ticketCount['ticketCount']
  avgComm = 0
  # print ticketCount, totalCommVal
  if ticketCountVal != 0:
    avgComm = totalCommVal/ticketCountVal

  cursor.close()  
  return render_template('agent.html', username=username, posts=data, totalComm=totalCommVal, avgComm=avgComm, ticketCount=ticketCountVal)      

@app.route('/searchPageAgent')
def searchPageAgent():
  return render_template('searchAgent.html')

@app.route('/searchAgent', methods=['POST'])
def searchAgent():
  username = session['username']
  cursor = conn.cursor()
  fromcity = request.form['fromcity']
  fromairport = request.form['fromairport']
  fromdate = request.form['fromdate']
  tocity = request.form['tocity']
  toairport = request.form['toairport']
  todate = request.form['todate']
  # Get booking_agent_id
  queryGetID = 'SELECT booking_agent_id FROM booking_agent WHERE email=%s'
  cursor.execute(queryGetID, username)
  agentID = cursor.fetchone()['booking_agent_id']
  # Main query  
  query = 'SELECT * FROM flight, airport, purchases, ticket \
          WHERE airport.airport_name=flight.departure_airport \
          AND flight.flight_num = ticket.flight_num AND flight.airline_name = ticket.airline_name\
          AND ticket.ticket_id = purchases.ticket_id\
          AND purchases.booking_agent_id = %s\
          AND airport.airport_city = %s \
          AND airport.airport_name = %s \
          -- AND flight.status = "Upcoming"\
          AND %s BETWEEN DATE_SUB(flight.departure_time, INTERVAL 2 DAY) AND DATE_ADD(flight.departure_time, INTERVAL 2 DAY) \
          AND %s BETWEEN DATE_SUB(flight.arrival_time, INTERVAL 2 DAY) AND DATE_ADD(flight.arrival_time, INTERVAL 2 DAY) \
          AND (flight.airline_name, flight.flight_num) in \
            (SELECT flight.airline_name, flight.flight_num FROM flight, airport \
            WHERE airport.airport_name=flight.arrival_airport \
            AND airport.airport_city = %s \
            AND airport.airport_name = %s)'
  cursor.execute(query, (agentID, fromcity, fromairport, fromdate, todate, tocity, toairport))
  data = cursor.fetchall()
  cursor.close()
  error = None
  if(data):
    return render_template('searchAgent.html', results=data)
  else:
    #returns an error message to the html page
    error = 'No results found'
    return render_template('searchAgent.html', error=error)   

@app.route('/commission', methods=['POST'])
def commission():
  username = session['username']
  cursor = conn.cursor()
  fromdate = request.form['fromdate']
  todate = request.form['todate']
  print(fromdate, todate)
  # Get booking_agent_id
  queryGetID = 'SELECT booking_agent_id FROM booking_agent WHERE email=%s'
  cursor.execute(queryGetID, username)
  agentID = cursor.fetchone()
  # print('~~~DEBUG: ', agentID)
  # Get total commsion in the past 30 days
  queryGetCommission = 'SELECT sum(price)*.10 as totalComm FROM purchases, ticket, flight \
                        WHERE purchases.ticket_id = ticket.ticket_id \
                        AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num \
                        AND purchases.purchase_date BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE) \
                        AND purchases.booking_agent_id = %s'
  cursor.execute(queryGetCommission, (fromdate, todate, agentID['booking_agent_id']))
  totalComm = cursor.fetchone()
  totalCommVal = 0
  if totalComm['totalComm'] != None:
    totalCommVal = totalComm['totalComm']
  # print('~~~DEBUG:: ', totalComm)
  # Get total tickets in the past 30 days 
  queryGetTicketCount = 'SELECT count(*) as ticketCount FROM purchases, ticket, flight \
                        WHERE purchases.ticket_id = ticket.ticket_id \
                        AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num \
                        AND purchases.purchase_date BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE) \
                        AND purchases.booking_agent_id = %s'
  cursor.execute(queryGetTicketCount, (fromdate, todate, agentID['booking_agent_id']))
  ticketCount = cursor.fetchone()
  ticketCountVal = ticketCount['ticketCount']  
  # print('~~~DEBUG: ', ticketCount)
  # avgComm = totalComm/ticketCount
  cursor.close()
  return render_template('commission.html', fromdate=fromdate, todate=todate, totalComm=totalCommVal, ticketCount=ticketCountVal)









