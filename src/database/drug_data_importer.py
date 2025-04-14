import json
import requests
from db_manager import DatabaseManager

class DrugDataImporter:
    def __init__(self):
        self.db_manager = DatabaseManager()
        
    def import_from_json(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            drugs = json.load(f)
            
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            for drug in drugs:
                cursor.execute("""
                    INSERT INTO drugs (
                        name, active_ingredients, usage_instructions,
                        side_effects, dosage, interactions
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    drug["name"],
                    ",".join(drug["active_ingredients"]),
                    drug["usage_instructions"],
                    ",".join(drug["side_effects"]),
                    drug["dosage"],
                    ",".join(drug["interactions"])
                ))
            conn.commit()

    def import_common_drugs(self):
        # Türkiye'de sık kullanılan ilaçların listesi
        common_drugs = [
            {
                "name": "Majezik",
                "active_ingredients": ["Flurbiprofen"],
                "usage_instructions": "Ağrı ve iltihap tedavisinde kullanılır. Yemeklerden sonra alınmalıdır.",
                "side_effects": ["Mide rahatsızlığı", "Baş dönmesi", "Mide kanaması riski"],
                "dosage": "100mg tablet",
                "interactions": ["Aspirin", "Varfarin", "Diğer NSAİ ilaçlar"]
            },
            {
                "name": "Voltaren",
                "active_ingredients": ["Diklofenak"],
                "usage_instructions": "Ağrı ve iltihap tedavisinde kullanılır. Yemeklerden sonra alınmalıdır.",
                "side_effects": ["Mide rahatsızlığı", "Baş ağrısı", "Mide kanaması riski"],
                "dosage": "75mg tablet",
                "interactions": ["Aspirin", "Varfarin", "Diğer NSAİ ilaçlar"]
            },
            {
                "name": "Augmentin",
                "active_ingredients": ["Amoksisilin", "Klavulanik asit"],
                "usage_instructions": "Bakteriyel enfeksiyonların tedavisinde kullanılır. Günde 2-3 kez alınmalıdır.",
                "side_effects": ["İshal", "Bulantı", "Döküntü", "Kaşıntı"],
                "dosage": "1000mg tablet",
                "interactions": ["Alkol", "Metotreksat", "Allopurinol"]
            },
            {
                "name": "Nexium",
                "active_ingredients": ["Esomeprazol"],
                "usage_instructions": "Mide asidi fazlalığı ve reflü tedavisinde kullanılır.",
                "side_effects": ["Baş ağrısı", "İshal", "Karın ağrısı"],
                "dosage": "40mg tablet",
                "interactions": ["Nelfinavir", "Klopidogrel", "Demir preparatları"]
            },
            {
                "name": "Xanax",
                "active_ingredients": ["Alprazolam"],
                "usage_instructions": "Anksiyete tedavisinde kullanılır. Doktor kontrolünde kullanılmalıdır.",
                "side_effects": ["Uyku hali", "Baş dönmesi", "Bağımlılık riski"],
                "dosage": "0.5mg tablet",
                "interactions": ["Alkol", "Opioidler", "Antidepresanlar"]
            },
            {
                "name": "Cipro",
                "active_ingredients": ["Siprofloksasin"],
                "usage_instructions": "Bakteriyel enfeksiyonların tedavisinde kullanılır.",
                "side_effects": ["Bulantı", "İshal", "Baş ağrısı", "Tendon problemleri"],
                "dosage": "500mg tablet",
                "interactions": ["Antasitler", "Demir preparatları", "Süt ürünleri"]
            },
            {
                "name": "Glucophage",
                "active_ingredients": ["Metformin"],
                "usage_instructions": "Tip 2 diyabet tedavisinde kullanılır. Yemeklerle birlikte alınmalıdır.",
                "side_effects": ["Mide bulantısı", "İshal", "Vitamin B12 eksikliği"],
                "dosage": "1000mg tablet",
                "interactions": ["Alkol", "İyotlu kontrast maddeler", "Diüretikler"]
            },
            {
                "name": "Euthyrox",
                "active_ingredients": ["Levotiroksin"],
                "usage_instructions": "Tiroid hormonu eksikliğinde kullanılır. Aç karnına alınmalıdır.",
                "side_effects": ["Çarpıntı", "Terleme", "Kilo kaybı", "Uykusuzluk"],
                "dosage": "100mcg tablet",
                "interactions": ["Demir preparatları", "Kalsiyum", "Antasitler"]
            },
            {
                "name": "Coraspin",
                "active_ingredients": ["Asetilsalisilik asit"],
                "usage_instructions": "Kan sulandırıcı olarak kullanılır.",
                "side_effects": ["Mide rahatsızlığı", "Kanama riski"],
                "dosage": "100mg tablet",
                "interactions": ["NSAİ ilaçlar", "Varfarin", "Heparin"]
            },
            {
                "name": "Ventolin",
                "active_ingredients": ["Salbutamol"],
                "usage_instructions": "Astım ve KOAH tedavisinde kullanılır.",
                "side_effects": ["Çarpıntı", "Tremor", "Baş ağrısı"],
                "dosage": "2mg tablet",
                "interactions": ["Beta blokerler", "Diüretikler", "Digoksin"]
            }
        ]
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            for drug in common_drugs:
                cursor.execute("""
                    INSERT INTO drugs (
                        name, active_ingredients, usage_instructions,
                        side_effects, dosage, interactions
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    drug["name"],
                    ",".join(drug["active_ingredients"]),
                    drug["usage_instructions"],
                    ",".join(drug["side_effects"]),
                    drug["dosage"],
                    ",".join(drug["interactions"])
                ))
            conn.commit() 