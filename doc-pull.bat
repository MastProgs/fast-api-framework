REM @echo off

git submodule update --remote --merge

xcopy ".\DerbyTornado-Doc\data\*" ".\DerbyWebServer\xlsx\" /e /h /k 

pause