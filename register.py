from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

from appdef import app, conn

@app.route('/registerCustomer')
def registerCustomer():
  return render_template('registerCustomer.html')

#Authenticates the register
@app.route('/registerAuthCustomer', methods=['GET', 'POST'])
def registerAuthCustomer():
  #grabs information from the forms
  email = request.form['email']
  name = request.form['name']
  password = request.form['password']
  building_number = request.form['building_number']
  street = request.form['street']
  city = request.form['city']
  state = request.form['state']
  phone_number = request.form['phone_number']
  passport_number = request.form['passport_number']
  passport_expiration = request.form['passport_expiration']
  passport_country = request.form['passport_country']
  date_of_birth = request.form['date_of_birth']

  #cursor used to send queries
  cursor = conn.cursor()
  #executes query
  query = 'SELECT * FROM customer WHERE email = %s'
  cursor.execute(query, (email))
  #stores the results in a variable
  data = cursor.fetchone()
  #use fetchall() if you are expecting more than 1 data row
  error = None
  if(data):
    #If the previous query returns data, then user exists
    error = "This user already exists"
    return render_template('registerCustomer.html', error = error)
  else:
    ins = 'INSERT INTO customer VALUES(%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(ins, (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
    conn.commit()
    cursor.close()
    return render_template('index.html')


#Define route for register
@app.route('/registerAgent')
def registerAgent():
  return render_template('registerAgent.html')

@app.route('/registerAuthAgent', methods=['GET', 'POST'])
def registerAuthAgent():
  email = request.form['email']
  password = request.form['password']
  booking_agent_id = request.form['booking_agent_id']

  cursor = conn.cursor()
  query = 'SELECT * FROM booking_agent WHERE email = %s'
  cursor.execute(query, (email))
  data = cursor.fetchone()
  error = None
  if(data):
    error = "This user already exists"
    return render_template('registerAgent.html', error = error)
  else:
    ins = 'INSERT INTO booking_agent VALUES(%s, md5(%s), %s)'
    cursor.execute(ins, (email, password, booking_agent_id))
    conn.commit()
    cursor.close()
    return render_template('index.html')      

@app.route('/registerStaff')
def registerStaff():
  return render_template('registerStaff.html')  

@app.route('/registerAuthStaff', methods=['GET', 'POST'])
def registerAuthStaff():
  username = request.form['username']
  password = request.form['password']
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  date_of_birth = request.form['date_of_birth']
  airline_name = request.form['airline_name']

  cursor = conn.cursor()
  query = 'SELECT * FROM airline_staff WHERE username = %s'
  cursor.execute(query, (username))
  data = cursor.fetchone()
  error = None
  if(data):
    error = "This user already exists"
    return render_template('registerStaff.html', error = error)
  else:
    ins = 'INSERT INTO airline_staff VALUES(%s, md5(%s), %s, %s, %s, %s)'
    cursor.execute(ins, (username, password, first_name, last_name, date_of_birth, airline_name))
    conn.commit()
    cursor.close()
    return render_template('index.html')     