from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, 
                           QPushButton, QLabel)

class AIConsultantTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Soru girişi
        self.question_label = QLabel("Sorunuzu yazın:")
        self.question_input = QTextEdit()
        self.question_input.setMaximumHeight(100)
        
        # Gönder butonu
        self.send_button = QPushButton("Danış")
        self.send_button.clicked.connect(self.get_ai_response)
        
        # Cevap alanı
        self.response_label = QLabel("Yapay Zeka Cevabı:")
        self.response_area = QTextEdit()
        self.response_area.setReadOnly(True)
        
        layout.addWidget(self.question_label)
        layout.addWidget(self.question_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.response_label)
        layout.addWidget(self.response_area)
        
    def get_ai_response(self):
        question = self.question_input.toPlainText()
        # Burada yapay zeka API'sine istek atacağız
        # Şimdilik örnek bir cevap gösterelim
        self.response_area.setText(f"Sorunuz: {question}\n\nYanıt işleniyor...") 