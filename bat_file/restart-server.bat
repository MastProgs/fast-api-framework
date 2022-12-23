

@echo off
setlocal

cd DerbyWebServer

set string=
for /f "delims=" %%i in (process_status.json) do set "string=%%i"

rem Remove quotes
set string=%string:"=%

rem Remove braces
set "string=%string:~1,-1%"

rem Change colon+space by equal-sign
set "string=%string:: ==%"

rem Separate parts at comma into individual assignments
set "%string:, =" & set "%"

taskkill /f /pid %pid%