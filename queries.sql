-- View upcoming flight of a customer
SELECT purchases.ticket_id, departure_airport, departure_time, arrival_airport, arrival_time
FROM purchases, ticket, flight
WHERE purchases.ticket_id = ticket.ticket_id 
AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num
AND customer_email = %s AND departure_time > curdate()

-- View upcoming flight of a an agent
SELECT customer_email, purchases.ticket_id, departure_airport, departure_time, arrival_airport, arrival_time
FROM purchases, ticket, flight, booking_agent
WHERE purchases.ticket_id = ticket.ticket_id 
AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num
AND purchases.booking_agent_id = booking_agent.booking_agent_id
AND booking_agent.email = %s AND departure_time > curdate()

-- Find flight based on arrival and departure city/time
