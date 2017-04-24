#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       db='airline-booking',
                       port=8889,
                       # unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
  return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
  return render_template('login.html')

#Define route for register
@app.route('/registerAgent')
def registerAgent():
  return render_template('registerAgent.html')

@app.route('/registerCustomer')
def registerCustomer():
  return render_template('registerCustomer.html')

@app.route('/registerStaff')
def registerStaff():
  return render_template('registerStaff.html')  

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
  #grabs information from the forms
  username = request.form['username']
  password = request.form['password']
  usrtype = request.form['usrtype']

  #cursor used to send queries
  cursor = conn.cursor()
  #executes query
  if usrtype == 'staff':
    query = 'SELECT * FROM airline_staff WHERE username = %s and password = md5(%s)'
  elif usrtype == 'customer':
    query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
  else:
    query = 'SELECT * FROM booking_agent WHERE email = %s and password = md5(%s)'

  cursor.execute(query, (username, password))
  #stores the results in a variable
  data = cursor.fetchone()
  #use fetchall() if you are expecting more than 1 data row
  cursor.close()
  error = None
  if(data):
    #creates a session for the the user
    #session is a built in
    session['username'] = username
    if usrtype == 'staff':
      return redirect(url_for('staffHome'))
    elif usrtype == 'customer':
      return redirect(url_for('customerHome'))
    else:
      return redirect(url_for('agentHome'))
    
  else:
    #returns an error message to the html page
    error = 'Invalid login or username'
    return render_template('login.html', error=error)

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

@app.route('/home')
def home():
  username = session['username']
  cursor = conn.cursor();
  query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
  cursor.execute(query, (username))
  data = cursor.fetchall()
  cursor.close()
  return render_template('home.html', username=username, posts=data)

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
    
@app.route('/staffHome')
def staffHome():
  return render_template('staff.html')

@app.route('/agentHome')
def agentHome():
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
  return render_template('agent.html', username=username, posts=data)

@app.route('/post', methods=['GET', 'POST'])
def post():
  username = session['username']
  cursor = conn.cursor();
  blog = request.form['blog']
  query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
  cursor.execute(query, (blog, username))
  conn.commit()
  cursor.close()
  return redirect(url_for('home'))

@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/')
    
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
  app.run('127.0.0.1', 5000, debug = True)
