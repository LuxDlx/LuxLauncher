::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFCpjaTa2BleeCaIS5Of66/m7jlgFeOMqdozT36ayLOEG5EbscIQR33lVloUFDxQ4
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSjk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFCpjaTa2BleeCaIS5Of66/m7jlgFeOMqdozT36ayIvUa5kHYWYM1+ntPlsgECQkWewquDg==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal enabledelayedexpansion
cls
:: Enable ANSI escape codes
for /f %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"

:: ASCII Art Lines
set "line1=  ______          ________ _____ _______ ______"
set "line2= / __ \ \        / /  ____|  __ \__   __|___  /"
set "line3=| |  | \ \  /\  / /| |__  | |__) | | |     / / "
set "line4=| |  | |\ \/  \/ / |  __| |  _  /  | |    / /  "
set "line5=| |__| | \  /\  /  | |____| | \ \  | |   / /__ "
set "line6= \___\_\  \/  \/   |______|_|  \_\ |_|  /_____|"

:: Print colored ASCII art
for /l %%i in (1,1,6) do (
    call :printColoredLine "!line%%i!"
)

echo %ESC%[92mLuxlauncher by QWERTZ!%ESC%[0m
timeout /t 3 /nobreak >nul
echo %ESC%[93mLaunching JVM with new java...%ESC%[0m
".\.qwertz\java\bin\java.exe" -jar LuxCore.jar
echo %ESC%[91mGoodbye!%ESC%[0m
timeout /t 3 /nobreak >nul

goto :eof

:printColoredLine
set "line=%~1"
set "coloredLine="
for /L %%j in (0,1,100) do (
    if "!line:~%%j,1!"=="" goto :endLine
    set /a "color=31+%%j%%6"
    set "coloredLine=!coloredLine!%ESC%[!color!m!line:~%%j,1!%ESC%[0m"
)
:endLine
echo(!coloredLine!
goto :eof