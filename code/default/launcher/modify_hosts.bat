@echo off
if not "%1" == "uac" (
goto GetUAC
) else ( goto DO )

:GetUAC
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "%~s0", "uac", "", "runas", 1 >> "%temp%\getadmin.vbs"

"%temp%\getadmin.vbs"
exit /B

:DO
if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
pushd "%CD%"
CD /D "%~dp0"

attrib C:\Windows\system32\drivers\etc\hosts -r
echo.>> C:\Windows\system32\drivers\etc\hosts
echo 104.28.2.6 doub.io>> C:\Windows\system32\drivers\etc\hosts