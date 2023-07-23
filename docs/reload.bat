call make clean html
call make html

if exist "%~dp0html\" RMDIR /S /Q "%~dp0html"
echo d | xcopy /s "%~dp0_build\html" "%~dp0html"

pause