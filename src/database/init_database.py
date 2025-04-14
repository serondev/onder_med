import os
import sys

# Proje kök dizinini Python path'ine ekle
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from database.db_manager import DatabaseManager
from database.drug_data_importer import DrugDataImporter
from database.titck_scraper import TITCKScraper

def init_database():
    # Eğer veritabanı dosyası varsa sil
    db_path = os.path.join(os.path.dirname(__file__), "drugs.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Veritabanını oluştur
    db = DatabaseManager()
    db.init_db()
    
    # Yaygın ilaçları ekle
    importer = DrugDataImporter()
    importer.import_common_drugs()
    
    # TİTCK'den ilaçları çek ve ekle
    print("TİTCK'den ilaç verileri çekiliyor...")
    scraper = TITCKScraper()
    scraper.fetch_and_save_drugs()
    
    print("Veritabanı başarıyla oluşturuldu ve veriler eklendi!")

if __name__ == "__main__":
    init_database() 