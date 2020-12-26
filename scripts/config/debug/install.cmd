@echo off
:: IconSet Builder Installation

:: Extract the IconSetBuilder archive
echo Installing IconSetBuilder...
powershell.exe -command "Expand-Archive IconSetBuilder.zip"
cd IconSetBuilder

:: Setup a local python virtual environment
echo creating the python environment...
python3 -m venv .\lib\python
cmd /k ".\lib\python\Scripts\activate.bat & python.exe -m pip install --upgrade pip & pip install vkbeautify Pillow dpath ruamel.yaml & exit"

echo.
echo IconSetBuilder setup complete.
echo Run "IconSetBuilder.cmd -i example\iconsetcfg.json" to create an example DOpus iconset.
echo.

