@echo off
echo ============================================
echo   Git Setup - Media Download Project
echo ============================================
echo.

REM Verificar se git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Git nao esta instalado!
    echo Por favor, instale o Git: https://git-scm.com/
    pause
    exit /b 1
)

echo [1/5] Inicializando repositorio Git...
git init

echo.
echo [2/5] Adicionando remote origin...
git remote remove origin 2>nul
git remote add origin https://github.com/Rui-Kaz/Media_Download.git

echo.
echo [3/5] Adicionando arquivos...
git add .

echo.
echo [4/5] Criando commit inicial...
git commit -m "Initial commit: Media Download application with GUI"

echo.
echo [5/5] Enviando para GitHub (branch main)...
git branch -M main
git push -u origin main --force

echo.
echo ============================================
echo   PUBLICACAO CONCLUIDA!
echo ============================================
echo.
echo Repositorio: https://github.com/Rui-Kaz/Media_Download
echo.
pause
