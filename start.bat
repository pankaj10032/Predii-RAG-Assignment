@echo off
echo ====================================
echo RAG System Launcher
echo ====================================
echo.
echo Choose how to run the system:
echo.
echo 1. Web Interface (Gradio)
echo 2. Command Line Interface
echo 3. Run Tests
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto web
if "%choice%"=="2" goto cli
if "%choice%"=="3" goto test
if "%choice%"=="4" goto end

:web
echo.
echo Starting Web Interface...
echo Opening in browser at http://localhost:7860
echo.
python app.py
goto end

:cli
echo.
echo Starting Command Line Interface...
echo.
python unified_rag_system.py
goto end

:test
echo.
echo Running Tests...
echo.
python test_simple.py
pause
goto end

:end
echo.
echo Goodbye!
pause
