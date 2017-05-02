from flask import Flask, render_template, request, session, redirect, url_for
import pymysql.cursors
import datetime

from appdef import *

#Get the airline the staff member works for
def getStaffAirline():
    username = session['username']
    cursor = conn.cursor()
    #username is a primary key
    query = 'select airline_name from airline_staff where username = %s'
    cursor.execute(query, (username))
    #fetchall returns an array, each element is a dictionary
    airline = cursor.fetchall()[0]['airline_name']
    cursor.close()
    
    return airline

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
    if data:
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
    
@app.route('/staffHome/searchFlights')
def searchFlightsPage():
    if authenticateStaff():
        cursor = conn.cursor()
        
        airline = getStaffAirline()
        
        query = 'select * from flight where airline_name = %s and ((departure_time between curdate() and date_add(curdate(), interval 30 day)) or (arrival_time between curdate() and date_add(curdate(), interval 30 day)))'
        cursor.execute(query, (airline))
        data = cursor.fetchall()
        
        cursor.close()
        
        error = request.args.get('error')
        return render_template('searchStaff.html', error=error, results=data)
    else:
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))

@app.route('/staffHome/searchFlights/city', methods=['POST'])
def searchFlightsCity():
    if authenticateStaff():
        cursor = conn.cursor()
        city = request.form['citysearchbox']
        airline = getStaffAirline()
        query = 'select * from flight,airport where (airport.airport_name=flight.departure_airport or airport.airport_name=flight.arrival_airport) and airport.airport_city=%s and airline_name=%s'
        cursor.execute(query, (city, airline))
        data = cursor.fetchall()
        cursor.close()
        error = None
        if data:
            return render_template('searchStaffResults.html', results=data)
        else:
            #returns an error message to the html page
            error = 'No results found'
            return redirect(url_for('searchFlightsPage', error=error))
    else:
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))

@app.route('/staffHome/searchFlights/airport', methods=['POST'])
def searchFlightsAirport():
    if authenticateStaff():
        cursor = conn.cursor()
        airport = request.form['airportsearchbox']
        airline = getStaffAirline()
        query = 'select * from flight where (departure_airport = %s or arrival_airport = %s) and airline_name=%s'
        cursor.execute(query, (airport, airport, airline))
        data = cursor.fetchall()
        cursor.close()
        error = None
        if data:
            return render_template('searchStaffResults.html', results=data)
        else:
            #returns an error message to the html page
            error = 'No results found'
            return redirect(url_for('searchFlightsPage', error=error))
    else:
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))
    
@app.route('/staffHome/searchFlights/date', methods=['POST'])
def searchFlightsDate():
    if authenticateStaff():
        begintime = request.form['begintime']
        endtime = request.form['endtime']
        
        if not validateDates(begintime, endtime):
            error = 'Invalid date range'
            return redirect(url_for('searchStaffPage', error=error))
        
        airline = getStaffAirline()
        
        cursor = conn.cursor()
        query = 'select * from flight where ((departure_time between %s and %s) or (arrival_time between %s and %s)) and airline_name=%s'
        cursor.execute(query, (begintime, endtime, begintime, endtime, airline))
        data = cursor.fetchall()
        cursor.close()
        error = None
        if data:
            return render_template('searchStaffResults.html', results=data)
        else:
            #returns an error message to the html page
            error = 'No results found'
            return redirect(url_for('searchStaffPage', error=error))
    else:
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))
    
@app.route('/staffHome/searchFlights/customers', methods=['POST'])
def searchFlightsCustomer():
    if authenticateStaff():
        flightnum = request.form['flightsearchbox']
        airline = getStaffAirline()
        
        cursor = conn.cursor()
        query = 'select customer_email from purchases natural join ticket where flight_num = %s and airline_name=%s'
        cursor.execute(query, (flightnum, airline))
        data = cursor.fetchall()
        cursor.close()
        if data:
            return render_template('searchStaffResults.html', customerresults=data, flightnum=flightnum)
        else:
            #returns an error message to the html page
            error = 'No results found'
            return redirect(url_for('searchFlightsPage', error=error))
    else:
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))
    
@app.route('/staffHome/createFlight')
def createFlightPage():
    if authenticateStaff():
        airline = getStaffAirline()
        
        cursor = conn.cursor()
        query = 'select distinct airport_name from airport'
        cursor.execute(query)
        airportdata = cursor.fetchall()
        
        query = 'select distinct airplane_id from airplane where airline_name=%s'
        cursor.execute(query, (airline))
        airplanedata = cursor.fetchall()
        
        cursor.close()
        
        error = request.args.get('error')
        return render_template('createFlight.html', error=error, airportdata=airportdata, airplanedata=airplanedata)
    else:
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))

@app.route('/staffHome/createFlight/Auth', methods=['POST'])
def createFlight():
    if not authenticateStaff():
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))
    
    username = session['username']
    
    flightnum = request.form['flightnum']
    departport = request.form['departport']
    departtime = request.form['departtime']
    arriveport = request.form['arriveport']
    arrivetime = request.form['arrivetime']
    price = request.form['price']
    status = "Upcoming"
    airplaneid = request.form['airplanenum']
    
    if not validateDates(departtime, arrivetime):
            error = 'Invalid date range'
            return redirect(url_for('createFlightPage', error=error))
    
    airline = getStaffAirline()
    
    #Check that airplane is valid
    cursor = conn.cursor()
    query = 'select * from airplane where airplane_id = %s'
    cursor.execute(query, (airplaneid))
    data = cursor.fetchall()
    if not data:
        error = 'Invalid Airplane ID'
        return redirect(url_for('createFlightPage', error=error))
    
    query = 'insert into flight values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (airline, flightnum, departport, departtime, arriveport, arrivetime, price, status, airplaneid))
    conn.commit()
    cursor.close()
    
    return redirect(url_for('staffHome', message="Operation Successful"))

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
    cursor = conn.cursor()
    flightnum = request.form['flightnum']
    status = request.form['status']
    if not status:
        error = 'Did not select new status'
        return redirect(url_for('changeFlightStatusPage', error=error))
    
    airline = getStaffAirline()
    
    #Check that the flight is from the same airline as the staff
    query = 'select * from flight where flight_num = %s and airline_name = %s'
    cursor.execute(query, (flightnum, airline))
    data = cursor.fetchall()
    if not data:
        error = 'Incorrect permission - can only change flights from your airline'
        return redirect(url_for('changeFlightStatusPage', error=error))
    
    #Update the specified flight
    query = 'update flight set status=%s where flight_num=%s and airline_name = %s'
    cursor.execute(query, (status, flightnum, airline))
    conn.commit()
    cursor.close()
    
    return redirect(url_for('staffHome', message="Operation Successful"))
    
@app.route('/staffHome/addAirplane')
def addAirplanePage():
    if authenticateStaff():
        error = request.args.get('error')
        return render_template('addAirplane.html', error=error)
    else:
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))

@app.route('/staffHome/addAirplane/confirm', methods=['POST'])
def addAirplane():
    if not authenticateStaff():
        error = 'Invalid Credentials'
        return redirect(url_for('errorpage', error=error))
    
    username = session['username']
    
    planeid = request.form['id']
    seats = request.form['seats']
    airline = getStaffAirline()
    
    #Check if planeid is not taken
    cursor = conn.cursor()
    query = 'select * from airplane where airplane_id = %s'
    cursor.execute(query, (planeid))
    data = cursor.fetchall()
    
    if data:
        error = "Airplane ID already taken"
        return redirect(url_for('addAirplanePage', error=error))
    
    #Insert the airplane
    query = 'insert into airplane values (%s, %s, %s)'
    cursor.execute(query, (airline, planeid, seats))
    conn.commit()
    
    #Get a full list of airplanes
    query = 'select * from airplane where airline_name = %s'
    cursor.execute(query, (airline))
    data = cursor.fetchall()
    cursor.close()
    
    return render_template('addAirplaneConfirm.html', results=data)

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

@app.route('/staffHome/viewAgents')
def viewAgentsPage():
    if authenticateStaff():
        error = request.args.get('error')
        return render_template('viewAgents.html', error=error)
    else:
        error = "Invalid Credentials"
        return redirect(url_for('errorpage', error=error))

@app.route('/staffHome/viewAgents/sales', methods=['POST'])
def viewAgentsSales():
    if authenticateStaff():
        daterange = request.form['range']
        airline = getStaffAirline()
        
        cursor = conn.cursor()
        query = 'select email,count(ticket_id) as sales from booking_agent natural join purchases natural join ticket where purchase_date >= date_sub(curdate(), interval 1 ' + daterange + ') and airline_name=%s group by email order by sales'
        cursor.execute(query, (airline))
        data = cursor.fetchall()
        cursor.close()
        
        #Use only the top 5 sellers
        #Python will not break if we try to access a range that extends beyond the end of the array
        return render_template('viewAgentsSales.html', results = data[0:5], date=daterange)
        
    else:
        error = "Invalid Credentials"
        return redirect(url_for('errorpage', error=error))

@app.route('/staffHome/viewAgents/commission')
def viewAgentsCommission():
    if authenticateStaff():
        airline = getStaffAirline()
        
        cursor = conn.cursor()
        query = 'select email,sum(flight.price)*0.1 as commission from booking_agent natural join purchases natural join ticket natural join flight where purchase_date >= date_sub(curdate(), interval 1 year) and airline_name=%s group by email order by commission'
        cursor.execute(query, (airline))
        data = cursor.fetchall()
        cursor.close()
        
        #Use only the top 5 sellers
        #Python will not break if we try to access a range that extends beyond the end of the array
        return render_template('viewAgentsCommission.html', results = data[0:5])
    else:
        error = "Invalid Credentials"
        return redirect(url_for('errorpage', error=error))

@app.route('/staffHome/viewCustomers')
def viewCustomersPage():
    if authenticateStaff():
        airline = getStaffAirline()
        
        cursor = conn.cursor()
        query = 'select customer_email, count(ticket_id) as customerpurchases \
                from purchases natural join ticket \
                where airline_name= %s \
                and purchase_date >= date_sub(curdate(), interval 1 year) group by customer_email \
                having customerpurchases \
                  >= all (select count(ticket_id) \
                  from purchases natural join ticket \
                  where airline_name = %s \
                  and purchase_date >= date_sub(curdate(), interval 1 year) GROUP by customer_email)'
        cursor.execute(query, (airline, airline))
        data = cursor.fetchall()
        cursor.close()
        
        error = request.args.get('error')
        return render_template('viewCustomers.html', error=error, results=data)
    else:
        error = "Invalid Credentials"
        return redirect(url_for('errorpage', error=error))

@app.route('/staffHome/viewCustomers/results', methods=['POST'])
def viewCustomers():
    if authenticateStaff():
        airline = getStaffAirline()
        customer = request.form['email']
        
        cursor = conn.cursor()
        query = 'select distinct flight_num from purchases natural join ticket where airline_name = %s and customer_email=%s'
        cursor.execute(query, (airline, customer))
        data = cursor.fetchall()
        cursor.close()
        
        return render_template('viewCustomersResults.html', results=data, customer=customer)
        
    else:
        error = "Invalid Credentials"
        return redirect(url_for('errorpage', error=error))
    
@app.route('/staffHome/viewReports')
def viewReportsPage():
    if authenticateStaff():
        airline = getStaffAirline()
        currentmonth = datetime.datetime.now().month
        monthtickets = []
        
        cursor = conn.cursor()
        for i in range(0, 12):
            query = 'select count(ticket_id) as sales \
            from purchases natural join ticket \
            where year(purchase_date) = year(curdate() - interval ' + str(i) + ' month) \
            and month(purchase_date) = month(curdate() - interval ' + str(i) + ' month) \
            and airline_name=%s'
            cursor.execute(query, (airline))
            data = cursor.fetchall()
            salemonth = ((currentmonth - (i+1)) % 12) + 1
            print data[0]['sales']
            monthtickets.append([data[0]['sales'], salemonth])
        
        cursor.close()
        
        return render_template('viewReports.html', results=monthtickets)
    else:
        error = "Invalid Credentials"
        return redirect(url_for('errorpage', error=error))
        
@app.route('/staffHome/viewReports/dates', methods=['POST'])
def viewReportsDates():
    if authenticateStaff():
        airline = getStaffAirline()
        begintime = request.form['begintime']
        endtime = request.form['endtime']
        
        if not validateDates(begintime, endtime):
            error = 'Invalid date range'
            return redirect(url_for('viewReportsPage', error=error))
        
        cursor = conn.cursor()
        query = 'select count(ticket_id) as sales from purchases natural join ticket where airline_name=%s and purchase_date between %s and %s'
        cursor.execute(query, (airline, begintime, endtime))
        data = cursor.fetchall()
        cursor.close()
        
        return render_template('viewReportsDate.html', sales=data[0]['sales'], begintime=begintime, endtime=endtime)
    else:
        error = "Invalid Credentials"
        return redirect(url_for('errorpage', error=error))
    
@app.route('/staffHome/viewReports/past', methods=['POST'])
def viewReportsPast():
    if authenticateStaff():
        airline = getStaffAirline()
        daterange = request.form['range']
        
        cursor = conn.cursor()
        query = 'select count(ticket_id) as sales from purchases natural join ticket where airline_name=%s and purchase_date >= date_sub(curdate(), interval 1 ' + daterange + ')'
        cursor.execute(query, (airline))
        data = cursor.fetchall()
        cursor.close()
        
        return render_template('viewReportsPast.html', sales=data[0]['sales'], datetime=daterange)
    else:
        error = "Invalid Credentials"
        return redirect(url_for('errorpage', error=error))