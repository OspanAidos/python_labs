import psycopg2
import connect

def main_menu():
    print("\n--- Practice 08: PhoneBook PRO ---")
    print("1. Search by Names (e.g. Aidos, Madi)")
    print("2. Add/Update Contact (Upsert)")
    print("3. Pagination (Limit & Offset)")
    print("4. Delete Contact")
    print("5. Bulk Insert (Add Multiple)")
    print("6. Exit")

def run():
    while True:
        main_menu()
        choice = input("Select: ")
        
        if choice == '6':
            break

        try:
            conn = connect.get_connection()
            cur = conn.cursor()

            if choice == '1':
                search_input = [s.strip() for s in input("Enter name(s): ").split(',')]
                cur.execute("SELECT * FROM get_multiple_contacts(%s)", (search_input,))
                rows = cur.fetchall()
                if rows:
                    for r in rows: print(f"Name: {r[1]} | Phone: {r[2]}")
                else:
                    print("No matches found.")
            
            elif choice == '2':
                n, ph = input("Name: "), input("Phone: ")
                cur.execute("CALL upsert_contact(%s, %s)", (n, ph))
                conn.commit()
                print("Done.")

            elif choice == '3':
                l, o = int(input("Limit: ")), int(input("Offset: "))
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (l, o))
                for r in cur.fetchall():
                    print(f"ID: {r[0]} | Name: {r[1]} | Phone: {r[2]}")

            elif choice == '4':
                t = input("Name or Phone to delete: ")
                cur.execute("CALL delete_contact_proc(%s)", (t,))
                conn.commit()
                print("Deleted.")

            elif choice == '5':
                names = [n.strip() for n in input("Names: ").split(',')]
                phones = [p.strip() for p in input("Phones: ").split(',')]
                if len(names) == len(phones):
                    cur.execute("CALL insert_bulk_contacts(%s, %s)", (names, phones))
                    conn.commit()
                    print("Bulk insert done.")
                else:
                    print("Error: Count mismatch!")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    run()