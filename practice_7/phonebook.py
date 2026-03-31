import psycopg2
import csv
import config
import os

def get_connect():
    return psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )

def create_table():
    try:
        with get_connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS phonebook (
                        user_id SERIAL PRIMARY KEY,
                        first_name VARCHAR(50) NOT NULL,
                        phone_number VARCHAR(20) NOT NULL UNIQUE
                    );
                """)
                print("Table is ready.")
    except Exception as e:
        print(f"Error creating table: {e}")

def import_from_csv(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found!")
        return
    try:
        with get_connect() as conn:
            with conn.cursor() as cur:
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        cur.execute(
                            "INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                            (row[0], row[1])
                        )
                print("Data imported from CSV successfully!")
    except Exception as e:
        print(f"Error during import: {e}")

def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    try:
        with get_connect() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", (name, phone))
                print(f"Contact {name} added.")
    except Exception as e:
        print(f"Error: {e}")

def update_contact():
    name = input("Enter the name of the contact you want to change: ")
    print("What to change? 1 - Name, 2 - Phone Number")
    sub_choice = input("> ")
    try:
        with get_connect() as conn:
            with conn.cursor() as cur:
                if sub_choice == '1':
                    new_name = input("Enter new name: ")
                    cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, name))
                else:
                    new_phone = input("Enter new phone number: ")
                    cur.execute("UPDATE phonebook SET phone_number = %s WHERE first_name = %s", (new_phone, name))
                print("Data updated.")
    except Exception as e:
        print(f"Error: {e}")

def query_contacts():
    search = input("Enter name or part of phone number to search: ")
    try:
        with get_connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM phonebook WHERE first_name LIKE %s OR phone_number LIKE %s", 
                            (f'%{search}%', f'%{search}%'))
                rows = cur.fetchall()
                if not rows:
                    print("No contacts found.")
                for row in rows:
                    print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    except Exception as e:
        print(f"Search error: {e}")

def delete_contact():
    target = input("Enter name or phone number to delete: ")
    try:
        with get_connect() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM phonebook WHERE first_name = %s OR phone_number = %s", (target, target))
                print(f"Contact {target} deleted (if it existed).")
    except Exception as e:
        print(f"Delete error: {e}")

def show_all():
    try:
        with get_connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM phonebook ORDER BY user_id")
                rows = cur.fetchall()
                print("\n--- ALL CONTACTS ---")
                for row in rows:
                    print(f"{row[0]}. {row[1]}: {row[2]}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        print("\n--- PHONEBOOK SYSTEM ---")
        print("1. Create table")
        print("2. Insert from CSV")
        print("3. Insert from console")
        print("4. Update contact")
        print("5. Query contacts")
        print("6. Delete contact")
        print("7. Show all contacts")
        print("8. Exit")
        
        choice = input("\nSelect action: ")
        
        if choice == '1': create_table()
        elif choice == '2': import_from_csv('contacts.csv')
        elif choice == '3': add_contact()
        elif choice == '4': update_contact()
        elif choice == '5': query_contacts()
        elif choice == '6': delete_contact()
        elif choice == '7': show_all()
        elif choice == '8': break
        else: print("Invalid input!")

if __name__ == "__main__":
    main()