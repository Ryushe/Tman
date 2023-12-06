python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Please install Python 3
	echo you can find it here: https://www.python.org/downloads/
	timeout /t 5 /nobreak >nul
    exit /b 1
)

pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip is not installed Installing pip first
	curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
    if %errorlevel% neq 0 (
        echo Failed to install pip
    )
) else (
	python -m pip install --upgrade pip
)

pip show discord.py >nul 2>&1
if %errorlevel% neq 0 (
    echo installing discord.py
	pip install discord.py
)

if %errorlevel% neq 0 (
    echo Failed to install discord.py, My Lord.
    exit /b 1
)

pip show python-dotenv >nul 2>&1
if %errorlevel% neq 0 (
    echo installing dotenv
	pip install python-dotenv
	
)

pip show requests >nul 2>&1
if %errorlevel% neq 0 (
    echo installing requests
	pip install requests
	
)

pip show requests >nul 2>&1
if %errorlevel% neq 0 (
    echo installing requests
	pip install requests
	
)
pip show beautifulsoup4 >nul 2>&1
if %errorlevel% neq 0 (
    echo installing bs4
	pip install beautifulsoup4
	
)


 exit /b 0
