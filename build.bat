@echo off
echo Building OnderMed...

:: Python virtual environment oluştur ve aktive et
python -m venv venv
call venv\Scripts\activate

:: Gerekli paketleri yükle
pip install -r requirements.txt
pip install pyinstaller

:: PyInstaller ile exe oluştur
pyinstaller --name="OnderMed" ^
            --windowed ^
            --icon="src/resources/images/logo_small.ico" ^
            --add-data="src/resources/images;resources/images" ^
            --hidden-import=PyQt6.QtCore ^
            --hidden-import=PyQt6.QtGui ^
            --hidden-import=PyQt6.QtWidgets ^
            src/main.py

:: Virtual environment'ı deaktive et
deactivate

echo Build completed!
pause 