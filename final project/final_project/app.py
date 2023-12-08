from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import datetime, timedelta, date
import pymysql
import hashlib

app = Flask(__name__)
app.secret_key = 'secret_key_trial'

##configure
conn = pymysql.connect(host='localhost',
                           port=8889,
                           user='root',
                           password='root',
                           db='airport management',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        departure_date = request.form['departure_date']
        cursor = conn.cursor()
        today = datetime.now().date()

        query = """
                SELECT * FROM Flight 
                WHERE departure_airport = %s AND arrival_airport = %s AND DATE(departure_date_time) =  %s
                AND DATE(departure_date_time) >= %s
            """
        cursor.execute(query, (source, destination, departure_date, today))
        flights = cursor.fetchall()
        conn.commit()
        cursor.close()
        return render_template('home.html', flights=flights)
    else:

        return render_template('home.html')


@app.route('/login_staff')
def show_login_staff():
    return render_template("login_staff.html")


@app.route('/perform_login_staff', methods=['POST', 'GET'])
def process_login_staff():
    username = request.form['username']
    password = request.form['password'].encode()

    
    hashed_pass = hashlib.md5(password).hexdigest()

    cursor = conn.cursor()
    query_to_check = "SELECT * FROM Airline_Staff WHERE username = %s AND password = %s"
    cursor.execute(query_to_check, (username, hashed_pass))
    result = cursor.fetchone()
    conn.commit()
    cursor.close()

    if result:
        session['username'] = username
        return redirect(url_for('staff_home'))
    else:
        error_message = "Login Failed. Please check your credentials."
        return render_template("login_staff.html", error_message=error_message)



@app.route('/signup_staff')
def signup_staff():
    return render_template('signup_staff.html')

@app.route('/perform_signup_staff', methods=['POST', 'GET'])
def perform_signup_staff():
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    date_of_birth = request.form['date_of_birth']
    airline_name = request.form['airline_name']
    phone_number = request.form['phone_number']
    email_address = request.form['email_address']


    if not password:
        error_message = "Password is required."
        return render_template("signup_staff.html", error_message=error_message)

    hashed_pass = hashlib.md5(password.encode()).hexdigest()

    cursor = conn.cursor()
    # print("Received airline name:", airline_name)

    cursor.execute("SELECT name FROM Airline WHERE name = %s", (airline_name))
    airline_exists = cursor.fetchone()
    if not airline_exists:
        error_message = "Airline not found. Please enter a valid airline name."
        return render_template("signup_staff.html", error_message=error_message)
    
    cursor.execute("SELECT username FROM Airline_Staff WHERE username = %s", (username))
    username_exists = cursor.fetchone()
    if username_exists:
        error_message = "Username already exists."
        return render_template("signup_staff.html", error_message=error_message)
    
   
    query_to_add = "INSERT INTO Airline_Staff (username, password, first_name, last_name, date_of_birth, airline_name) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query_to_add, (username, hashed_pass, first_name, last_name,date_of_birth,airline_name))
    conn.commit()


    query_to_add = "INSERT INTO Airline_Staff_Phone (username, phone_number) VALUES (%s, %s)"
    cursor.execute(query_to_add, (username, phone_number))
    conn.commit()

    query_to_add = "INSERT INTO Airline_Staff_Email (username, email_address) VALUES (%s, %s)"
    cursor.execute(query_to_add, (username, email_address))
    conn.commit()

    #return redirect(url_for('staff_home'))
    #return redirect(url_for('login_staff'))
    return redirect('/login_staff')


@app.route('/staff_home', methods=['GET'])
def staff_home():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_staff'))
    return render_template('staff_home.html')


@app.route('/staff_flights', methods=['GET', 'POST'])
def staff_flights():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_staff'))

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM Airline_Staff WHERE username = %s", (username))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        return "No associated airline found."

    airline_name = result['airline_name']
    today = datetime.now().date()
    thirty_days = today + timedelta(days=30)

    query = "SELECT * FROM Flight WHERE airline_name = %s"
    parameters = [airline_name]

    if request.method == 'POST':
        source = request.form.get('source')
        destination = request.form.get('destination')
        departure_date = request.form.get('departure_date')
        arrival_date = request.form.get('arrival_date')

        if source:

            query += " AND departure_airport = %s"
            parameters.append(source)
        if destination:

            query += " AND arrival_airport = %s"
            parameters.append(destination)
        if departure_date:

            query += " AND DATE(departure_date_time) = %s"
            parameters.append(departure_date)
        if arrival_date:
    
            query += " AND DATE(arrival_date_time) = %s"
            parameters.append(arrival_date)
    else:
        query += " AND departure_date_time BETWEEN %s AND %s"
        parameters.extend([today, thirty_days])

    cursor.execute(query, parameters)
    flights = cursor.fetchall()
    cursor.close()

    return render_template('staff_flights.html', flights=flights)



@app.route('/view_flight_customers', methods=['GET', 'POST'])
def view_flight_customers():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_staff'))

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM Airline_Staff WHERE username = %s", (username))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        return "No associated airline found."

    airline_name = result['airline_name']
    if request.method == 'POST':
        flight_number = request.form.get('flight_number')
        query = """
            SELECT c.first_name, c.last_name, c.email_address 
            FROM Customer c
            JOIN Ticket t ON t.customer_email = c.email_address
            WHERE t.flight_number = %s AND t.airline_name = %s"""
            
        cursor.execute(query, (flight_number,airline_name))
        customers = cursor.fetchall()
        cursor.close()

        return render_template('view_flight_customers.html', customers=customers)
    else:
        return render_template('view_flight_customers.html')


@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_staff'))
    #print(username)

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM Airline_Staff WHERE username = %s", (username))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        return "No associated airline found."

    airline_name = result['airline_name']


    def retrive_flights(airline_name):
            today = datetime.now().date()
            thirty_days = today + timedelta(days=30)
            query = "SELECT * FROM Flight WHERE airline_name = %s AND departure_date_time BETWEEN %s AND %s"
            
            cursor.execute(query, (airline_name, today, thirty_days))
            return cursor.fetchall()

    if request.method == 'POST':
        # Extract data from form
        flight_number = request.form['flight_number']
        departure_airport = request.form['departure_airport']
        departure_date_time = request.form['departure_date_time']
        arrival_airport = request.form['arrival_airport']
        arrival_date_time = request.form['arrival_date_time']
        base_price_of_ticket = request.form['base_price_of_ticket']
        airplane_id = request.form['airplane_id']
        status = request.form['status']


        flights = retrive_flights(airline_name)

        cursor.execute("SELECT * FROM Airplane WHERE identification_number = %s AND airline_name = %s", (airplane_id, airline_name))
        result = cursor.fetchone()

        if not result:
            cursor.close()
            error_message = "Failed to add Flight. Airplane doesnt exist."
            return render_template("create_flight.html", flights=flights, error_message=error_message)
        

        cursor.execute("""SELECT * FROM  Maintenance_procedure 
                        WHERE airplane_id = %s AND
                        (%s BETWEEN start_date_time AND end_date_time) OR
                        (%s BETWEEN start_date_time AND end_date_time) """
                        ,(airplane_id, departure_date_time, arrival_date_time))
        
        result = cursor.fetchone()
        if result:
            cursor.close()
            error_message = "Failed to add Flight. Airplane is under maintenance."
            return render_template("create_flight.html", flights=flights, error_message=error_message)


        query_Flight_id_check = "SELECT * FROM Flight WHERE flight_number = %s AND airline_name = %s"
        cursor.execute(query_Flight_id_check, (flight_number,airline_name))
        result = cursor.fetchone()
        

        if result:
            cursor.close()
            #if that flight already exisits
            error_message = "Failed to add Flight. Flight ID exists."
            return render_template("create_flight.html", flights=flights, error_message=error_message)


        # Insert data into the database
        query = """INSERT INTO Flight (flight_number, airline_name, departure_airport, 
                  departure_date_time, arrival_airport, arrival_date_time, 
                  base_price_of_ticket, airplane_id, status) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        cursor.execute(query, (flight_number, airline_name, departure_airport, 
                               departure_date_time, arrival_airport, arrival_date_time, 
                               base_price_of_ticket, airplane_id, status))
        conn.commit()

        success_message = "Flight added successfully!"
        cursor.close()

        return render_template("create_flight.html", flights=flights, success_message=success_message)
    else:
        cursor = conn.cursor()
        flights = retrive_flights(airline_name)
        cursor.close()
        return render_template('create_flight.html', flights=flights)
    


@app.route('/change_flight_status', methods=['POST', 'GET'])
def change_flight_status():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_staff'))
    
    if request.method == 'POST':

        cursor = conn.cursor()
        cursor.execute("SELECT airline_name FROM Airline_Staff WHERE username = %s", (username))
        result = cursor.fetchone()

        if not result:
            cursor.close()
            return "No associated airline found."

        airline_name = result['airline_name']
        flight_number = request.form['flight_number']
        new_status = request.form['status']


        cursor = conn.cursor()
        query_Flight_id_check = "SELECT * FROM Flight WHERE flight_number = %s AND airline_name = %s"
        cursor.execute(query_Flight_id_check, (flight_number,airline_name))
        result = cursor.fetchone()
        conn.commit()
        

        if not result:
            #flight doesnt exist
            error_message = "Failed to update Flight. Flight doesnt exist."
            cursor.close()
            return render_template("change_flight_status.html", error_message=error_message)
            

        query = "UPDATE Flight SET status = %s WHERE flight_number = %s AND airline_name = %s"
        cursor.execute(query, (new_status, flight_number, airline_name))
        conn.commit()
        cursor.close()

        success_message = "Flight status updated successfully."
        return render_template("change_flight_status.html", success_message=success_message)
    return render_template("change_flight_status.html")



@app.route('/add_airplane', methods=['GET', 'POST'])
def add_plane():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_staff'))

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM Airline_Staff WHERE username = %s", (username))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        return "No associated airline found."

    airline_name = result['airline_name']

    if request.method == 'POST':
        # Extract data from form
        airplane_id = request.form['identification_number']
        number_of_seats = request.form['number_of_seats']
        manufacturing_company  = request.form['manufacturing_company']
        model_number  = request.form['model_number']
        manufacturing_date  = request.form['manufacturing_date']
        
        ##https://docs.python.org/3/library/datetime.html

        manufacturing_year = int(manufacturing_date[:4])
        current_year = date.today().year
        age = current_year - manufacturing_year


        cursor = conn.cursor()
        query_plane_id_check = "SELECT * FROM Airplane WHERE identification_number = %s"
        cursor.execute(query_plane_id_check, (airplane_id))
        result = cursor.fetchone()
        conn.commit()
        cursor.close()

        if result:
            error_message = "Failed to add Flight. Airplane already exist."
            return render_template("add_airplane.html", error_message=error_message)
        
        # Insert data into the database
        cursor = conn.cursor()
        query = """INSERT INTO Airplane (identification_number, airline_name, number_of_seats, 
                  manufacturing_company, model_number, manufacturing_date, 
                  age) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (airplane_id, airline_name, number_of_seats, 
                               manufacturing_company, model_number, manufacturing_date, 
                               age))
        conn.commit()

        success_message = "Airplane added successfully!"


        query = "SELECT * FROM Airplane WHERE airline_name = %s"
        cursor.execute(query, (airline_name))
        airplanes = cursor.fetchall()
        cursor.close()

        return render_template("display_planes.html", success_message=success_message, airplanes = airplanes)
    else:
        return render_template('add_airplane.html')
    
@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_staff'))
    
    cursor = conn.cursor()
    query = "SELECT * FROM Airport"
    cursor.execute(query)
    airports = cursor.fetchall()
    cursor.close()
    

    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        city  = request.form['city']
        country  = request.form['country']
        number_of_terminals = request.form['number_of_terminals']
        airport_type = request.form['airport_type']

        cursor = conn.cursor()
        query_airport_code_check = "SELECT * FROM Airport WHERE code = %s"
        cursor.execute(query_airport_code_check, (code))
        result = cursor.fetchone()
        conn.commit()
        
        if result:
            cursor.close()
            error_message = "Failed to add Airport. Airport already exist."
            return render_template("add_airport.html", error_message=error_message , airports= airports)
        
        query = """INSERT INTO Airport (code, name, city, 
                  country, number_of_terminals, airport_type) 
                  VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (code, name, city, country, number_of_terminals, airport_type))
        conn.commit()

        query = "SELECT * FROM Airport"
        cursor.execute(query)
        airports = cursor.fetchall()
        cursor.close()


        success_message = "Airport added successfully!"
        return render_template('add_airport.html' , success_message=success_message, airports= airports)
    else:

        return render_template('add_airport.html' , airports= airports)
        
@app.route('/view_flight_ratings', methods=['GET', 'POST'])
def view_flight_ratings():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_staff'))

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM Airline_Staff WHERE username = %s", (username))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        return "No associated airline found."

    airline_name = result['airline_name']
    if request.method == 'POST':
        flight_number = request.form.get('flight_number') 
        query = """
                SELECT fr.flight_number, fr.customer_email, fr.rating, fr.comment,  avg_ratings.average_rating
                FROM Flight_Rating fr
                JOIN (
                    SELECT flight_number, AVG(rating) as average_rating
                    FROM Flight_Rating
                    WHERE airline_name = %s AND flight_number = %s
                    GROUP BY flight_number
                ) avg_ratings ON fr.flight_number = avg_ratings.flight_number
                WHERE fr.airline_name = %s AND fr.flight_number = %s
            """
        cursor.execute(query, (airline_name, flight_number, airline_name, flight_number))

    else:
        query = """
            SELECT fr.flight_number, fr.customer_email, fr.rating, fr.comment, avg_ratings.average_rating
            FROM Flight_Rating fr
            JOIN (
                SELECT flight_number, AVG(rating) as average_rating
                FROM Flight_Rating
                WHERE airline_name = %s
                GROUP BY flight_number
            ) avg_ratings ON fr.flight_number = avg_ratings.flight_number
            WHERE fr.airline_name = %s
    """
        cursor.execute(query, (airline_name, airline_name))
    ratings = cursor.fetchall()
    cursor.close()

    return render_template('view_flight_ratings.html', ratings=ratings)

@app.route('/schedule_maintenance', methods=['GET', 'POST'])
def schedule_maintenance():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_staff'))

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM Airline_Staff WHERE username = %s", (username))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        return "No associated airline found."

    airline_name = result['airline_name']
    if request.method == 'POST':
        airplane_id = request.form['airplane_id']
        start_date_time = request.form['start_date_time']
        end_date_time = request.form['end_date_time']

        # if airplane is already scheduled for flights during maintenance
        cursor.execute("""SELECT * FROM Flight WHERE airplane_id = %s AND airline_name = %s 
                AND (
                       (departure_date_time BETWEEN %s AND %s) OR (arrival_date_time BETWEEN %s AND %s)
                       )""", (airplane_id, airline_name, start_date_time, end_date_time, start_date_time, end_date_time))
        

        result = cursor.fetchone()
        if result:
            cursor.close()
            error_message="Airplane is assigned to a flight during the maintenance period!"
            return render_template('schedule_maintenance.html', error_message =error_message)
        
         # Schedule maintenance

        cursor.execute("""INSERT INTO Maintenance_procedure (airline_name, airplane_id, start_date_time, end_date_time) 
            VALUES (%s, %s, %s, %s)""", (airline_name, airplane_id, start_date_time, end_date_time))
           
        conn.commit()
        cursor.close()

        success_message="Maintenance Scheduled."
        return render_template('schedule_maintenance.html', success_message =success_message)
    else:
        return render_template('schedule_maintenance.html')

@app.route('/frequent_customers', methods=['GET'])
def frequent_customers():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_staff'))

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM Airline_Staff WHERE username = %s", (username))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        return "No associated airline found."

    airline_name = result['airline_name']
    
        # get the frequent customers
    query = """
                SELECT customer_email, COUNT(*) as flight_count 
                FROM Ticket
                Where airline_name = %s and 
                purchase_date_time BETWEEN curdate() - INTERVAL 1 YEAR AND CURDATE()
                GROUP BY customer_email 
                ORDER BY flight_count DESC
                """
        
        #one year -> curdate() - INTERVAL 1 YEAR to get prev year
         
    cursor.execute(query, (airline_name))
    frequent_customers = cursor.fetchmany(10)
        
    cursor.close()

    return render_template('frequent_customers.html', customers=frequent_customers)

    #two seprate HTML files

@app.route('/customer_flights', methods=['GET', 'POST'])
def customer_flights():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_staff'))

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM Airline_Staff WHERE username = %s", (username))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        return "No associated airline found."

    airline_name = result['airline_name']
    if request.method == 'POST':
        customer_email = request.form.get('customer_email')
        #get all flights a Customer has taken only on that particular airline.
        query = """
                SELECT * FROM Flight 
                WHERE flight_number IN  
                         (SELECT flight_number 
                          FROM Ticket 
                          WHERE customer_email = %s AND airline_name = %s)"""
        
         #customer email from ticket-->

        cursor.execute(query, (customer_email,airline_name))
        customer_flights = cursor.fetchall()
        cursor.close()
        #customer_email=customer_email
        return render_template('customer_flights.html', flights=customer_flights, customer_email=customer_email)
    return render_template('customer_flights.html')

@app.route('/earned_revenue', methods=['GET'])
def earned_revenue():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_staff'))

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM Airline_Staff WHERE username = %s", (username))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        return "No associated airline found."

    airline_name = result['airline_name']

    # revenue for the last month
    last_month = """
        SELECT SUM(calculated_ticket_price) AS month
        FROM Ticket
        WHERE airline_name = %s AND 
        purchase_date_time BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND NOW()
    """
    cursor.execute(last_month, (airline_name))
    last_month_revenue = cursor.fetchone()
    last_month_revenue = last_month_revenue['month']

   # revenue for the last month
    last_year = """
        SELECT SUM(calculated_ticket_price) AS year
        FROM Ticket
        WHERE airline_name = %s AND 
        purchase_date_time BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND NOW()
    """
    cursor.execute(last_year, (airline_name))
    last_year_revenue = cursor.fetchone()
    last_year_revenue = last_year_revenue['year']

    if not last_year_revenue:
        last_year_revenue = 0
    if not last_month_revenue:
        last_month_revenue = 0
    
    cursor.close()

    return render_template('earned_revenue.html', month=last_month_revenue, year=last_year_revenue)

@app.route('/staff_log_out', methods=['GET'])
def staff_log_out():
    session.pop('username', None)
    #return redirect(url_for('perform_login_staff'))
    #return redirect('/login_staff')
    return render_template("login_staff.html", error_message="Loged Out!")
   
@app.route('/staff_update_profile', methods=['GET', 'POST'])
def staff_update_profile():
    username = session.get('username')
    if not username:
        return redirect(url_for('login_staff'))

    cursor = conn.cursor()
    cursor.execute("SELECT airline_name FROM Airline_Staff WHERE username = %s", (username))
    result = cursor.fetchone()
    email_success = None
    phone_success = None
    error_phone = None
    error_email = None

    if not result:
        cursor.close()
        return "No associated airline found."
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        if email:
            cursor.execute("SELECT * From Airline_Staff_Email WHERE email_address = %s", (email))
            result = cursor.fetchone()
            if result:
                error_email = "email already exists"
            else:

                cursor.execute("""INSERT INTO Airline_Staff_Email (username, email_address) VALUES (%s, %s)""",
                    (username, email))
                email_success = "Email Added!"
                conn.commit()
        if phone:
            cursor.execute("SELECT * From Airline_Staff_Phone WHERE phone_number = %s", (phone))
            result = cursor.fetchone()
            if result:
                error_phone = "phone already exists"
            else:
                cursor.execute("""INSERT INTO Airline_Staff_Phone (username, phone_number) VALUES (%s, %s)""",
                    (username, email))
                phone_success = "Phone Added!"
                conn.commit()
        cursor.close()

    return render_template('staff_update_profile.html', email_success=email_success, phone_success = phone_success, error_phone = error_phone , error_email =error_email)



@app.route('/customer_registration')
def customer_registration():
    return render_template('Customer_registration.html')


@app.route('/add_customer', methods=['POST', 'GET'])
def add_customer():
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        building_number = request.form['building_number'] if request.form['building_number'] else None
        street_name = request.form['street_name']
        apartment_number = request.form['apartment_number'] if request.form['apartment_number'] else None
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        date_of_birth = request.form['date_of_birth']
        phone = request.form['phone']
        passport_number = request.form['passport_number']
        passport_expiration = request.form['passport_expiration']
        passport_country = request.form['passport_country']

        if not password:
            error_message = "Password is required."
            return render_template('Customer_registration.html', failure=error_message)

        hashed_pass = hashlib.md5(password.encode()).hexdigest()

        cursor = conn.cursor()

        check_email_query = "SELECT * FROM Customer WHERE email_address = %s"
        cursor.execute(check_email_query, (email))
        if cursor.fetchone():
            return render_template('Customer_registration.html', failure="Email already exists")


        check_phone_query = "SELECT * FROM Customer_Phone WHERE email_address = %s AND phone_number = %s"
        cursor.execute(check_phone_query, (email ,phone))
        if cursor.fetchone():
            return render_template('Customer_registration.html', failure="phone_number already exists") 

        check_passport_query = "SELECT * FROM Customer_Passport WHERE email_address = %s AND passport_number = %s"
        cursor.execute(check_passport_query, (email ,passport_number))
        if cursor.fetchone():
            return render_template('Customer_registration.html', failure="Passport number already exists")

        #print(result_phone, result, result_passport)


        if not cursor.fetchone():
            query = """INSERT INTO Customer (email_address, password, first_name, last_name, 
                        building_number, street_name, apartment_number, city, state, zip_code, date_of_birth) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (email, hashed_pass, first_name, last_name, building_number, 
                                    street_name, apartment_number, city, state, zip_code, date_of_birth))
            conn.commit()
            query_to_add_phone = "INSERT INTO Customer_Phone (email_address, phone_number) VALUES (%s, %s)"
            cursor.execute(query_to_add_phone, (email, phone))

            query_to_add_passport = "INSERT INTO Customer_Passport (email_address, passport_number, passport_expiration, passport_country) VALUES (%s, %s, %s, %s)"
            cursor.execute(query_to_add_passport, (email, passport_number, passport_expiration, passport_country))

            cursor.close()
            return render_template('login_customer.html')
        
        else:
            return render_template('Customer_registration.html', failure="Failed to add Customer")



@app.route('/customer_login', methods=['GET'])
def customer_login():
    return render_template('login_customer.html')

@app.route('/perform_customer_login', methods=['POST', 'GET'])
def perform_customer_login():

    email = request.form['email_address'] 
    password = request.form['password'].encode()
    hashed_pass = hashlib.md5(password).hexdigest()

    cursor = conn.cursor()
    query_to_check = "SELECT * FROM Customer WHERE email_address = %s AND password = %s"
    cursor.execute(query_to_check, (email, hashed_pass))
    result = cursor.fetchone()
    cursor.close()

    if result:
        session['email_address'] = email
        return redirect(url_for('customer_home'))
    else:
        error_message = "Login Failed. Please check your credentials."
        return render_template("login_customer.html", error_message=error_message)

@app.route('/customer_home', methods=['GET'])
def customer_home():
    email_address = session.get('email_address')
    if not email_address:
        return redirect(url_for('customer_login'))
    return render_template('customer_home.html')


@app.route('/update_customer_profile', methods=['GET', 'POST'])
def update_customer_profile():
    email_address = session.get('email_address')
    if not email_address:
        return redirect(url_for('customer_login'))

    cursor = conn.cursor()
    phone_success = passport_success = None
    error_phone = error_passport = None

    if request.method == 'POST':
        phone = request.form.get('phone')
        passport_number = request.form.get('passport_number')
        passport_expiration = request.form.get('passport_expiration')
        passport_country = request.form.get('passport_country')

        if phone:
            cursor.execute("SELECT * FROM Customer_Phone WHERE email_address = %s AND phone_number = %s", (email_address, phone))
            result = cursor.fetchone()
            if result:
                error_phone = "Phone number already exists"
            else:
                cursor.execute("INSERT INTO Customer_Phone (email_address, phone_number) VALUES (%s, %s)", (email_address, phone))
                phone_success = "Phone number added!"
                conn.commit()

        if passport_number:
            cursor.execute("SELECT * FROM Customer_Passport WHERE email_address = %s AND passport_number = %s", (email_address , passport_number))
            result = cursor.fetchone()
            if result:
                error_passport = "Passport number already exists"
            else:
                cursor.execute("""INSERT INTO Customer_Passport (email_address, passport_number, passport_expiration, passport_country) 
                                  VALUES (%s, %s, %s, %s)""",
                               (email_address, passport_number, passport_expiration, passport_country))
                passport_success = "Passport details added!"
                conn.commit()

        cursor.close()

    return render_template('customer_update_profile.html', phone_success=phone_success, error_phone=error_phone, passport_success=passport_success, error_passport=error_passport)


@app.route('/view_customer_flights', methods=['GET', 'POST'])
def view_customer_flights():
    email_address = session.get('email_address')
    if not email_address:
        return redirect(url_for('customer_login'))

    current_date = datetime.now()
    flight_option = request.form.get('flight_option', 'future')

    cursor = conn.cursor()
    if flight_option == 'future':
        query = """SELECT Flight.*, Ticket.ticket_ID FROM Flight 
                   JOIN Ticket ON Flight.flight_number = Ticket.flight_number 
                   AND Flight.departure_date_time = Ticket.departure_date_time 
                   WHERE Ticket.customer_email = %s AND Flight.departure_date_time > %s"""
        

        cursor.execute(query, (email_address, current_date))
        flights = cursor.fetchall()
        cursor.close()
    elif flight_option == 'past':
        query = """SELECT Flight.*, Ticket.ticket_ID FROM Flight 
                   JOIN Ticket ON Flight.flight_number = Ticket.flight_number 
                   AND Flight.departure_date_time = Ticket.departure_date_time 
                   WHERE Ticket.customer_email = %s AND Flight.departure_date_time < %s"""
        cursor.execute(query, (email_address, current_date))
        flights = cursor.fetchall()
        cursor.close()
    else:  # All flights
        query = """SELECT Flight.*, Ticket.ticket_ID FROM flight 
                   JOIN Ticket ON Flight.flight_number = Ticket.flight_number 
                   AND Flight.departure_date_time = Ticket.departure_date_time 
                   WHERE Ticket.customer_email = %s"""
    
        cursor.execute(query, (email_address))
        flights = cursor.fetchall()
        cursor.close()

    return render_template('view_customer_flights.html', flights=flights, flight_option=flight_option)

@app.route('/customer_search_flights', methods=['POST', 'GET'])
def search_flights():
    email_address = session.get('email_address')
    if not email_address:
        return redirect(url_for('customer_login'))
    flights = None
    if request.method == 'POST':
        departure_airport = request.form['departure_airport']
        arrival_airport = request.form['arrival_airport']
        departure_date = request.form['departure_date']
        return_date = request.form.get('return_date')
        trip_type = request.form['trip_type']

        cursor = conn.cursor()
        query = """
        SELECT flight_number, airline_name, departure_airport, arrival_airport, departure_date_time, arrival_date_time, base_price_of_ticket 
            FROM Flight 
            WHERE departure_airport = %s 
            AND arrival_airport = %s 
            AND DATE(departure_date_time) = %s
            AND departure_date_time >= NOW()
        """
        values = [departure_airport, arrival_airport, departure_date]

        if trip_type == "roundtrip" and return_date:
            query += " AND DATE(arrival_date_time) = %s AND arrival_date_time >= NOW()"
            values.append(return_date)

        cursor.execute(query, values)
        flights = cursor.fetchall()
        cursor.close()

    return render_template('customer_search_flights.html', flights=flights)


@app.route('/purchase_ticket', methods=['GET', 'POST'])
def purchase_ticket():
    email_address = session.get('email_address')
    if not email_address:
        return redirect(url_for('customer_login'))

    if request.method == 'POST':
        flight_number = request.form['flight_number']
        airline_name = request.form['airline_name']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        card_type = request.form['card_type']
        card_number = request.form['card_number']
        name_on_card = request.form['name_on_card']
        expiration_date = request.form['expiration_date']

        cursor = conn.cursor()

        cursor.execute("SELECT departure_date_time, base_price_of_ticket, airplane_id FROM Flight WHERE flight_number = %s AND airline_name = %s", (flight_number, airline_name))
        flight = cursor.fetchone()

        if not flight:
            return render_template('purchase_ticket.html', message="Flight not found")

        departure_date_time = flight['departure_date_time']
        base_price = flight['base_price_of_ticket']
        airplane_id = flight['airplane_id']


        cursor.execute("SELECT number_of_seats FROM Airplane WHERE identification_number = %s", (airplane_id))
        result = cursor.fetchone()
        if result is None:
            return render_template('purchase_ticket.html', message="Airplane not found")
        
        total_seats = result['number_of_seats']

        cursor.execute("SELECT COUNT(*) as ticket_count FROM Ticket WHERE flight_number = %s", (flight_number))
        tickets_sold = cursor.fetchone()['ticket_count']

        if tickets_sold >= total_seats:
            return render_template('purchase_ticket.html', message="Sold Out")
        calculated_price = base_price * 1.25 if tickets_sold / total_seats >= 0.8 else base_price

        query = """INSERT INTO Ticket (flight_number, departure_date_time, airline_name, purchase_date_time, base_ticket_price, calculated_ticket_price ,customer_email,
             first_name ,last_name , date_of_birth, card_type ,card_number ,name_on_card ,expiration_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (flight_number, departure_date_time, airline_name, datetime.now(), base_price, calculated_price, email_address, first_name, last_name, date_of_birth, card_type, card_number, name_on_card, expiration_date))
        ticket_id = cursor.lastrowid
        conn.commit()

        return render_template('purchase_ticket.html', ticket_id=ticket_id)

    return render_template('purchase_ticket.html')

@app.route('/customer_log_out', methods=['GET'])
def customer_log_out():
    session.pop('email_address', None)
    return render_template("login_customer.html", error_message="Logged Out!")


@app.route('/cancel_ticket_page', methods=['GET'])
def cancel_ticket_page():
    return render_template('cancel_ticket.html', message="")

@app.route('/cancel_ticket', methods=['POST'])
def cancel_ticket():
    email_address = session.get('email_address')
    if not email_address:
        # Redirect to login if the user is not logged in
        return redirect(url_for('customer_login'))

    ticket_id = request.form['ticket_id']
    current_time = datetime.now()
    with conn.cursor() as cursor:
        # Check if the ticket exists, belongs to the customer, and the flight is more than 24 hours in the future
        query = """
        SELECT Ticket.flight_number, Ticket.departure_date_time FROM Ticket
        JOIN Flight ON Ticket.flight_number = Flight.flight_number 
        WHERE ticket_ID = %s AND customer_email = %s
        """
        cursor.execute(query, (ticket_id, email_address))
        ticket_info = cursor.fetchone()
        if ticket_info and ticket_info['departure_date_time'] > current_time + timedelta(hours=24):
            # If conditions are met delete the ticket
            delete_query = "DELETE FROM Ticket WHERE ticket_ID = %s"
            cursor.execute(delete_query, (ticket_id,))
            conn.commit()
            return render_template('cancel_ticket.html', success_message="Ticket successfully cancelled.")
        else:
            # If conditions are not met, inform the user
            return render_template('cancel_ticket.html', error_message="Ticket cannot be cancelled. It is either non-existent or the flight is within 24 hours.")
        ## print("#######################")

        ##cursor.close()


@app.route('/rate_flight', methods=['GET', 'POST'])
def rate_flight():
    email_address = session.get('email_address')
    if not email_address:
        return redirect(url_for('customer_login'))

    if request.method == 'POST':
        flight_number = request.form['flight_number']
        rating = request.form['rating']
        comment = request.form['comment']
        departure_date_time = request.form['departure_date_time']

        cursor = conn.cursor()
        # Check if the customer has taken this flight
        query_check_flight = """
        SELECT * FROM Ticket
        WHERE customer_email = %s AND flight_number = %s AND departure_date_time = %s
        """
        cursor.execute(query_check_flight, (email_address, flight_number, departure_date_time))
        if cursor.fetchone():
            # Insert the rating and comment
            insert_query = """
            INSERT INTO Flight_Rating (flight_number, airline_name, departure_date_time, customer_email, rating, comment)
            SELECT flight_number, airline_name, departure_date_time, %s, %s, %s
            FROM Flight
            WHERE flight_number = %s AND departure_date_time = %s
            """
            cursor.execute(insert_query, (email_address, rating, comment, flight_number, departure_date_time))
            conn.commit()
            message = "Rating and comment added successfully."
        else:
            message = "You have not taken this flight."

        cursor.close()
        return render_template('rate_flight.html', message=message)

    return render_template('rate_flight.html')

@app.route('/track_spending', methods=['GET', 'POST'])
def track_spending():
    email_address = session.get('email_address')
    if not email_address:
        return redirect(url_for('login_customer'))

    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    # Default date range: last 6 months and last year
    if not start_date and not end_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

    cursor = conn.cursor()

    # Query for total spending in specified date range
    total_spending_query = """
    SELECT SUM(calculated_ticket_price) AS total_spending
    FROM Ticket
    WHERE customer_email = %s AND
    purchase_date_time BETWEEN %s AND %s
    """
    cursor.execute(total_spending_query, (email_address, start_date, end_date))
    total_spending = cursor.fetchone()['total_spending']

    # Query for month-wise spending in the last 6 months
    month_wise_spending_query = """
    SELECT MONTH(purchase_date_time) AS month, SUM(calculated_ticket_price) AS monthly_spending
    FROM Ticket
    WHERE customer_email = %s AND
    purchase_date_time BETWEEN %s AND %s
    GROUP BY MONTH(purchase_date_time)
    """
    cursor.execute(month_wise_spending_query, (email_address, start_date, end_date))
    month_wise_spending = cursor.fetchall()

    cursor.close()

    return render_template('track_spending.html', total_spending=total_spending, month_wise_spending=month_wise_spending)


if __name__ == '__main__':
    app.run(debug=True)
