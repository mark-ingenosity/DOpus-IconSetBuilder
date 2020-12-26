@echo off
:: Run IconSetBuilder

:: activate the python environment and run IconSetBuilder.py with arguments
cmd /k ".\lib\python\Scripts\activate.bat & python .\lib\IconSetBuilder.py %* & exit"
