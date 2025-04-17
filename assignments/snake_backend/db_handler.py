import psycopg2 
# from snake import username as name

conn = psycopg2.connect(
database = 'snake_game',
user = 'postgres', 
host = 'localhost', 
password = 'NaruSaske51>_',
port = 5432
)

conn.autocommit = True

current_user = ''

# Queries

query_create_table_users = """
    CREATE TABLE users(
        user_id SERIAL NOT NULL PRIMARY KEY,
        username VARCHAR(255) UNIQUE
    )
"""

query_create_table_user_scores = """
    CREATE TABLE user_scores(
        user_id SERIAL NOT NULL PRIMARY KEY,
        username VARCHAR(255),
        score INT,
        level INT
    )
"""

# Functions


# A function for executing any queries
def execute_query(query): 
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# A function for getting the input from the user
def input_user(username):
    global current_user
    current_user = username


# A function for adding the new username
def add_user(name):
    command = 'INSERT INTO users(username) VALUES (%s)'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (name,))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)



# A function for checking whether the user exists in the database or not
def check_user_exists(name):
    command = 'SELECT * FROM users WHERE username = %s'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (name,))
            result = cur.fetchall()
            return bool(result) # we return the boolean value of the resulting list. If the list is empty the boolean will be False
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    
# A function for adding a new score to the table
def add_new_score(score, level):
    command = "INSERT INTO user_scores(username, score, level) VALUES (%s, %s, %s)"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (current_user, score, level))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# A function for processing the user's score. It check whether the 'username' exists or not
# if it doesn't exist, the new 'username' is added and the function add_new_score() is called
def process_score(score, level):
    user_exists = check_user_exists(current_user)
    if not user_exists:
        add_user(current_user)
    add_new_score(score, level)


# A function to show the highest level of the user when he/she enters the username or the 'pause' button is pressed
def show_highest_level():
    command = 'SELECT MAX(level) FROM user_scores WHERE username = %s'
    try:
        with conn.cursor() as cur:
            cur.execute(command, (current_user,))
            result = cur.fetchall()
            return result
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# This if statement is necessary to make sure that the code block inside of it is not executed automatically
# when it's called as a module in another file. 
# But if it's called explicitly like 'db_handler.input_user()', the code block will be executed
if __name__ == '__main__':
    input_user()
    process_score()
    # execute_query(query_create_table_user_scores)
    # execute_query(query_create_table_users)
