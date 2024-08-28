import psycopg2
import getpass

# Database connection details
hostname = 'localhost'
database = 'demo'
username = 'postgres'
password = 'Vishalrai2000@'
port_id = 5432

def connect_db():
    """Establish a database connection."""
    return psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username, 
        password=password,
        port=port_id
    )

def create_user_table():
    """Create the users table if it doesn't exist."""
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
        ''')
        conn.commit()
    except Exception as error:
        print("Error creating table:", error)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def register_user():
    """Register a new user."""
    try:
        conn = connect_db()
        cur = conn.cursor()
        
        username = input("Enter username: ")
        while True:
            password = getpass.getpass("Enter password: ")
            confirm_password = getpass.getpass("Confirm password: ")
            if password == confirm_password:
                break
            else:
                print("Passwords do not match. Please try again.")

        cur.execute(''' INSERT INTO users (username, password) VALUE (%s, %s) ''', (username, password))
        
        conn.commit()
        print("User registered successfully!")
    except Exception as error:
        print("Error registering user:", error)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def login_user():
    """Log in an existing user."""
    try:
        conn = connect_db()
        cur = conn.cursor()
        
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        
        cur.execute('''SELECT * FROM users WHERE username = %s AND password = %s''', (username, password))
        
        user = cur.fetchone()
        
        if user:
            print("Login successful!")
        else:
            print("Invalid username or password. Please try again.")
            while True:
                password = getpass.getpass("Re-enter password: ")
                cur.execute('''SELECT * FROM users WHERE username = %s AND password = %s''', (username, password))
                
                user = cur.fetchone()
                
                if user:
                    print("Login successful!")
                    break
                else:
                    print("Passwords do not match. Please try again.")
    except Exception as error:
        print("Error during login:", error)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def main():
    """Main function to run the application."""
    create_user_table()
    
    print("1. Register")
    print("2. Login")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == '1':
        register_user()
    elif choice == '2':
        login_user()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()



