import os
import sys

# Proje kök dizinini Python path'ine ekle
if getattr(sys, 'frozen', False):
    # PyInstaller ile paketlenmiş
    application_path = sys._MEIPASS
    # Modül yolunu ekle
    sys.path.insert(0, application_path)
else:
    # Normal Python çalışma zamanı
    application_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(application_path))

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # Veritabanı dizininin yolunu ayarla
    os.makedirs(os.path.join(application_path, "database"), exist_ok=True)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 