@echo off
rem Set up the environment.
setlocal

rem Extract the VBS script.
rem set rand=%random%
echo for each Process in GetObject^(^"winmgmts:^")^.ExecQuery^(^"Select * from Win32_Process^") > tmp-ListProcsCpuUsagePercent.vbs

echo 	WScript^.echo Process^.name ^& vbTab ^& Process^.processID ^& vbTab ^& CPUUSage^(Process^.Handle) ^& ^" %%^" >> tmp-ListProcsCpuUsagePercent.vbs

echo Next >> tmp-ListProcsCpuUsagePercent.vbs

echo Function CPUUSage^( ProcID ) >> tmp-ListProcsCpuUsagePercent.vbs

echo 	On Error Resume Next >> tmp-ListProcsCpuUsagePercent.vbs

echo 	Set objService ^= GetObject^(^"Winmgmts:^{impersonationlevel^=impersonate^}!^\Root^\Cimv2^") >> tmp-ListProcsCpuUsagePercent.vbs

echo 	For Each objInstance1 in objService^.ExecQuery^(^"Select * from Win32_PerfRawData_PerfProc_Process where IDProcess ^= '^" ^& ProcID ^& ^"'^") >> tmp-ListProcsCpuUsagePercent.vbs

echo 		N1 ^= objInstance1^.PercentProcessorTime >> tmp-ListProcsCpuUsagePercent.vbs

echo 		D1 ^= objInstance1^.TimeStamp_Sys100NS >> tmp-ListProcsCpuUsagePercent.vbs

echo 		Exit For >> tmp-ListProcsCpuUsagePercent.vbs

echo 	Next >> tmp-ListProcsCpuUsagePercent.vbs

echo 	WScript^.Sleep^(1500) >> tmp-ListProcsCpuUsagePercent.vbs

echo 	For Each perf_instance2 in objService^.ExecQuery^(^"Select * from Win32_PerfRawData_PerfProc_Process where IDProcess ^= '^" ^& ProcID ^& ^"'^") >> tmp-ListProcsCpuUsagePercent.vbs

echo 		N2 ^= perf_instance2^.PercentProcessorTime >> tmp-ListProcsCpuUsagePercent.vbs

echo 		D2 ^= perf_instance2^.TimeStamp_Sys100NS >> tmp-ListProcsCpuUsagePercent.vbs

echo 		Exit For >> tmp-ListProcsCpuUsagePercent.vbs

echo 	Next >> tmp-ListProcsCpuUsagePercent.vbs

echo 	' CounterType - PERF_100NSEC_TIMER_INV >> tmp-ListProcsCpuUsagePercent.vbs

echo 	' Formula - ^(1- ^(^(N2 - N1) ^/ ^(D2 - D1))) x 100 >> tmp-ListProcsCpuUsagePercent.vbs

echo 	Nd ^= ^(N2 - N1) >> tmp-ListProcsCpuUsagePercent.vbs

echo 	Dd ^= ^(D2-D1) >> tmp-ListProcsCpuUsagePercent.vbs

echo 	PercentProcessorTime ^= ^( ^(Nd^/Dd))  * 100 >> tmp-ListProcsCpuUsagePercent.vbs

echo 	CPUUSage ^= Round^(PercentProcessorTime ,0) >> tmp-ListProcsCpuUsagePercent.vbs

echo End Function >> tmp-ListProcsCpuUsagePercent.vbs



rem Execute the script.
cscript.exe //nologo tmp-ListProcsCpuUsagePercent.vbs 
del /f tmp-ListProcsCpuUsagePercent.vbs
