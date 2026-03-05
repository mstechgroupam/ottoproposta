@echo off
chcp 65001 > nul
echo =============================================
echo   Otto Energia Solar - Gerador de Propostas
echo =============================================
echo.
echo Iniciando servidor...
echo Acesse: http://localhost:5000
echo.
echo Para parar: Ctrl+C
echo.
python app.py
pause
