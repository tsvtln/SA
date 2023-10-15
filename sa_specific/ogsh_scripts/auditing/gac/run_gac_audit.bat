@echo off
REM
REM run_gac_audit.bat
REM
REM A wrapper script for calling gac_audit.py with the proper python path
REM and python binary.
REM
setlocal
set PATH=%SystemDrive%\Program Files\Loudcloud\lcpython15;%PATH%
set PYTHONPATH=%SystemDrive%\Program Files\Loudcloud\blackshadow
set SRC=%SystemDrive%\temp
python "%SRC%\gac_audit.py" %*
