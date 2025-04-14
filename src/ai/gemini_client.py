import os
import google.generativeai as genai
from dotenv import load_dotenv
from PyQt6.QtCore import QSettings

class GeminiClient:
    def __init__(self):
        # Önce QSettings'den API anahtarını kontrol et
        settings = QSettings("OnderMed", "IlacDanisman")
        api_key = settings.value("api_key")
        
        if not api_key:
            # QSettings'de yoksa .env dosyasını kontrol et
            load_dotenv()
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("API anahtarı bulunamadı! Lütfen Ayarlar sekmesinden API anahtarınızı girin.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def get_drug_advice(self, symptoms: str) -> str:
        prompt = f"""
        Ben bir eczacı asistanıyım. Aşağıdaki belirtilere göre ilaç önerisi yapmam gerekiyor:
        Belirtiler: {symptoms}
        
        Lütfen:
        1. Bu belirtilere uygun olabilecek ilaçları öner
        2. Her ilacın kullanım amacını belirt
        3. Önemli uyarıları ekle
        4. Doktora başvurulması gereken durumları belirt
        
        NOT: Bu sadece bilgilendirme amaçlıdır, kesin teşhis ve tedavi için mutlaka bir doktora başvurulmalıdır.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
        
    def get_drug_interaction(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
        
    def get_pharmacist_response(self, user_message: str) -> str:
        prompt = f"""
        Ben bir eczacı asistanıyım. Kullanıcının sorusuna profesyonel ve yardımcı bir şekilde cevap vermeliyim.
        
        Kullanıcı sorusu: {user_message}
        
        Lütfen:
        1. Soruyu dikkatlice analiz et
        2. İlaçlar ve sağlık konusunda doğru bilgiler ver
        3. Gerektiğinde doktora yönlendir
        4. Önemli uyarıları ekle
        
        NOT: Bu bilgiler sadece bilgilendirme amaçlıdır.
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def get_drug_info(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text 