import sqlite3
from typing import List, Optional
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.drug import Drug
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_path: str = None):
        if db_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(current_dir, "drugs.db")
            print(f"Veritabanı yolu: {self.db_path}")  # Debug için
        else:
            self.db_path = db_path
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS drugs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    active_ingredients TEXT NOT NULL,
                    usage_instructions TEXT NOT NULL,
                    side_effects TEXT NOT NULL,
                    dosage TEXT NOT NULL,
                    interactions TEXT
                )
            ''')
            conn.commit()
    
    def get_drug_by_name(self, name: str) -> Optional[Drug]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM drugs WHERE name LIKE ?", (f"%{name}%",))
            row = cursor.fetchone()
            print(f"Aranan ilaç: {name}, Sonuç: {row}")  # Debug için
            if row:
                return Drug.from_dict({
                    'id': row[0],
                    'name': row[1],
                    'active_ingredients': row[2].split(','),
                    'usage_instructions': row[3],
                    'side_effects': row[4].split(','),
                    'dosage': row[5],
                    'interactions': row[6].split(',') if row[6] else []
                })
        return None
        
    def get_all_drugs(self) -> List[Drug]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM drugs")
            rows = cursor.fetchall()
            return [Drug.from_dict({
                'id': row[0],
                'name': row[1],
                'active_ingredients': row[2].split(','),
                'usage_instructions': row[3],
                'side_effects': row[4].split(','),
                'dosage': row[5],
                'interactions': row[6].split(',') if row[6] else []
            }) for row in rows] 