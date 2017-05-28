# All Use Cases and Queries

## Register
Create new customer, agent, staff by inserting new entries into the corresponding tables. Passwords are MD5 hashed.
```sql
INSERT INTO customer VALUES(%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)
INSERT INTO booking_agent VALUES(%s, md5(%s), %s)
INSERT INTO airline_staff VALUES(%s, md5(%s), %s, %s, %s, %s)
```

## Login
Login check for customer, agent, staff by selecting from the corresponding tables with the correct username and password. Passwords are MD5 hashed.
```sql
SELECT * FROM airline_staff WHERE username = %s and password = md5(%s)
SELECT * FROM customer WHERE email = %s and password = md5(%s)
SELECT * FROM booking_agent WHERE email = %s and password = md5(%s)
```

## Customer
Get all Upcoming flights info for a customer 
```sql
SELECT purchases.ticket_id, ticket.airline_name, ticket.flight_num, departure_airport, departure_time, arrival_airport, arrival_time 
FROM purchases, ticket, flight 
WHERE purchases.ticket_id = ticket.ticket_id 
AND ticket.airline_name = flight.airline_name 
AND ticket.flight_num = flight.flight_num 
AND customer_email = %s AND departure_time > curdate()
```

Search for customer flights by source city, aiport and destination city, airport and date. For the date range, we add an extra flexibility of 2 days before or after the specified dates.
```sql
SELECT * FROM flight, airport, purchases, ticket 
WHERE airport.airport_name=flight.departure_airport 
AND flight.flight_num = ticket.flight_num AND flight.airline_name = ticket.airline_name
AND ticket.ticket_id = purchases.ticket_id
AND purchases.customer_email = %s
AND airport.airport_city = %s 
AND airport.airport_name = %s 
-- AND flight.status = "Upcoming" 
AND %s BETWEEN DATE_SUB(flight.departure_time, INTERVAL 2 DAY) AND DATE_ADD(flight.departure_time, INTERVAL 2 DAY) 
AND %s BETWEEN DATE_SUB(flight.arrival_time, INTERVAL 2 DAY) AND DATE_ADD(flight.arrival_time, INTERVAL 2 DAY) 
AND (flight.airline_name, flight.flight_num) in 
  (SELECT flight.airline_name, flight.flight_num FROM flight, airport 
  WHERE airport.airport_name=flight.arrival_airport 
  AND airport.airport_city = %s 
  AND airport.airport_name = %s)
```

Search flights for customer to purchase. The search part is similar to the above query, but we also check for the seats left for the flight to make sure that the flight isn't overbooked (unlike United). 
```sql
SELECT distinct f.airline_name, f.flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, airplane_id 
FROM flight as f, airport 
WHERE airport.airport_name=f.departure_airport 
AND airport.airport_city = %s 
AND airport.airport_name = %s 
AND %s BETWEEN DATE_SUB(f.departure_time, INTERVAL 2 DAY) AND DATE_ADD(f.departure_time, INTERVAL 2 DAY)
AND %s BETWEEN DATE_SUB(f.arrival_time, INTERVAL 2 DAY) AND DATE_ADD(f.arrival_time, INTERVAL 2 DAY)
AND (f.airline_name, f.flight_num) in 
  (SELECT flight.airline_name, flight.flight_num FROM flight, airport 
  WHERE airport.airport_name=flight.arrival_airport 
  AND airport.airport_city = %s 
  AND airport.airport_name = %s) 
AND (SELECT DISTINCT seats 
    FROM flight, airplane 
    WHERE flight.airplane_id = airplane.airplane_id AND flight.airline_name = airplane.airline_name 
    AND flight.airline_name = f.airline_name AND flight.flight_num = f.flight_num) 
    >= (SELECT COUNT(*) 
    FROM ticket 
    WHERE ticket.airline_name = f.airline_name AND ticket.flight_num = f.flight_num)
```

Purchase new tickets. Add new tickets and also update the purchase table for the customer.
```sql
INSERT INTO ticket VALUES(%s, %s, %s)
INSERT INTO purchases VALUES(%s, %s, %s, CURDATE())
```

## Booking Agent
All search and purchase queries are very similar to those of a customer. I won't include them here to avoid redundancy. The different queries for a booking agent is with finding the commision and tickets they bought. 

Get total commission in the past 30 days
```sql
SELECT sum(price)*.10 as totalComm FROM purchases, ticket, flight 
WHERE purchases.ticket_id = ticket.ticket_id 
AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num 
AND purchases.purchase_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE() 
AND purchases.booking_agent_id = %s
```

Get the number of tickets bought in the past 30 days
```sql
SELECT count(*) as ticketCount FROM purchases, ticket, flight 
WHERE purchases.ticket_id = ticket.ticket_id 
AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num 
AND purchases.purchase_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE() 
AND purchases.booking_agent_id = %s
```

Get booking_agent_id from booking agent's email
```sql
SELECT booking_agent_id FROM booking_agent WHERE email=%s
```

Get commision and ticket in a specified date range
```sql
SELECT sum(price)*.10 as totalComm FROM purchases, ticket, flight 
WHERE purchases.ticket_id = ticket.ticket_id 
AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num 
AND purchases.purchase_date BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE) 
AND purchases.booking_agent_id = %s
```
```sql
SELECT count(*) as ticketCount FROM purchases, ticket, flight 
WHERE purchases.ticket_id = ticket.ticket_id 
AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num 
AND purchases.purchase_date BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE) 
AND purchases.booking_agent_id = %s
```

## Public Info
Search for flight based on city
```sql
SELECT *
FROM flight,airport
WHERE (airport.airport_name=flight.departure_airport OR airport.airport_name=flight.arrival_airport)
AND airport.airport_city=%s
AND (departure_time >= curtime() OR arrival_time >= curtime())
```

Search for flight based on airport
```sql
SELECT *
FROM flight
WHERE (departure_airport = %s OR arrival_airport = %s)
AND (departure_time >= curtime() OR arrival_time >= curtime())
```

Search for flight based on a range of dates
```sql
SELECT *
FROM flight
WHERE ((departure_time BETWEEN %s AND %s) OR (arrival_time BETWEEN %s and %s))
AND (departure_time >= curtime() OR arrival_time >= curtime())
```

## Airline Staff

Authenticating the staff member before performing any actions
```sql
SELECT airline_name
FROM airline_staff
WHERE username = %s
```
Getting the airline that the staff member works for
```sql
SELECT airline_name
FROM airline_staff
WHERE username = %s
```

### View Flights

Get flights from the next 30 days from the airline that the staff member works for
```sql
SELECT *
FROM flight
WHERE airline_name = %s
AND ((departure_time BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY))
OR (arrival_time BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)))
```

Search for flights based on city that are from the staff's airline
```sql
SELECT *
FROM flight,airport
WHERE (airport.airport_name=flight.departure_airport OR airport.airport_name=flight.arrival_airport)
AND airport.airport_city=%s
AND airline_name=%s
```

Search for flights based on airport that are from the staff's airline
```sql
SELECT *
FROM flight
WHERE (departure_airport = %s OR arrival_airport = %s) AND airline_name=%s
```

Search for flights based on a range of dates that are from the staff's airline
```sql
SELECT *
FROM flight
WHERE ((departure_time BETWEEN %s AND %s) 
OR (arrival_time BETWEEN %s AND %s))
AND airline_name=%s
```

Search for customers that are on the specified flight
```sql
SELECT customer_email 
FROM purchases NATURAL JOIN ticket 
WHERE flight_num = %s
AND airline_name=%s
```

### Create Flight

Get all airports and airplaines to aid with creating a flight
```sql
SELECT DISTINCT airport_name FROM airport
SELECT DISTINCT airplane_id FROM airplane WHERE airline_name=%s
```

Validate airplane and insert data
```sql
SELECT * FROM airplane WHERE airplane_id = %s
INSERT INTO flight VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
```

### Change Flight Status

Check that a valid flight exists, then update the row in the table
```sql
SELECT * FROM flight WHERE flight_num = %s AND airline_name = %s
UPDATE flight SET status=%s WHERE flight_num=%s AND airline_name = %s
```

### Add Airplane

Check if the airplane id is open, then insert the new plane
```sql
SELECT * FROM airplane WHERE airplane_id = %s
INSERT INTO airplane VALUES (%s, %s, %s)
```

### Add Airport

Insert the given airport
```sql
INSERT INTO airport VALUES (%s, %s)
```

### View Agents

List the number of tickets each agent has sold, sorted by number sold.
Extracting the top 5 sellers is done in python
```sql
SELECT email,COUNT(ticket_id) AS sales 
FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
WHERE purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 ' + daterange + ')
AND airline_name=%s
GROUP BY email ORDER BY sales
```

List the total commission each agent has earned, sorted by highest earned.
Assumes 10% commission, and extracting top 5 sellers is done in python.
```sql
SELECT email,SUM(flight.price)*0.1 AS commission
FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight
WHERE purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) 
AND airline_name=%s
GROUP BY email ORDER BY commission
```

### View Customers

Get the most frequent customer (based on purchases from last year)
```sql
SELECT customer_email, COUNT(ticket_id) AS customerpurchases
FROM purchases NATURAL JOIN ticket
WHERE airline_name = %s
AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY customer_email
HAVING customerpurchases >= ALL
    (SELECT COUNT(ticket_id)
    FROM purchases NATURAL JOIN ticket
    WHERE airline_name = %s
    AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    GROUP BY customer_email)
```

Find which flights the customer has flown on
```sql
SELECT DISTINCT flight_num 
FROM purchases NATURAL JOIN ticket
WHERE airline_name = %s
AND customer_email=%s
```

### View Reports

Gets the number of tickets sold in each month for last year.
Used to generate the bar graph in the home page for viewing reports.
Query is run 12 times, once for each month. Each loop, the current date is
subtracted by *i* months and all tickets sold in the resulting month is then found.
```sql
SELECT COUNT(ticket_id) AS sales
FROM purchases NATURAL JOIN ticket
WHERE YEAR(purchase_date) = YEAR(CURDATE() - INTERVAL ' + str(i) + ' MONTH) \
AND MONTH(purchase_date) = MONTH(CURDATE() - INTERVAL ' + str(i) + ' MONTH) \
AND airline_name=%s
```

Get the number of tickets sold in the given date range
```sql
SELECT COUNT(ticket_id) AS sales
FROM purchases NATURAL JOIN ticket 
WHERE airline_name=%s 
AND purchase_date BETWEEN %s AND %s
```

Get the number of tickets sold in either the past year or the past month, whichever
is selected by the user
```sql
SELECT COUNT(ticket_id) AS sales 
FROM purchases NATURAL JOIN ticket 
WHERE airline_name=%s 
AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 ' + daterange + ')
```