-- Test data 

delete from purchases;
delete from ticket;
delete from flight;
delete from airport; 
delete from airline_staff; 
delete from airplane;  
delete from airport; 
delete from airline; 
delete from booking_agent;
delete from customer; 

-- Airlines
insert into airline values("Emirates");
insert into airline values("Korea Air");
insert into airline values("Vietnam Airlines");
insert into airline values("Delta Airlines");
insert into airline values("Lufthansa");  
insert into airline values("All Nippon Airways");
insert into airline values("American Airlines");
insert into airline values("Air France");  

-- Airports
insert into airport values("Heathrow", "London");
insert into airport values("O'Hare", "Chicago");
insert into airport values("JFK", "NYC");
insert into airport values("Changi", "Singapore");
insert into airport values("Tan Son Nhat", "HCMC");
insert into airport values("Incheon", "Seoul");  
insert into airport values("DFW", "Dallas");
insert into airport values("Narita", "Tokyo");  

-- Airplanes
insert into airplane values("Emirates", 777, 250);
insert into airplane values("Korea Air", 777, 250);
insert into airplane values("Korea Air", 797, 250);
insert into airplane values("Lufthansa", 777, 250);
insert into airplane values("Air France", 787, 350);
insert into airplane values("All Nippon Airways", 797, 450);
insert into airplane values("Vietnam Airlines", 777, 500);
insert into airplane values("American Airlines", 350 ,500);
insert into airplane values("Delta Airlines", 777, 250);  

-- Flights
-- Summary: 
  -- JFK - O'Hare and vice versa
  -- Incheon - JFK
  -- Tan Son Nhat - JFK
  -- Narita - O'Hare
  -- JFK - DFW
insert into flight values("Emirates", 9911, "JFK",  "2017-06-19 22:30:00", "O'Hare", "2017-06-20 06:00:00", 800, "Upcoming", 777);
insert into flight values("Delta Airlines", 805, "O'Hare", "2017-04-03 20:45:00", "JFK", "2017-04-04 07:00:00", 499, "Upcoming", 777);
insert into flight values("Delta Airlines", 806, "O'Hare", "2017-04-02 19:45:00", "JFK",  "2017-04-02 23:00:00", 299, "Upcoming", 777);
insert into flight values("Korea Air", 77, "Incheon", "2017-04-30 19:45:00", "JFK",  "2017-05-01 23:00:00", 2990, "Upcoming", 777);
insert into flight values("Korea Air", 67, "Incheon", "2017-04-30 3:00:00", "JFK",  "2017-05-02 23:00:00", 1990, "Upcoming", 777);
insert into flight values("Korea Air", 97, "Incheon", "2017-04-30 7:00:00", "JFK",  "2017-04-30 23:00:00", 4990, "Upcoming", 797);  
insert into flight values("Vietnam Airlines", 103, "Tan Son Nhat", "2017-04-30 19:45:00", "JFK",  "2017-05-02 23:00:00", 1099, "Upcoming", 777);
insert into flight values("All Nippon Airways", 567, "Narita", "2017-05-19 19:45:00", "O'Hare",  "2017-05-20 23:00:00", 2990, "Upcoming", 797);
insert into flight values("Delta Airlines", 23, "JFK",  "2017-04-19 22:30:00", "DFW", "2017-04-20 06:00:00", 800, "Upcoming", 777);  
insert into flight values("Lufthansa", 57, "JFK",  "2017-04-19 22:30:00", "DFW", "2017-04-20 06:00:00", 800, "Upcoming", 777);  
insert into flight values("American Airlines", 789, "JFK",  "2017-04-19 22:30:00", "DFW", "2017-04-20 06:00:00", 800, "Upcoming", 350);    




-- c. Insert at least two customers with appropriate names and other attributes. 
-- Insert one booking agent with appropriate name and other attributes.
-- insert into customer values("bob.henderson@gmail.com", "Bob", "Bob1357", "55", "Jay St", "Brooklyn", "NY", "2123474071", "A12312448", "2021-12-12", "USA", "1960-01-01");
-- insert into customer values("marie.henderson@gmail.com", "Marie", "LoveBob1357", "55", "Jay St", "Brooklyn", "NY", "2123478928", "A12311348", "2021-12-12", "USA", "1965-05-06");
-- insert into booking_agent values("rachel.patrina@sta.org", "Ah$981", "S2736");
-- CREATE FROM WEB APP

-- e. Insert At least One airline Staff working for Emirates.
-- insert into airline_staff values("ncaffrey1", "N1ceTr!", "Neal", "Caffrey", "12-12-1980", "Emirates");
-- CREATE FROM WEB APP

-- g. Insert some tickets for corresponding flights. 
-- One customer buy ticket directly and one customer buy ticket using a booking agent.
-- insert into ticket values(123456, "Emirates", 9911);
-- insert into purchases values(123456, "hieu@gmail.com", null, "2015-03-05");
-- insert into ticket values(67890, "United Airlines", 805);
-- insert into purchases values(67890, "hieu@gmail.com", 67890, "2015-03-05");
-- insert into ticket values(987654, "Emirates", 9911);
-- insert into purchases values(987654, "mocha@gmail.com", null, "2015-03-05");