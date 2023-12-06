rem Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Please install Python 3
	echo you can find it here: https://www.python.org/downloads/
	timeout /t 5 /nobreak >nul
    exit /b 1
)

rem Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip is not installed. Installing pip first.
	curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
    if %errorlevel% neq 0 (
        echo Failed to install pip
    )
) else (
	python -m pip install --upgrade pip
)

rem Check if discord.py is installed
pip show discord.py >nul 2>&1
if %errorlevel% neq 0 (
    echo installing discord.py.
	pip install discord.py
	pause
)

if %errorlevel% neq 0 (
    echo Failed to install discord.py, My Lord.
    exit /b 1
)