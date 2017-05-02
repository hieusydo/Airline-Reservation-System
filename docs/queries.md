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
ELECT count(*) as ticketCount FROM purchases, ticket, flight 
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

## Airline Staff

