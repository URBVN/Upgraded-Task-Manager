import mysql.connector

def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="test", 
            database="task_manager"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Chyba připojení k databázi: {err}")
        return None

def vytvoreni_tabulky():
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT NOT NULL,
                stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
                datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()

def pridat_ukol():
    nazev = input("\nZadejte název úkolu: ").strip()
    popis = input("Zadejte popis úkolu: ").strip()
    if not nazev or not popis:
        print("Název i popis jsou povinné!")
        return
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
        conn.commit()
        print(f"Úkol '{nazev}' byl přidán.")
        cursor.close()
        conn.close()

def zobrazit_ukoly():
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nazev, popis, stav FROM ukoly WHERE stav IN ('Nezahájeno', 'Probíhá')")
        ukoly = cursor.fetchall()
        if not ukoly:
            print("\nSeznam úkolů je prázdný.")
        else:
            print("\nSeznam úkolů:")
            for ukol in ukoly:
                print(f"{ukol[0]}. {ukol[1]} - {ukol[2]} [{ukol[3]}]")
        cursor.close()
        conn.close()

def aktualizovat_ukol():
    zobrazit_ukoly()
    try:
        id_ukolu = int(input("\nZadejte ID úkolu pro aktualizaci: "))
        conn = pripojeni_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
            if cursor.fetchone() is None:
                print("Úkol s tímto ID neexistuje.")
                cursor.close()
                conn.close()
                return
            
            novy_stav = input("Nový stav (Probíhá/Hotovo): ").strip().capitalize()
            if novy_stav not in ["Probíhá", "Hotovo"]:
                print("Neplatný stav!")
                cursor.close()
                conn.close()
                return
            
            cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, id_ukolu))
            conn.commit()
            print("Úkol byl aktualizován.")
            cursor.close()
            conn.close()
    except ValueError:
        print("Neplatné ID!")

def odstranit_ukol():
    zobrazit_ukoly()
    try:
        id_ukolu = int(input("\nZadejte ID úkolu pro odstranění: "))
        conn = pripojeni_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ukoly WHERE id = %s", (id_ukolu,))
            if not cursor.fetchone():
                print("Úkol s tímto ID neexistuje.")
                cursor.close()
                conn.close()
                return
            
            cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
            conn.commit()
            print("Úkol byl odstraněn.")
            cursor.close()
            conn.close()
    except ValueError:
        print("Neplatné ID!")

def hlavni_menu():
    vytvoreni_tabulky()
    while True:
        print("\nSprávce úkolů - Hlavní menu:")
        print("1 - Přidat nový úkol")
        print("2 - Zobrazit úkoly")
        print("3 - Aktualizovat úkol")
        print("4 - Odstranit úkol")
        print("5 - Konec programu")
        volba = input("\nVyberte možnost (1-5): ")
        if volba == "1":
            pridat_ukol()
        elif volba == "2":
            zobrazit_ukoly()
        elif volba == "3":
            aktualizovat_ukol()
        elif volba == "4":
            odstranit_ukol()
        elif volba == "5":
            print("\nKonec programu.")
            break
        else:
            print("Neplatná volba, zkuste to znovu.")

if __name__ == "__main__":
    hlavni_menu()