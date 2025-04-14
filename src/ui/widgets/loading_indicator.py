from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QMovie
import os

class LoadingIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.hide()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Arka planı saydam yap
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Ana container
        self.container = QWidget(self)
        container_layout = QVBoxLayout(self.container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Yükleme etiketi
        self.loading_label = QLabel()
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        gif_path = os.path.join(base_dir, 'resources', 'images', 'loading.gif')
        
        if os.path.exists(gif_path):
            self.movie = QMovie(gif_path)
            self.movie.setScaledSize(QSize(64, 64))
            self.loading_label.setMovie(self.movie)
            self.loading_label.setFixedSize(64, 64)
        else:
            self.loading_label.setText("Yükleniyor...")
            
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # "Yanıt bekleniyor..." yazısı
        self.text_label = QLabel("Yanıt bekleniyor...")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet("""
            color: #2980b9;
            font-size: 14px;
            font-weight: bold;
            margin-top: 10px;
        """)
        
        # Widget'ları container'a ekle
        container_layout.addWidget(self.loading_label)
        container_layout.addWidget(self.text_label)
        
        # Container'ı ana layout'a ekle
        layout.addWidget(self.container)
        
        # Container stil
        self.container.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
                border: 1px solid #cccccc;
            }
        """)
        
        # Minimum boyutlar
        self.setMinimumSize(200, 150)
        
    def showEvent(self, event):
        super().showEvent(event)
        # Widget gösterildiğinde ortala
        if self.parent():
            self.move(
                (self.parent().width() - self.width()) // 2,
                (self.parent().height() - self.height()) // 2
            )
        
    def start(self):
        if hasattr(self, 'movie'):
            self.movie.start()
        self.raise_()  # En üstte göster
        self.show()
        
    def stop(self):
        if hasattr(self, 'movie'):
            self.movie.stop()
        self.hide() 