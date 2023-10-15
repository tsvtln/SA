@echo off
REM win-md5sum.bat
REM
REM A wrapper script for calling md5sum.py with the proper python path
REM and python binary.

dir %WINDIR%\system32\*.exe /B /X > %TEMP%\exefiles
dir %WINDIR%\system32\*.dll /B /X > %TEMP%\dllfiles

setlocal
set PATH=%SystemDrive%\Program Files\Loudcloud\lcpython15;%PATH%
set PYTHONPATH=%SystemDrive%\Program Files\Loudcloud\blackshadow
set SRC=%ProgramFiles%\Loudcloud\bin
python "%SRC%\win-md5sum.py" %TEMP%\exefiles
python "%SRC%\win-md5sum.py" %TEMP%\dllfiles

del %TEMP%\exefiles
del %TEMP%\dllfiles
