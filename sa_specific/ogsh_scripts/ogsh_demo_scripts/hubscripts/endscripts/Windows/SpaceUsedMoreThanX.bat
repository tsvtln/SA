
@echo off
rem Set up the environment.
setlocal

rem Extract the VBS script.
rem set rand=%random%
echo rem File tmp-ParitionswithLessthanX.vbs > tmp-ParitionswithLessthanX.vbs
echo Option Explicit >> tmp-ParitionswithLessthanX.vbs
echo Dim objWshNetwork >> tmp-ParitionswithLessthanX.vbs
echo Dim strComputerName >> tmp-ParitionswithLessthanX.vbs
echo Dim objArgs >> tmp-ParitionswithLessthanX.vbs
echo Dim DiskSet >> tmp-ParitionswithLessthanX.vbs
echo Dim Disk >> tmp-ParitionswithLessthanX.vbs
echo Dim strDesc >> tmp-ParitionswithLessthanX.vbs
echo Dim DiskThreshold >> tmp-ParitionswithLessthanX.vbs
echo On Error Goto 0 >> tmp-ParitionswithLessthanX.vbs
echo Set objWshNetwork ^= WScript^.CreateObject^(^"WScript^.Network^") >> tmp-ParitionswithLessthanX.vbs
echo strComputerName ^= objWshNetwork^.ComputerName >> tmp-ParitionswithLessthanX.vbs
echo Set objArgs ^= WScript^.Arguments >> tmp-ParitionswithLessthanX.vbs
echo Select Case objArgs^.count >> tmp-ParitionswithLessthanX.vbs
echo     case 0 >> tmp-ParitionswithLessthanX.vbs
echo 	DiskThreshold ^= 0^.10  >> tmp-ParitionswithLessthanX.vbs
echo     case 1 >> tmp-ParitionswithLessthanX.vbs
echo 	If objArgs^(0) ^>^= 0 And objArgs^(0) ^<^= 100 Then >> tmp-ParitionswithLessthanX.vbs
echo 		DiskThreshold ^= objArgs^(0) ^/ 100 >> tmp-ParitionswithLessthanX.vbs
echo 	Else >> tmp-ParitionswithLessthanX.vbs
echo 		Wscript^.Echo vbNewLine ^& ^" Error: Incorrect value as argument!!^" ^& vbNewLine ^& _ >> tmp-ParitionswithLessthanX.vbs
echo 			^" Threshold value must be between 0 and 100, inclusive^.^" ^& vbNewLine ^& vbNewLine >> tmp-ParitionswithLessthanX.vbs
echo 		Wscript^.Quit^(1) >> tmp-ParitionswithLessthanX.vbs
echo 	End If >> tmp-ParitionswithLessthanX.vbs
echo     case else >> tmp-ParitionswithLessthanX.vbs
echo     	Wscript^.Echo ^" Error: Incorrect number of arguments!!^" ^& vbNewLine ^& _ >> tmp-ParitionswithLessthanX.vbs
echo 		^" Threshold value must be between 0 and 100, inclusive^.^" ^& vbNewLine ^& vbNewLine >> tmp-ParitionswithLessthanX.vbs
echo 	WScript^.Quit^(1) >> tmp-ParitionswithLessthanX.vbs
echo End Select >> tmp-ParitionswithLessthanX.vbs
echo Set DiskSet ^= GetObject^(^"winmgmts:^{impersonationLevel^=impersonate^}^")^.ExecQuery^(^"select FreeSpace,Size,Name from Win32_LogicalDisk where DriveType^=3^") >> tmp-ParitionswithLessthanX.vbs
echo Const diskHeader ^= "Host|Drivename|Capacity|Available|PercentAvail" >> tmp-ParitionswithLessThanX.vbs
echo    wscript^.echo diskHeader ^& vbNewLine >> tmp-ParitionswithLessthanX.vbs
echo For each Disk in DiskSet >> tmp-ParitionswithLessthanX.vbs
echo 	If ^(Disk^.FreeSpace^/Disk^.Size) ^< DiskThreshold Then >> tmp-ParitionswithLessthanX.vbs
echo         strDesc ^= strComputerName ^& ^"^|^" ^& Left^(Disk^.Name,Len^(Disk^.Name)-1) >> tmp-ParitionswithLessthanX.vbs
echo         strDesc ^= strDesc ^& ^"^|^" ^& ^(CInt^(100 * ^(Disk^.Size ^/ 1073741824)) ^/ 100) >> tmp-ParitionswithLessthanX.vbs
echo 		strDesc ^= strDesc ^& ^"^|^" ^& _ >> tmp-ParitionswithLessthanX.vbs
echo 			^(CInt^(100 * Disk^.FreeSpace ^/ 1073741824) ^/ 100) ^& ^"^|^" ^& _ >> tmp-ParitionswithLessthanX.vbs
echo 			^(CInt^(100 * ^(Disk^.FreeSpace^/Disk^.Size)))  ^& ^"^|^" >> tmp-ParitionswithLessthanX.vbs
echo 	End If >> tmp-ParitionswithLessthanX.vbs
echo 	Wscript^.Echo strDesc >> tmp-ParitionswithLessthanX.vbs
echo Next >> tmp-ParitionswithLessthanX.vbs
echo Set DiskSet ^= Nothing >> tmp-ParitionswithLessthanX.vbs
echo Wscript^.Quit^(0) >> tmp-ParitionswithLessthanX.vbs


rem Execute the script.
cscript.exe //nologo  tmp-ParitionswithLessthanX.vbs %1
del /f tmp-ParitionswithLessthanX.vbs
