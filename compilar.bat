@echo off
echo ============================================
echo   COMPILADOR - Descarregador de Videos
echo ============================================
echo.

REM Verificar se FFmpeg existe
if not exist "ffmpeg_bin\ffmpeg.exe" (
    echo [AVISO] FFmpeg nao encontrado!
    echo.
    echo Para criar executavel com redimensionamento integrado:
    echo   1. Execute: python download_ffmpeg.py
    echo   2. Aguarde download completar
    echo   3. Execute novamente este script
    echo.
    choice /C SN /M "Deseja baixar FFmpeg agora? (S/N)"
    if errorlevel 2 goto :continue
    if errorlevel 1 (
        echo.
        echo Baixando FFmpeg...
        C:\Users\CSTE2\AppData\Local\Programs\Python\Python314\python.exe download_ffmpeg.py
        if errorlevel 1 (
            echo Erro ao baixar. Continuando sem FFmpeg...
            timeout /t 3
            goto :continue
        )
        echo.
    )
)

:continue
echo.
echo Iniciando compilacao...
echo.

REM Verificar se deve adicionar FFmpeg
set FFMPEG_ARG=
if exist "ffmpeg_bin\ffmpeg.exe" (
    echo [OK] Incluindo FFmpeg no executavel...
    set FFMPEG_ARG=--add-data=ffmpeg_bin;ffmpeg_bin
    echo.
)

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
    %FFMPEG_ARG% ^
    saca_videos.py

echo.
echo ============================================
echo   COMPILACAO CONCLUIDA!
echo ============================================
echo.
echo O executavel esta em: .\dist\DescarregadorVideos.exe
echo.

if exist "ffmpeg_bin\ffmpeg.exe" (
    echo [OK] FFmpeg INCLUIDO - Funciona em qualquer PC!
) else (
    echo [AVISO] FFmpeg NAO incluido - Redimensionamento requer instalacao
)

echo.
echo Pode copiar este arquivo para qualquer PC Windows
echo e executar sem precisar de Python instalado!
echo.
pause
