@echo off
:: IconSet Builder Setup
:: Usage: run this script once to setup the Python environment for the app

echo Setting up IconSetBuilder for first use... please be patient

echo Creating the python environment
python3 -m venv .\lib\python
cmd /k ".\lib\python\Scripts\activate.bat & python.exe -m pip install --upgrade pip & pip install vkbeautify Pillow dpath ruamel.yaml & exit"

echo.
echo Setup complete. You can delete this setup.cmd file
echo Run "IconSetBuilder.cmd -i example\iconsetcfg.json" to create an example DOpus iconset
echo.

