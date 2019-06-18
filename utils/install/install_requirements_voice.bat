@echo off
color 3
pushd %~dp0
echo ===============================
echo Devolution Voice - Requirements
echo ===============================
echo.
echo Ensure you have python3.7 and pip installed before running this script!
echo.
echo [Devolution] Press any key to start the installation!
PAUSE>nul

::Attempts to start py launcher without relying on PATH
%SYSTEMROOT%\py.exe --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO attempt
%SYSTEMROOT%\py.exe -3 -m pip install -U pip
%SYSTEMROOT%\py.exe -3 -m pip install -U discord.py
%SYSTEMROOT%\py.exe -3 -m pip install -U youtube_dl
echo.
echo [Devolution] Installation Complete - Press any key to finish!
PAUSE >nul
GOTO end

::Attempts to start py launcher by relying on PATH
:attempt
py.exe --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO lastattempt
py.exe -3 -m pip install -U discord.py
PAUSE
GOTO end

::As a last resort, attempts to start whatever Python there is
:lastattempt
python.exe --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO message
python.exe -m pip install -U discord.py
PAUSE
GOTO end

:message
echo Couldn't find a valid Python ^>3.5 installation. Python needs to be installed and available in the PATH environment
echo variable.
echo https://github.com/No1IrishStig/DevolutionBeta
PAUSE

:end
