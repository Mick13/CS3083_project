create table Airport (
    code VARCHAR(3) PRIMARY KEY NOT NULL,
    -- 3 characters to indicate airport
    name VARCHAR(255),
    city VARCHAR(255),
    country VARCHAR(255),
    number_of_terminals INT,
    airport_type VARCHAR(15) CHECK (airport_type IN ('domestic', 'international', 'both'))
);

create table Airline (
    name VARCHAR(255) PRIMARY KEY
);

create table Airplane (
    identification_number VARCHAR(255) not NULL,
    airline_name VARCHAR(255) not NULL,
    number_of_seats INT,
    manufacturing_company VARCHAR(255),
    model_number VARCHAR(255),
    manufacturing_date DATE,
    age INT,
    PRIMARY KEY (identification_number, airline_name),
    FOREIGN KEY (airline_name) REFERENCES Airline(name)
    	on delete cascade
);

create table Maintenance_procedure (
    airline_name VARCHAR(255) NOT NULL,
    airplane_id VARCHAR(255) NOT NULL,
    start_date_time DATETIME NOT NULL,
    end_date_time DATETIME,
    PRIMARY KEY (airline_name, airplane_id, start_date_time),
    FOREIGN KEY (airline_name, airplane_id) REFERENCES Airplane (airline_name, identification_number)
    		on delete cascade
);



CREATE TABLE Flight (
    flight_number VARCHAR(255) NOT NULL,
    airline_name VARCHAR(255) NOT NULL,
    departure_airport VARCHAR(3) NOT NULL,
    departure_date_time DATETIME,
    arrival_airport VARCHAR(3),
    arrival_date_time DATETIME,
    base_price_of_ticket DECIMAL(10, 2),
    airplane_id VARCHAR(255),
    status VARCHAR(15) CHECK (card_type IN ('delayed', 'on time', 'canceled')),
    PRIMARY KEY (flight_number, airline_name, departure_date_time),
    FOREIGN KEY (airline_name) REFERENCES Airline(name),
    FOREIGN KEY (departure_airport) REFERENCES Airport(code),
    FOREIGN KEY (arrival_airport) REFERENCES Airport(code),
    FOREIGN KEY (airplane_id, airline_name) REFERENCES Airplane(identification_number, airline_name)
);


CREATE TABLE Customer (
    email_address VARCHAR(200) PRIMARY KEY NOT NULL,
    password VARCHAR(100),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    building_number INT,
    street_name VARCHAR(100),
    apartment_number INT,
    city VARCHAR(100), 
    state VARCHAR(100), 
    zip_code VARCHAR(100),
    date_of_birth DATE
    
);

CREATE TABLE Customer_Phone (
    email_address VARCHAR(200) not NULL,
    phone_number VARCHAR(15) not NULL,
    PRIMARY KEY (email_address, phone_number),
    FOREIGN KEY (email_address) REFERENCES Customer(email_address)
        on delete cascade
);

CREATE TABLE Customer_Passport (
    email_address VARCHAR(100) not NULL,
    passport_number VARCHAR(9) not NULL,
    passport_expiration DATE not NULL,
    passport_country VARCHAR(100) not NULL,
    PRIMARY KEY (email_address, passport_number),
    FOREIGN KEY (email_address) REFERENCES Customer(email_address)
    on delete cascade
);

CREATE TABLE Flight_Rating (
    flight_number VARCHAR(255) not NULL,
    airline_name VARCHAR(255) not NULL,
    departure_date_time DATETIME not NULL,
    customer_email VARCHAR(200) not NULL,
    rating INT(10),
    -- range
    comment VARCHAR(255),
    PRIMARY KEY (flight_number, airline_name, departure_date_time, customer_email),
    FOREIGN KEY (flight_number, airline_name, departure_date_time) REFERENCES Flight(flight_number, airline_name, departure_date_time),
    FOREIGN KEY (customer_email) REFERENCES Customer(email_address)
);

CREATE TABLE Ticket (
    ticket_ID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (ticket_ID),
    flight_number VARCHAR(255),
    departure_date_time DATETIME,
    airline_name VARCHAR(255),
    purchase_date_time DATETIME,
    base_ticket_price DECIMAL(10, 2),
    calculated_ticket_price DECIMAL(10, 2),
    customer_email VARCHAR(100),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    card_type VARCHAR(15) CHECK (card_type IN ('credit', 'debit')),
    card_number VARCHAR(19),
    name_on_card VARCHAR(100),
    expiration_date DATE,
    FOREIGN KEY (flight_number, airline_name, departure_date_time) REFERENCES Flight(flight_number, airline_name, departure_date_time)
        on delete cascade,
    FOREIGN KEY (customer_email) REFERENCES Customer(email_address)

);



CREATE TABLE Airline_Staff (
    username VARCHAR(50) PRIMARY KEY NOT NULL,
    password VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    airline_name VARCHAR(255),
    FOREIGN KEY (airline_name) REFERENCES Airline(name)

);


CREATE TABLE Airline_Staff_Phone (
    username VARCHAR(50) NOT NULL,
    phone_number VARCHAR(15) not NULL,
    PRIMARY KEY (username, phone_number),
    FOREIGN KEY (username) REFERENCES Airline_Staff(username)
    	on delete cascade
);

CREATE TABLE Airline_Staff_Email (
    username VARCHAR(50),
    email_address VARCHAR(100),
    PRIMARY KEY (username, email_address),
    FOREIGN KEY (username) REFERENCES Airline_Staff(username)
    	on delete cascade
);
