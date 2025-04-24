# Using Functions and stored Procedures
import psycopg2, csv
from psycopg2 import extensions

conn = psycopg2.connect(database = "phonebook", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "NaruSaske51>_",
                        port = 5432)

conn.autocommit = True

command_create_db = 'CREATE DATABASE phone'
command_create_table = """
    CREATE TABLE phonebook( 
        user_id SERIAL NOT NULL PRIMARY KEY, 
        username VARCHAR(255),
        phone_number VARCHAR(255)
    )
"""
command_insert_into_csv = 'INSERT INTO phonebook (username, phone_number) VALUES (%s, %s)'

command_update_phone = 'UPDATE phonebook SET phone_number = %s WHERE user_id = %s'

command_update_name = 'UPDATE phonebook SET username = %s WHERE user_id = %s'

command_filter_name_starts = "SELECT * FROM phonebook WHERE username LIKE %s"

command_filter_phone_starts = "SELECT * FROM phonebook WHERE phone_number LIKE %s"

command_delete_by_phone = "DELETE FROM phonebook WHERE phone_number = %s"

command_delete_by_name = "DELETE FROM phonebook WHERE username = %s"

create_function_select_starts_with_by_name = """
        CREATE OR REPLACE FUNCTION select_starts_with(starts_with varchar)
        RETURNS TABLE(
            user_id integer, 
            name varchar,
            phone_number varchar
        ) AS 
        $$
        BEGIN
            RETURN QUERY
            SELECT p.user_id, p.username, p.phone_number FROM phonebook p WHERE p.username LIKE starts_with || '%';
        END;
        $$
        LANGUAGE plpgsql;
""" # || -> means concatenation of strings in SQL
    # p is an alias for the name of the table, it's useful not to write the full name of the table every time

create_function_select_starts_with_by_phone_number = """
        CREATE OR REPLACE FUNCTION select_starts_with_phone(starts_with varchar)
        RETURNS TABLE(
            user_id integer, 
            name varchar,
            phone_number varchar
        ) AS 
        $$
        BEGIN
            RETURN QUERY
            SELECT p.user_id, p.username, p.phone_number FROM phonebook p WHERE p.phone_number LIKE starts_with || '%';
        END;
        $$
        LANGUAGE plpgsql;
"""

create_function_offset_limit = """
        CREATE OR REPLACE FUNCTION select_offset_limit(inserted_offset integer, inserted_limit integer)
        RETURNS TABLE(
            user_id integer, 
            name varchar,
            phone_number varchar
        ) AS 
        $$
        BEGIN
            RETURN QUERY
            SELECT p.user_id, p.username, p.phone_number FROM phonebook p LIMIT inserted_limit OFFSET inserted_offset;
        END;
        $$
        LANGUAGE plpgsql;
"""

create_procedure_insert_by_name_phone = """
        CREATE OR REPLACE PROCEDURE insert_by_name_and_phone(inserted_name varchar, inserted_phone varchar) AS 
        $$
        BEGIN
            IF EXISTS(SELECT 1 FROM phonebook p WHERE p.username = inserted_name) THEN
                UPDATE phonebook SET phone_number = inserted_phone WHERE username = inserted_name;
            ELSE 
                INSERT INTO phonebook(username, phone_number) VALUES(inserted_name, inserted_phone);
            END IF;
        END;
        $$
        LANGUAGE plpgsql;
"""

create_procedure_delete_by_name = """
        CREATE OR REPLACE PROCEDURE delete_by_name(inserted_name varchar) AS 
        $$
        BEGIN
            DELETE FROM phonebook WHERE username = inserted_name;
        END;
        $$
        LANGUAGE plpgsql;
"""

create_procedure_delete_by_phone = """
        CREATE OR REPLACE PROCEDURE delete_by_phone(inserted_phone varchar) AS 
        $$
        BEGIN
            DELETE FROM phonebook WHERE phone_number = inserted_phone;
        END;
        $$
        LANGUAGE plpgsql;
"""

# A new data type for incorrect rows in SQL
create_new_type_for_incorrect_users = """CREATE TYPE invalid_user_info AS (
        username VARCHAR,
        phone_number VARCHAR
);
"""

# A new data type in SQL for storing users' info 
create_new_type_for_users = """
    CREATE TYPE user_info AS (
    username VARCHAR,
    phone_number VARCHAR
);
"""

create_procedure_insert_users = """
        CREATE OR REPLACE PROCEDURE insert_users(
            users_list user_info[],
            INOUT invalid_rows user_info[]
    ) AS
        $$
        DECLARE
            rec user_info;
        BEGIN
            FOREACH rec IN ARRAY users_list LOOP
                IF rec.phone_number ~ '^\d{11}$' THEN 
                    INSERT INTO phonebook(username, phone_number)
                    VALUES(rec.username, rec.phone_number);
                ELSE 
                    invalid_rows := array_append(invalid_rows, rec);
                END IF;
            END LOOP;
        END;
        $$
        LANGUAGE plpgsql;
""" 
# invalid_rows := array_append(invalid_rows, rec); -> in this line array_append() appends invalid rows to
# invalid_rows variable and assigns the result back to the invalid_rows

# ~ is in SQL to perform regular expression matching on a string.
# ^ -> means 'starts with'
# \d{11} -> with exactly 11 digits
# $ -> ends after those 11 digits

cur = conn.cursor()

csv_file = 'phones.csv'

def csv_to_db(csv_file):
    with open(csv_file, 'r') as file_csv:
        reader_csv = csv.reader(file_csv, delimiter = ',')
        for row in reader_csv:
            cur.execute(command_insert_into_csv, (row[0], row[1]))

# Inserting data into the PhoneBook.


# Printing every row of the table
def print_rows():
    cur.execute('SELECT * FROM phonebook')
    results = cur.fetchall()
    for row in results:
        print(row)


# Inserting data to the table 
def insert_to_db():
    username = input('Enter the username: ')
    phone = input('Enter the phone number: ')
    cur.execute(command_insert_into_csv, (username, phone))

# 3 Updating data in the table (change user first name or phone)


# Changing by the name
def change_name():  
    new_username = input("Enter the new username: ")
    id = int(input('Enter the ID you want to change: '))
    cur.execute(command_update_name, (new_username, id))
    print_rows()

# Changing by the phone number
def change_phone_number():
    new_phone = input("Enter the new phone number: ")
    id = int(input('Enter the ID you want to change: '))
    cur.execute(command_update_phone, (new_phone, id))
    print_rows()

# Filtering by the name that starts by the user's input
def filter_name_start_by():
    starts_with = input("Enter the letters that have to start with: ")
    cur.execute(command_filter_name_starts, (starts_with + '%',))   
    results = cur.fetchall()
    for row in results:
        print(row)

# Filtering by the name taht starts by the user's input
def filter_phone_start_by():
    starts_with = input('Enter the digits that the phone number has to start with: ')
    cur.execute(command_filter_phone_starts, (starts_with + '%',)) # After cur.execute(...) the result of the 
    results = cur.fetchall()                                       # query is saved inside the cur object  
    for row in results: # .fetchall() takes all rows from the result of the last cur.execute() query 
        print(row)      # and returns them as a list of tuples

# Deleting by the phone number
def delete_by_phone():
    phone_number = input('Enter the phone you want to delete: ')
    cur.execute(command_delete_by_phone, (phone_number,))
    print_rows()

# Deleting by the name
def delete_by_name():
    name = input('Enter the name you want to delete: ')
    cur.execute(command_delete_by_name, (name,))
    print_rows()


# Function for retrieving usernames that start with the given letter
def get_starting_with(letter):
    command = 'SELECT username FROM phonebook WHERE LEFT(username, 1) = %s'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (letter,))
            result = cur.fetchall()
            print(result)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    
# Function that returns all records based on part of name  
def select_record_by_username_pattern(pattern):
    command = 'SELECT * FROM select_starts_with(%s)'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (pattern,))
            result = cur.fetchall()
            for row in result:
                print(row)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# Function that returns all records based on part of phone_numbers 
def select_record_by_phone_number_pattern(pattern):
    command = 'SELECT * FROM select_starts_with_phone(%s)'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (pattern,))
            result = cur.fetchall()
            for row in result:
                print(row) 
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    
# Insert new user by name and phone, update phone if user already exists
def insert_by_name_and_phone(name, phone):
    command = 'CALL insert_by_name_and_phone(%s, %s)'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (name, phone))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# Procedure to deleting data from tables by username
def delete_by_username(name):
    command = 'CALL delete_by_name(%s)'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (name,))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# Procedure to deleting data from tables by phone_number
def delete_by_phone(phone):
    command = 'CALL delete_by_phone(%s)'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (phone,))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# Function to querying data from the tables with pagination (by limit and offset)
def select_by_offset_and_limit(offset, limit):
    command = 'SELECT * FROM select_offset_limit(%s, %s)'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (offset, limit))
            result = cur.fetchall()
            for row in result:
                print(row)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# Procedure to insert many new users from a list of names and phones
def insert_users(users_to_insert):
    command_1 = 'CALL insert_users(%s, %s)'
    invalid_rows = []
    # Adapting users so that SQL would understand it  
    adapted_users = [adapt_user(User_info(username, phone)) for username, phone in users_to_insert]
    try:
        with conn.cursor() as cur:
            cur.execute(command_1, (adapted_users, invalid_rows))
            conn.commit()
            # Printing the invalid rows back to the terminal
            result = cur.fetchone()
            for row in result:
                print('Invalid rows:', row)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
            
            # result = cur.fetchone()[0]

            # invalid_rows = invalid_rows_result[0][0]
            # print('Invalid rows: ', result)
    
# Used to group username and phone number together and pass them as one object to SQL
class User_info:
    def __init__(self, username, phone_number):
        self.username = username
        self.phone_number = phone_number

# Converts a User_info object into a SQL-safe string for PostgreSQL
def adapt_user(user):
    username = psycopg2.extensions.adapt(user.username).getquoted().decode('utf-8')
    phone_number = psycopg2.extensions.adapt(user.phone_number).getquoted().decode('utf-8')
    # print(username, phone_number)
    # print(f'ROW({username}, {phone_number})::user_info')
    return psycopg2.extensions.AsIs(f'ROW({username}, {phone_number})::user_info')

# whenever you pass a User_info object into a query, psycopg2 will 
# automatically call your adapt_user() function to get the correct SQL version.
psycopg2.extensions.register_adapter(User_info, adapt_user)

# Function for executing queries
def execute_query(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

users_to_insert = (
    ("Sakura Haruno", '87005554433'),
    ('Kakashi Hatake', '87001112233'),
    ('Hinata Hyuga', '87009998877'),
    ('Hashirama Senju', '879872223232'),
    ('Naruto Uzumaki', '8780'),
    ('Itachi Uchiha', '8777')
)

# Getting the user input
def get_user_input():
    commands = """    insert - Inserting into the database
    change name - Changing the name of the user by the id
    change phone number - Changing the phone number of the user by the id
    filter by name - Filtering by the name that starts with the given value
    filter by phone number - Filtering by the phone number that starts with the given value
    delete by name - Deleting record by the name 
    delete by phone number - Deleting record by the phone number
    print all - Printing all records in the table
    insert csv - Inserting all records to the database from the csv file
    start with letter - Selecting usernames starting with the given letter
    select by name start with pattern - Selecting records starting with the given pattern of name
    select by phone_number start with pattern - Selecting records starting with the given pattern of phone number
    insert by phone and name - Inserting new user by name and phone, update phone if user already exists
    delete by username - Procedure to deleting data from tables by username
    delete by phone number - Procedure to deleting data from tables by phone_number
    select by offset and limit - Function to querying data from the tables with pagination (by limit and offset)
    insert users - Procedure to insert many new users by list of name and phone"""
    print(commands)
    user_input = input("Enter the command: ")
    if user_input == 'insert':
        insert_to_db()
    elif user_input == 'change name':
        change_name()
    elif user_input == 'change phone number':
        change_phone_number()
    elif user_input == 'filter by name':
        filter_name_start_by()
    elif user_input == 'filter by phone number':
        filter_phone_start_by()
    elif user_input == 'delete name':
        delete_by_name()
    elif user_input == 'delete phone number':
        delete_by_phone()
    elif user_input == 'print all':
        print_rows()
    elif user_input == 'insert csv':
        csv_to_db(csv_file)
        print_rows()
    elif user_input == 'start with letter':
        letter = input('Enter the letter: ')
        get_starting_with(letter)
    elif user_input == 'select by name start with pattern':
        pattern = input("Enter the pattern: ")
        select_record_by_username_pattern(pattern)
    elif user_input == 'select by phone_number start with pattern':
        pattern = input("Enter the pattern: ")
        select_record_by_phone_number_pattern(pattern)
    elif user_input == 'insert by phone and name':
        name = input("Enter the name: ")
        phone = input("Enter the phone: ")
        insert_by_name_and_phone(name, phone)
    elif user_input == 'delete by username':
        name = input("Enter the name: ")
        delete_by_username(name)
    elif user_input == 'delete by phone number':
        phone = input("Enter the phone: ")
        delete_by_phone(phone)
    elif user_input == 'select by offset and limit':
        offset = input("Enter the offset: ")
        limit = input("Enter the limit: ")
        select_by_offset_and_limit(offset, limit)
    elif user_input == 'insert users':
        insert_users(users_to_insert)

# cur.execute(command_create_db)

# cur.execute(command_create_table)

# Getting user_input
get_user_input()

# Function that returns all records based on part of name 
# execute_query(create_function_select_starts_with_by_name)

# Function that returns all records based on part of phone_numbe 
# execute_query(create_function_select_starts_with_by_phone_number)


# Creating a Procedure to insert new user by name and phone, update phone if user already exists
# execute_query(create_procedure_insert_by_name_phone)

# Procedure to deleting data from tables by username
# execute_query(create_procedure_delete_by_name)

# Procedure to deleting data from tables by phone
# execute_query(create_procedure_delete_by_phone)


# Function to querying data from the tables with pagination (by limit and offset)
# execute_query(create_function_offset_limit)


# Creating new data type in SQL for incorrect users
# execute_query(create_new_type_for_incorrect_users)

# Creating new data type in SQL for users
# execute_query(create_new_type_for_users)

# Procedure to insert many new users by list of name and phone
# execute_query(create_procedure_insert_users)

conn.commit()

cur.close()
conn.close()

