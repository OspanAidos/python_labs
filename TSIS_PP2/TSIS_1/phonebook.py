import psycopg2
from psycopg2.extras import RealDictCursor
import json
import os
from config import params

def get_connection():
    """Создает подключение к базе данных."""
    return psycopg2.connect(**params)

# --- 1. ЭКСПОРТ В JSON ---
def export_to_json(filename="contacts_export.json"):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Собираем данные: контакт + его группа + массив телефонов
        query = """
            SELECT pb.first_name, pb.email, pb.birthday, g.name as group_name,
                   (SELECT json_agg(json_build_object('phone', ph.phone, 'type', ph.type)) 
                    FROM phones ph WHERE ph.contact_id = pb.user_id) as phones
            FROM phonebook pb
            LEFT JOIN groups g ON pb.group_id = g.id
        """
        cur.execute(query)
        data = cur.fetchall()
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, default=str)
        print(f"\n✅ Данные успешно экспортированы в {filename}")
        
    except Exception as e:
        print(f"\n❌ Ошибка при экспорте: {e}")
    finally:
        if conn: conn.close()

# --- 2. ИМПОРТ ИЗ JSON ---
def import_from_json(filename="contacts_import.json"):
    if not os.path.exists(filename):
        print(f"\n❌ Файл '{filename}' не найден. Создайте его для теста!")
        return

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        with open(filename, "r", encoding="utf-8") as f:
            contacts = json.load(f)
        
        for c in contacts:
            # Проверка дубликата по имени
            cur.execute("SELECT user_id FROM phonebook WHERE first_name = %s", (c['first_name'],))
            exists = cur.fetchone()
            
            if exists:
                ans = input(f"\n❓ Контакт '{c['first_name']}' уже существует. Перезаписать (o) или пропустить (s)? ").lower()
                if ans == 's': continue
                cur.execute("DELETE FROM phonebook WHERE user_id = %s", (exists[0],))

            # Вставка основного контакта
            cur.execute("""
                INSERT INTO phonebook (first_name, email, birthday) 
                VALUES (%s, %s, %s) RETURNING user_id
            """, (c['first_name'], c.get('email'), c.get('birthday')))
            new_id = cur.fetchone()[0]

            # Если в JSON есть список телефонов, вставляем их в таблицу phones
            if 'phones' in c and c['phones']:
                for p in c['phones']:
                    cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                                (new_id, p['phone'], p['type']))
        
        conn.commit()
        print("\n✅ Импорт завершен!")
        
    except Exception as e:
        print(f"\n❌ Ошибка при импорте: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()

# --- 3. ПОИСК, ФИЛЬТР, ПАГИНАЦИЯ ---
def advanced_search():
    query_str = input("\n🔎 Поиск (имя, email или телефон): ")
    conn = get_connection()
    cur = conn.cursor()
    # Вызываем нашу SQL-функцию из procedures.sql
    cur.execute("SELECT * FROM search_contacts_ext(%s)", (query_str,))
    results = cur.fetchall()
    
    print("\n" + "="*50)
    for r in results:
        print(f"ID: {r[0]} | Имя: {r[1]} | Email: {r[2]}")
        print(f"   Телефоны: {r[3] if r[3] else 'Нет данных'}")
    print("="*50)
    conn.close()

def view_paginated():
    limit = 5
    offset = 0
    conn = get_connection()
    cur = conn.cursor()
    
    while True:
        cur.execute("SELECT first_name, email FROM phonebook ORDER BY first_name LIMIT %s OFFSET %s", (limit, offset))
        rows = cur.fetchall()
        
        if not rows and offset == 0:
            print("\n📭 Книга пуста.")
            break
        
        print(f"\n--- Страница {(offset//limit)+1} ---")
        for row in rows:
            print(f"👤 {row[0]} - {row[1] if row[1] else 'нет email'}")
            
        cmd = input("\n[n]ext (след), [p]rev (пред), [q]uit (выход): ").lower()
        if cmd == 'n': 
            if len(rows) == limit: offset += limit
            else: print("Это последняя страница.")
        elif cmd == 'p': 
            if offset >= limit: offset -= limit
        elif cmd == 'q': break
    conn.close()

# --- 4. ГЛАВНОЕ МЕНЮ ---
def main_menu():
    while True:
        print("\n📱 PHONEBOOK EXTENDED SYSTEM")
        print("1. Расширенный поиск")
        print("2. Просмотр страниц (Пагинация)")
        print("3. Экспорт в JSON")
        print("4. Импорт из JSON")
        print("5. Добавить телефон (Процедура)")
        print("6. Сменить группу (Процедура)")
        print("0. Выход")
        
        choice = input("\nВыберите опцию: ")
        
        if choice == '1': advanced_search()
        elif choice == '2': view_paginated()
        elif choice == '3': export_to_json()
        elif choice == '4': import_from_json()
        elif choice == '5':
            name = input("Имя контакта: ")
            phone = input("Номер телефона: ")
            ptype = input("Тип (mobile/work/home): ")
            conn = get_connection(); cur = conn.cursor()
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
            conn.commit(); conn.close()
            print("✅ Телефон добавлен через процедуру!")
        elif choice == '6':
            name = input("Имя контакта: ")
            group = input("Новая группа: ")
            conn = get_connection(); cur = conn.cursor()
            cur.execute("CALL move_to_group(%s, %s)", (name, group))
            conn.commit(); conn.close()
            print("✅ Группа обновлена!")
        elif choice == '0': break
        else: print("❌ Неверный ввод")

if __name__ == "__main__":
    main_menu()