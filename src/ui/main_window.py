from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                           QLabel, QHBoxLayout, QScrollArea, QCheckBox, QPushButton,
                           QDialog)
from PyQt6.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt6.QtCore import Qt, QTimer, QSettings
from ui.tabs.drug_info_tab import DrugInfoTab
from ui.tabs.interaction_tab import InteractionTab
from ui.tabs.symptom_tab import SymptomTab
from ui.tabs.chat_tab import ChatTab
from ui.tabs.settings_tab import SettingsTab
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Önder Med - İlaç Danışmanı")
        self.setGeometry(100, 100, 1200, 800)
        
        # Kaynak dosyaları için temel dizin
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.resources_dir = os.path.join(self.base_dir, 'resources', 'images')
        
        # Pencere ikonu
        icon_path = os.path.join(self.resources_dir, 'logo_small.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setup_ui()
        self.setup_style()
        
        # Ayarları yükle ve tutorial'ı göster
        self.settings = QSettings("OnderMed", "IlacDanisman")
        show_tutorial = self.settings.value("show_tutorial", True, type=bool)
        if show_tutorial:
            self.show_tutorial()

    def setup_ui(self):
        # Ana widget ve layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header bölümü (logo ve bekletme yazısı için)
        header_layout = QHBoxLayout()
        
        # Bekletme yazısı
        self.waiting_label = QLabel("Lütfen Bekleyiniz...")
        self.waiting_label.setStyleSheet("""
            QLabel {
                color: #e74c3c;  /* Kırmızı renk */
                font-size: 24px;  /* Daha büyük yazı */
                font-weight: bold;
                padding: 10px;
                margin-left: 50px;  /* Sola doğru kaydır */
            }
        """)
        self.waiting_label.hide()  # Başlangıçta gizli
        
        # Yanıp sönme efekti için timer
        self.blink_timer = QTimer(self)
        self.blink_timer.setInterval(800)  # 800ms aralıkla yanıp sönme
        self.blink_timer.timeout.connect(self.blink_waiting_text)
        self.blink_opacity = 1.0
        self.blink_direction = -0.2  # Opaklık değişim miktarı
        
        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(self.resources_dir, 'logo_medium.png')
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            scaled_logo = logo_pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_logo)
            logo_label.setStyleSheet("padding: 10px; margin-right: 20px;")
        
        # Layout'a ekle
        header_layout.addStretch(1)  # Sol tarafta az boşluk
        header_layout.addWidget(self.waiting_label)  # Bekletme yazısı
        header_layout.addStretch(2)  # Sağ tarafta daha fazla boşluk
        header_layout.addWidget(logo_label)  # Logo en sağda
        
        # Tab widget oluşturma
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        
        # Sekme değişikliğini takip et
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        # Sekmeleri ekle
        drug_info_tab = DrugInfoTab()
        drug_info_tab.set_main_window(self)
        self.tabs.addTab(drug_info_tab, "İlaç Bilgisi")
        
        interaction_tab = InteractionTab()
        interaction_tab.set_main_window(self)
        self.tabs.addTab(interaction_tab, "İlaç Etkileşimleri")
        
        symptom_tab = SymptomTab()
        symptom_tab.set_main_window(self)
        self.tabs.addTab(symptom_tab, "Belirti Analizi")
        
        chat_tab = ChatTab()
        chat_tab.set_main_window(self)
        self.tabs.addTab(chat_tab, "Hasta Şikayet Değerlendirme")
        
        settings_tab = SettingsTab()
        self.tabs.addTab(settings_tab, "⚙️ Ayarlar")
        
        # Layout'a widget'ları ekle
        layout.addLayout(header_layout)
        layout.addWidget(self.tabs)
        
    def setup_style(self):
        # Ana renk paleti
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#2c3e50"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#f5f5f5"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#3498db"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
        self.setPalette(palette)
        
        # Stil sayfası
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                color: #2c3e50;
                padding: 8px 16px;
                margin: 2px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                font-size: 14px;
                min-height: 20px;
            }
            QTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                font-size: 15px;
                line-height: 1.6;
                background-color: #ffffff;
                selection-background-color: #cce5ff;
            }
            QTextEdit#responseArea {
                background-color: #ffffff;
                font-family: "Segoe UI", Arial, sans-serif;
                padding: 20px;
                line-height: 1.8;
            }
            QLabel {
                font-size: 14px;
                color: #2c3e50;
                padding: 5px 0;
            }
            QTextEdit#chatHistory {
                background-color: #f8f9fa;
                font-family: Arial;
                padding: 15px;
            }
            /* Kaydırma çubuğu stilleri */
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """) 

    def blink_waiting_text(self):
        # Opaklığı değiştir
        self.blink_opacity += self.blink_direction
        if self.blink_opacity <= 0.5 or self.blink_opacity >= 1.0:  # Minimum opaklığı artırdık
            self.blink_direction *= -1  # Yönü tersine çevir
        
        # Stil sayfasını güncelle
        self.waiting_label.setStyleSheet(f"""
            QLabel {{
                color: #e74c3c;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
                margin-left: 50px;
                opacity: {self.blink_opacity};
            }}
        """)
    
    def show_waiting(self):
        self.waiting_label.show()
        self.blink_timer.start()
    
    def hide_waiting(self):
        self.waiting_label.hide()
        self.blink_timer.stop()
    
    def on_tab_changed(self, index):
        # Sekme değiştiğinde bekletme yazısını gizle
        self.hide_waiting() 

    def show_tutorial(self):
        tutorial = QDialog(self)
        tutorial.setWindowTitle("Hoş Geldiniz!")
        tutorial.setFixedSize(800, 600)
        
        layout = QVBoxLayout(tutorial)
        
        # Başlık
        title = QLabel("Önder Med - İlaç Danışmanı'na Hoş Geldiniz!")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin: 20px 0;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Açıklama metni
        description = QLabel("""
            <p style='font-size: 16px; line-height: 1.6;'>
            Bu uygulama ile yapabilecekleriniz:
            </p>
            
            <ul style='font-size: 14px; line-height: 1.8;'>
                <li><b>İlaç Bilgisi:</b> İlaçlar hakkında detaylı bilgi alabilirsiniz.</li>
                <li><b>İlaç Etkileşimleri:</b> İki ilacın birbiriyle etkileşimini kontrol edebilirsiniz.</li>
                <li><b>Belirti Analizi:</b> Belirtilerinize göre olası durumları öğrenebilirsiniz.</li>
                <li><b>Hasta Şikayet Değerlendirme:</b> Şikayetlerinizi yapay zeka ile analiz edebilirsiniz.</li>
            </ul>
            
            <p style='font-size: 14px; color: #e74c3c; margin-top: 20px;'>
            <b>Önemli Not:</b> Bu uygulama bir sağlık profesyonelinin yerini tutmaz. 
            Tüm tıbbi kararlar için mutlaka bir doktora danışınız.
            </p>
            
            <p style='font-size: 14px; margin-top: 20px;'>
            <b>Başlamadan Önce:</b> Ayarlar sekmesinden API anahtarınızı girmeyi unutmayın!
            </p>
        """)
        description.setWordWrap(True)
        description.setTextFormat(Qt.TextFormat.RichText)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidget(description)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
        """)
        
        # "Bir daha gösterme" checkbox'ı
        dont_show = QCheckBox("Bir daha gösterme")
        dont_show.setStyleSheet("margin-top: 10px;")
        
        # Tamam butonu
        ok_button = QPushButton("Anladım")
        ok_button.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        ok_button.clicked.connect(lambda: self.close_tutorial(tutorial, dont_show.isChecked()))
        
        # Layout'a widget'ları ekle
        layout.addWidget(title)
        layout.addWidget(scroll)
        layout.addWidget(dont_show)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Dialog'u göster
        tutorial.exec()
    
    def close_tutorial(self, dialog, dont_show_again):
        if dont_show_again:
            self.settings.setValue("show_tutorial", False)
        dialog.accept() 