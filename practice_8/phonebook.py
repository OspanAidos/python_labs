import psycopg2
import connect

def main_menu():
    print("\n--- Practice 08: Functions & Procedures ---")
    print("1. Search (Function)")
    print("2. Upsert (Procedure)")
    print("3. Pagination (Function)")
    print("4. Delete (Procedure)")
    print("5. Bulk Insert (New Procedure)")
    print("6. Exit")

def run():
    while True:
        main_menu()
        choice = input("Select: ")
        
        if choice == '6':
            print("Goodbye!")
            break

        
        try:
            conn = connect.get_connection()
            cur = conn.cursor()

            if choice == '1':
                p = input("Enter search pattern (name or phone): ")
                cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (p,))
                rows = cur.fetchall()
                if rows:
                    for r in rows: print(f"ID: {r[0]} | Name: {r[1]} | Phone: {r[2]}")
                else:
                    print("No contacts found.")
            
            elif choice == '2':
                n = input("Name: ")
                ph = input("Phone: ")
                cur.execute("CALL upsert_contact(%s, %s)", (n, ph))
                conn.commit()
                print("Contact added or updated successfully.")

            
            elif choice == '3':
                l = int(input("Limit (how many): "))
                o = int(input("Offset (skip): "))
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (l, o))
                for r in cur.fetchall():
                    print(f"ID: {r[0]} | Name: {r[1]} | Phone: {r[2]}")

            
            elif choice == '4':
                t = input("Name or Phone to delete: ")
                cur.execute("CALL delete_contact_proc(%s)", (t,))
                conn.commit()
                print("Deleted successfully (if existed).")

            
            elif choice == '5':
                print("Enter names separated by comma (e.g. Aidos,Madi,Ivan):")
                names = [n.strip() for n in input().split(',')]
                print("Enter phones separated by comma (e.g. 707,701,705):")
                phones = [p.strip() for p in input().split(',')]
                
                if len(names) != len(phones):
                    print("Error: The number of names and phones must be the same!")
                else:
                    cur.execute("CALL insert_bulk_contacts(%s, %s)", (names, phones))
                    conn.commit()
                    print(f"Successfully processed {len(names)} contacts.")

            else:
                print("Invalid choice, try again.")

        except Exception as e:
            print(f"Database error: {e}")
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    run()