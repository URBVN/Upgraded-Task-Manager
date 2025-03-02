import pytest
import mysql.connector
from unittest.mock import patch
from Main_v2 import pridat_ukol, aktualizovat_ukol, odstranit_ukol

def pripojeni_test_db():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "test",
        database = "test_task_manager"
    )

@pytest.fixture(scope = "function")
def test_db():
    conn = pripojeni_test_db()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS ukoly")
    cursor.execute('''
        CREATE TABLE ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(255) NOT NULL,
            popis TEXT NOT NULL,
            stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
            datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    
    yield conn
    
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS ukoly")
    conn.commit()
    cursor.close()
    conn.close()

def test_pridat_ukol_pozitivni(test_db):
    with patch('Main_v2.pripojeni_db', return_value = test_db), \
         patch('builtins.input', side_effect = ["Test úkol", "Test popis"]), \
         patch.object(test_db, 'close', lambda: None):
        
        pridat_ukol()
    
    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM ukoly")
    result = cursor.fetchall()
    cursor.close()
    assert len(result) == 1

def test_pridat_ukol_negativni(test_db):
    with patch('Main_v2.pripojeni_db', return_value = test_db), \
         patch('builtins.input', side_effect = ["", ""]), \
         patch.object(test_db, 'close', lambda: None):
        
        pridat_ukol()
    
    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM ukoly")
    result = cursor.fetchall()
    cursor.close()
    assert len(result) == 0

def test_aktualizovat_ukol_pozitivni(test_db):
    cursor = test_db.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Test", "Test"))
    test_db.commit()
    task_id = cursor.lastrowid
    cursor.close()

    with patch('Main_v2.pripojeni_db', return_value = test_db), \
         patch('builtins.input', side_effect=[str(task_id), "Hotovo"]), \
         patch.object(test_db, 'close', lambda: None):
        
        aktualizovat_ukol()
    
    cursor = test_db.cursor()
    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (task_id,))
    result = cursor.fetchone()[0]
    cursor.close()
    assert result == "Hotovo"

def test_aktualizovat_ukol_negativni(test_db):
    with patch('Main_v2.pripojeni_db', return_value = test_db), \
         patch('builtins.input', side_effect=["9999", "Hotovo"]), \
         patch.object(test_db, 'close', lambda: None):
        
        aktualizovat_ukol()
    
    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM ukoly")
    result = cursor.fetchall()
    cursor.close()
    assert len(result) == 0

def test_odstranit_ukol_pozitivni(test_db):
    cursor = test_db.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", ("Test", "Test"))
    test_db.commit()
    task_id = cursor.lastrowid
    cursor.close()

    with patch('Main_v2.pripojeni_db', return_value = test_db), \
         patch('builtins.input', side_effect = [str(task_id)]), \
         patch.object(test_db, 'close', lambda: None):
        
        odstranit_ukol()
    
    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (task_id,))
    result = cursor.fetchall()
    cursor.close()
    assert len(result) == 0

def test_odstranit_ukol_negativni(test_db):
    with patch('Main_v2.pripojeni_db', return_value = test_db), \
         patch('builtins.input', side_effect = ["9999"]), \
         patch.object(test_db, 'close', lambda: None):
        
        odstranit_ukol()
    
    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM ukoly")
    result = cursor.fetchall()
    cursor.close()
    assert len(result) == 0
