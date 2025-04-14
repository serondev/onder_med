from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                           QPushButton, QLabel, QMessageBox, QComboBox, QGroupBox)
from PyQt6.QtCore import QSettings, Qt
import google.generativeai as genai
import os

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("OnderMed", "IlacDanisman")
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # API Ayarları Grubu
        api_group = QGroupBox("API Ayarları")
        api_layout = QVBoxLayout()
        
        # Başlık ve açıklama
        title = QLabel("API Ayarları")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        
        description = QLabel(
            "Google Gemini API anahtarınızı buraya giriniz. "
            "API anahtarını almak için "
            "<a href='https://makersuite.google.com/app/apikey'>buraya tıklayın</a>."
        )
        description.setOpenExternalLinks(True)
        description.setWordWrap(True)
        description.setStyleSheet("margin-bottom: 20px;")
        
        # API giriş alanı
        api_input_layout = QHBoxLayout()
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("API Anahtarını buraya yapıştırın...")
        self.api_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.show_api = QPushButton("Göster")
        self.show_api.setCheckable(True)
        self.show_api.clicked.connect(self.toggle_api_visibility)
        
        self.test_button = QPushButton("Test Et")
        self.test_button.clicked.connect(self.test_api)
        
        self.save_button = QPushButton("Kaydet")
        self.save_button.clicked.connect(self.save_settings)
        
        api_input_layout.addWidget(self.api_input)
        api_input_layout.addWidget(self.show_api)
        api_input_layout.addWidget(self.test_button)
        api_input_layout.addWidget(self.save_button)
        
        # API durumu
        self.status_label = QLabel()
        self.status_label.setStyleSheet("margin-top: 10px;")
        
        # API layout'a ekle
        api_layout.addWidget(title)
        api_layout.addWidget(description)
        api_layout.addLayout(api_input_layout)
        api_layout.addWidget(self.status_label)
        api_group.setLayout(api_layout)
        
        # Ekran Ayarları Grubu
        display_group = QGroupBox("Ekran Ayarları")
        display_layout = QVBoxLayout()
        
        # Ekran modu seçimi
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Ekran Modu:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Pencere", "Tam Ekran"])
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        
        # Ölçeklendirme seçimi
        scale_layout = QHBoxLayout()
        scale_label = QLabel("Ölçeklendirme:")
        self.scale_combo = QComboBox()
        self.scale_combo.addItems(["100%", "125%", "150%", "175%", "200%"])
        scale_layout.addWidget(scale_label)
        scale_layout.addWidget(self.scale_combo)
        
        # Çözünürlük seçimi
        resolution_layout = QHBoxLayout()
        resolution_label = QLabel("Çözünürlük:")
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems([
            "800x600", "1024x768", "1280x720", 
            "1366x768", "1920x1080", "Otomatik"
        ])
        resolution_layout.addWidget(resolution_label)
        resolution_layout.addWidget(self.resolution_combo)
        
        # Ekran ayarları butonları
        display_buttons = QHBoxLayout()
        self.apply_display = QPushButton("Uygula")
        self.apply_display.clicked.connect(self.apply_display_settings)
        self.reset_display = QPushButton("Varsayılana Dön")
        self.reset_display.clicked.connect(self.reset_display_settings)
        display_buttons.addWidget(self.apply_display)
        display_buttons.addWidget(self.reset_display)
        
        # Ekran ayarları layout'a ekle
        display_layout.addLayout(mode_layout)
        display_layout.addLayout(scale_layout)
        display_layout.addLayout(resolution_layout)
        display_layout.addLayout(display_buttons)
        display_group.setLayout(display_layout)
        
        # Ana layout'a grupları ekle
        layout.addWidget(api_group)
        layout.addWidget(display_group)
        layout.addStretch()
        
    def toggle_api_visibility(self):
        if self.show_api.isChecked():
            self.api_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_api.setText("Gizle")
        else:
            self.api_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_api.setText("Göster")
    
    def test_api(self):
        api_key = self.api_input.text().strip()
        if not api_key:
            self.show_status("Lütfen API anahtarı girin!", "error")
            return
        
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Merhaba")
            
            self.show_status("API bağlantısı başarılı!", "success")
            self.save_button.setEnabled(True)
        except Exception as e:
            self.show_status(f"API hatası: {str(e)}", "error")
            self.save_button.setEnabled(False)
    
    def show_status(self, message, status_type):
        if status_type == "success":
            color = "#27ae60"
        elif status_type == "error":
            color = "#c0392b"
        else:
            color = "#2c3e50"
        
        self.status_label.setStyleSheet(f"color: {color}; margin-top: 10px;")
        self.status_label.setText(message)
    
    def save_settings(self):
        api_key = self.api_input.text().strip()
        if api_key:
            self.settings.setValue("api_key", api_key)
            QMessageBox.information(self, "Başarılı", "API anahtarı başarıyla kaydedildi!")
            self.show_status("Ayarlar kaydedildi!", "success")
    
    def apply_display_settings(self):
        # Ayarları kaydet
        self.settings.setValue("display/mode", self.mode_combo.currentText())
        self.settings.setValue("display/scale", self.scale_combo.currentText())
        self.settings.setValue("display/resolution", self.resolution_combo.currentText())
        
        # Ana pencereyi bul ve ayarları uygula
        main_window = self.window()
        
        # Önce tüm pencere durumlarını temizle
        main_window.setWindowState(Qt.WindowState.WindowNoState)
        
        # Ekran modu
        mode = self.mode_combo.currentText()
        if mode == "Tam Ekran":
            # Tam ekran modu - kontrol düğmeleri ile
            main_window.showMaximized()
            
            # Pencere boyutunu ekran boyutuna ayarla
            screen = main_window.screen()
            main_window.setGeometry(screen.availableGeometry())
        else:  # Pencere modu
            # Normal pencere moduna dön
            main_window.showNormal()
            
            # Varsayılan boyutu ayarla
            resolution = self.resolution_combo.currentText()
            if resolution != "Otomatik":
                width, height = map(int, resolution.split("x"))
                main_window.resize(width, height)
            else:
                # Varsayılan boyut
                main_window.resize(1200, 800)
            
            # Ekranın ortasına konumlandır
            screen_geometry = main_window.screen().geometry()
            x = (screen_geometry.width() - main_window.width()) // 2
            y = (screen_geometry.height() - main_window.height()) // 2
            main_window.move(x, y)
        
        # Ölçeklendirme
        scale = float(self.scale_combo.currentText().replace("%", "")) / 100.0
        
        QMessageBox.information(self, "Başarılı", "Ekran ayarları uygulandı!")
    
    def reset_display_settings(self):
        # Varsayılan değerlere dön
        self.mode_combo.setCurrentText("Pencere")
        self.scale_combo.setCurrentText("100%")
        self.resolution_combo.setCurrentText("Otomatik")
        
        # Ayarları uygula
        self.apply_display_settings()
    
    def load_settings(self):
        # API ayarlarını yükle
        api_key = self.settings.value("api_key", "")
        self.api_input.setText(api_key)
        
        # Ekran ayarlarını yükle
        self.mode_combo.setCurrentText(self.settings.value("display/mode", "Pencere"))
        self.scale_combo.setCurrentText(self.settings.value("display/scale", "100%"))
        self.resolution_combo.setCurrentText(self.settings.value("display/resolution", "Otomatik")) 