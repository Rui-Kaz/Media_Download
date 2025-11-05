@echo off
echo ============================================
echo   COMPILADOR - Descarregador de Videos
echo ============================================
echo.
echo Iniciando compilacao...
echo.

C:\Users\CSTE2\AppData\Local\Programs\Python\Python314\python.exe -m PyInstaller ^
    --name=DescarregadorVideos ^
    --onefile ^
    --windowed ^
    --clean ^
    --noconfirm ^
    --hidden-import=yt_dlp ^
    --hidden-import=tkinter ^
    --hidden-import=threading ^
    --hidden-import=warnings ^
    --collect-all=yt_dlp ^
    --optimize=2 ^
    saca_videos.py

echo.
echo ============================================
echo   COMPILACAO CONCLUIDA!
echo ============================================
echo.
echo O executavel esta em: .\dist\DescarregadorVideos.exe
echo.
echo Pode copiar este arquivo para qualquer PC Windows
echo e executar sem precisar de Python instalado!
echo.
pause
