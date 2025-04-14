from PyQt6.QtCore import QObject, pyqtSignal

class AIWorker(QObject):
    finished = pyqtSignal(str)  # İşlem bittiğinde sinyal gönder
    error = pyqtSignal(str)     # Hata durumunda sinyal gönder
    
    def __init__(self, ai_client, prompt, method):
        super().__init__()
        self.ai_client = ai_client
        self.prompt = prompt
        self.method = method
    
    def run(self):
        try:
            if self.method == "drug_info":
                response = self.ai_client.get_drug_info(self.prompt)
            elif self.method == "interaction":
                response = self.ai_client.get_drug_interaction(self.prompt)
            elif self.method == "symptom":
                response = self.ai_client.get_drug_advice(self.prompt)
            elif self.method == "chat":
                response = self.ai_client.get_pharmacist_response(self.prompt)
            
            self.finished.emit(response)
        except Exception as e:
            self.error.emit(str(e)) 