import psycopg2
import connect

def main_menu():
    print("\n--- Practice 08: Functions & Procedures ---")
    print("1. Search (Function)")
    print("2. Upsert (Procedure)")
    print("3. Pagination (Function)")
    print("4. Delete (Procedure)")
    print("5. Exit")

def run():
    while True:
        main_menu()
        choice = input("Select: ")
        conn = connect.get_connection()
        cur = conn.cursor()

        try:
            if choice == '1':
                p = input("Pattern: ")
                cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (p,))
                for r in cur.fetchall(): print(r)
            
            elif choice == '2':
                n, ph = input("Name: "), input("Phone: ")
                cur.execute("CALL upsert_contact(%s, %s)", (n, ph))
                conn.commit()
                print("Done.")

            elif choice == '3':
                l, o = input("Limit: "), input("Offset: ")
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (l, o))
                for r in cur.fetchall(): print(r)

            elif choice == '4':
                t = input("Name or Phone to delete: ")
                cur.execute("CALL delete_contact_proc(%s)", (t,))
                conn.commit()
                print("Deleted.")

            elif choice == '5': break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    run()