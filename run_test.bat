@echo off
echo ========================================
echo RAG System - Comprehensive Test Runner
echo ========================================
echo.
echo Running comprehensive test suite...
echo This will test all 40 queries across 5 categories
echo.

python run_comprehensive_test.py

echo.
echo ========================================
echo Test completed! Check the JSON output file for detailed results.
echo ========================================
pause