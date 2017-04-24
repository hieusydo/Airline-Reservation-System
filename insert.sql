-- Hieu Do (hsd258)
-- Course Project - Part 2 

delete from airport; 
delete from airline_staff; 
delete from airplane;  
delete from airport; 
delete from flight; 
delete from purchases;
delete from ticket; 
delete from airline; 
delete from booking_agent;
delete from customer; 
-- a. One Airline name "Emirates".
insert into airline values("Emirates");
insert into airline values("United Airlines");

-- b. At least Two airports named "JFK" in NYC and "Chicago International Airport" in Chicago.
insert into airport values("JFK", "NYC");
insert into airport values("Chicago International Airport", "Chicago");

-- c. Insert at least two customers with appropriate names and other attributes. 
-- Insert one booking agent with appropriate name and other attributes.
-- insert into customer values("bob.henderson@gmail.com", "Bob", "Bob1357", "55", "Jay St", "Brooklyn", "NY", "2123474071", "A12312448", "2021-12-12", "USA", "1960-01-01");
-- insert into customer values("marie.henderson@gmail.com", "Marie", "LoveBob1357", "55", "Jay St", "Brooklyn", "NY", "2123478928", "A12311348", "2021-12-12", "USA", "1965-05-06");
-- insert into booking_agent values("rachel.patrina@sta.org", "Ah$981", "S2736");
-- CREATE FROM WEB APP

-- d. Insert at least two airplanes.
insert into airplane values("Emirates", "B777", 396);
insert into airplane values("United Airlines", "B767", 250);

-- e. Insert At least One airline Staff working for Emirates.
-- insert into airline_staff values("ncaffrey1", "N1ceTr!", "Neal", "Caffrey", "12-12-1980", "Emirates");
-- CREATE FROM WEB APP

-- f. Insert several flights with upcoming, in-progress, delayed statuses.
insert into flight values("Emirates", 9911, "JFK",  "2017-06-19 22:30:00", "Chicago International Airport", "2017-06-20 06:00:00", 800, "Upcoming", "B777");
insert into flight values("United Airlines", 805, "Chicago International Airport", "2017-04-03 20:45:00", "JFK", "2017-04-04 07:00:00", 499, "In-Progress", "B767");
insert into flight values("United Airlines", 806, "Chicago International Airport", "2017-04-02 19:45:00", "JFK",  "2017-04-02 23:00:00", 299, "Delayed", "B767");

-- g. Insert some tickets for corresponding flights. 
-- One customer buy ticket directly and one customer buy ticket using a booking agent.
insert into ticket values(123456, "Emirates", 9911);
insert into purchases values(123456, "hieu@gmail.com", null, "2015-03-05");
insert into ticket values(67890, "United Airlines", 805);
insert into purchases values(67890, "hieu@gmail.com", 67890, "2015-03-05");
insert into ticket values(987654, "Emirates", 9911);
insert into purchases values(987654, "mocha@gmail.com", null, "2015-03-05");