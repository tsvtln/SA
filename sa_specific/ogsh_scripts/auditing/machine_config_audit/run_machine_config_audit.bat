@echo off
REM
REM run_machine_config_audit.bat
REM
REM A wrapper script for calling machine_config_audit.py 
REM with the proper path and python binary.
REM
setlocal
set PATH=%SystemDrive%\Program Files\Loudcloud\lcpython15;%PATH%
set PYTHONPATH=%SystemDrive%\Program Files\Loudcloud\blackshadow
set SRC=%SystemDrive%\temp
python "%SRC%\machine_config_audit.py" %*
