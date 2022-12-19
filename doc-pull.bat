REM @echo off

git submodule update --remote --merge

xcopy ".\(폴더명)\data\*" ".\(폴더명)\xlsx\" /e /h /k 

pause
