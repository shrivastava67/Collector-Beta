@echo off
echo Installing Your Software on Windows...

REM Step 1: Install Python (if not already installed)
if not exist "%ProgramFiles%\Python\Python39" (
    echo Installing Python...
    start /wait python-3.9.7-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
)

REM Step 2: Install pip (if not already installed)
if not exist "%ProgramFiles%\Python\Python39\Scripts\pip.exe" (
    echo Installing pip...
    start /wait python-3.9.7-amd64.exe -m ensurepip --default-pip
)

REM Step 3: Install required packages
echo Installing required Python packages...
pip install -r requirements.txt

REM Step 4: Create desktop shortcut
echo Creating desktop shortcut...
copy your_shortcut.lnk %userprofile%\Desktop\

echo Installation complete!
