
@echo off
rem Set up the environment.
setlocal

rem Extract the VBS script.
rem set rand=%random%
echo rem File tmp-SpecificProcCpu.vbs > tmp-SpecificProcCpu.vbs
echo     CONST CONST_ERROR                   ^= 0 >> tmp-SpecificProcCpu.vbs
echo     CONST CONST_WSCRIPT                 ^= 1 >> tmp-SpecificProcCpu.vbs
echo     CONST CONST_CSCRIPT                 ^= 2 >> tmp-SpecificProcCpu.vbs
echo     CONST CONST_SHOW_USAGE              ^= 3 >> tmp-SpecificProcCpu.vbs
echo     CONST CONST_PROCEED                 ^= 4 >> tmp-SpecificProcCpu.vbs
echo     CONST cpuHeader ^= "Host|Process Name|PID|CPU">> tmp-SpecificProcCpu.vbs
echo     Dim intOpMode >> tmp-SpecificProcCpu.vbs
echo     Dim strOutputFile, strProcessName >> tmp-SpecificProcCpu.vbs
echo     VerifyHostIsCscript^() >> tmp-SpecificProcCpu.vbs
echo     intOpMode ^= intParseCmdLine^(strOutputFile,  _ >> tmp-SpecificProcCpu.vbs
echo                 strProcessName) >> tmp-SpecificProcCpu.vbs
echo     If strProcessName ^= ^"^" Then       >> tmp-SpecificProcCpu.vbs
echo         strProcessName ^= ^"System Idle Process^" >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo Select Case intOpMode >> tmp-SpecificProcCpu.vbs
echo   Case CONST_SHOW_USAGE >> tmp-SpecificProcCpu.vbs
echo     Call ShowUsage^() >> tmp-SpecificProcCpu.vbs
echo   Case CONST_PROCEED >> tmp-SpecificProcCpu.vbs
echo     Call DisplayProcessInfo^( strProcessName ) >> tmp-SpecificProcCpu.vbs
echo   Case CONST_ERROR >> tmp-SpecificProcCpu.vbs
echo   Case Else                     >> tmp-SpecificProcCpu.vbs
echo     Print ^"Error occurred in passing parameters^.^" >> tmp-SpecificProcCpu.vbs
echo End Select >> tmp-SpecificProcCpu.vbs
echo Wscript^.Quit^(0) >> tmp-SpecificProcCpu.vbs
echo Private Sub DisplayProcessInfo^( strProcessName ) >> tmp-SpecificProcCpu.vbs
echo     Dim objWMIService, colSettings, objComputer >> tmp-SpecificProcCpu.vbs
echo     Dim iNumberOfProcessors, iCpuUsagePercentage >> tmp-SpecificProcCpu.vbs
echo     Dim Process >> tmp-SpecificProcCpu.vbs
echo     Dim objOutputFile >> tmp-SpecificProcCpu.vbs
echo     Dim strOutputLine >> tmp-SpecificProcCpu.vbs
echo     Set objWMIService ^= GetObject^(^"winmgmts:^" _ >> tmp-SpecificProcCpu.vbs
echo             ^& ^"^{impersonationLevel^=impersonate^}!^\^\^.^\root^\cimv2^") >> tmp-SpecificProcCpu.vbs
echo     Set colSettings ^= objWMIService^.ExecQuery _ >> tmp-SpecificProcCpu.vbs
echo                             ^(^"Select * from Win32_ComputerSystem^") >> tmp-SpecificProcCpu.vbs
echo     For Each objComputer in colSettings  >> tmp-SpecificProcCpu.vbs
echo         iNumberOfProcessors ^= objComputer^.NumberOfProcessors >> tmp-SpecificProcCpu.vbs
echo         strComputerName ^= objComputer^.Name >> tmp-SpecificProcCpu.vbs
echo     Next >> tmp-SpecificProcCpu.vbs
echo     If Not IsEmpty^(strOutputFile) Then >> tmp-SpecificProcCpu.vbs
echo         If ^(NOT fsOpenFile^(strOutputFile, objOutputFile)) Then >> tmp-SpecificProcCpu.vbs
echo             Call Wscript^.Echo ^(^"Could not open an output file^.^") >> tmp-SpecificProcCpu.vbs
echo             Exit Sub >> tmp-SpecificProcCpu.vbs
echo         End If >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo    wscript^.echo cpuHeader ^& vbNewLine >> tmp-SpecificProcCpu.vbs
echo     For each Process in GetObject^(^"winmgmts:^")^.ExecQuery^(_ >> tmp-SpecificProcCpu.vbs
echo                     ^"Select * from Win32_Process where Name ^= '^" ^+ _ >> tmp-SpecificProcCpu.vbs
echo                     strProcessName ^+ ^"'^") >> tmp-SpecificProcCpu.vbs
echo     iCpuUsagePercentage ^= CInt^(CPUUSage^(Process^.Handle)) >> tmp-SpecificProcCpu.vbs
echo     If iCpuUsagePercentage ^> 0 Then  >> tmp-SpecificProcCpu.vbs
echo         iCpuUsagePercentage ^= iCpuUsagePercentage ^/ iNumberOfProcessors >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo     strOutputLine ^= strComputerName ^& _ >> tmp-SpecificProcCpu.vbs
echo             ^"^|^" ^& Process^.name ^& _ >> tmp-SpecificProcCpu.vbs
echo             ^"^|^" ^& Process^.ProcessID ^& _ >> tmp-SpecificProcCpu.vbs
echo             ^"^|^" ^& iCpuUsagePercentage ^& _ >> tmp-SpecificProcCpu.vbs
echo             ^"^|^"  >> tmp-SpecificProcCpu.vbs
echo         Call WriteLine^(strOutputLine, objOutputFile) >> tmp-SpecificProcCpu.vbs
echo     Next >> tmp-SpecificProcCpu.vbs
echo     If IsObject^(objOutputFile) Then >> tmp-SpecificProcCpu.vbs
echo         objOutputFile^.Close >> tmp-SpecificProcCpu.vbs
echo         Call Wscript^.Echo ^(^"Results are saved in file ^" ^& strOutputFile ^& ^"^.^") >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo     Set objWMIService ^= Nothing >> tmp-SpecificProcCpu.vbs
echo     Set colSettings ^= Nothing >> tmp-SpecificProcCpu.vbs
echo End Sub >> tmp-SpecificProcCpu.vbs
echo Function CPUUSage^( ProcID ) >> tmp-SpecificProcCpu.vbs
echo 	On Error Resume Next >> tmp-SpecificProcCpu.vbs
echo 	Set objService ^= GetObject^(^"Winmgmts:^{impersonationlevel^=impersonate^}!^\Root^\Cimv2^") >> tmp-SpecificProcCpu.vbs
echo 	For Each objInstance1 in objService^.ExecQuery^(^"Select * from Win32_PerfRawData_PerfProc_Process where IDProcess ^= '^" ^& ProcID ^& ^"'^") >> tmp-SpecificProcCpu.vbs
echo 		N1 ^= objInstance1^.PercentProcessorTime >> tmp-SpecificProcCpu.vbs
echo 		D1 ^= objInstance1^.TimeStamp_Sys100NS >> tmp-SpecificProcCpu.vbs
echo 		Exit For >> tmp-SpecificProcCpu.vbs
echo 	Next >> tmp-SpecificProcCpu.vbs
echo 	WScript^.Sleep^(1500) >> tmp-SpecificProcCpu.vbs
echo 	For Each perf_instance2 in objService^.ExecQuery^(^"Select * from Win32_PerfRawData_PerfProc_Process where IDProcess ^= '^" ^& ProcID ^& ^"'^") >> tmp-SpecificProcCpu.vbs
echo 		N2 ^= perf_instance2^.PercentProcessorTime >> tmp-SpecificProcCpu.vbs
echo 		D2 ^= perf_instance2^.TimeStamp_Sys100NS >> tmp-SpecificProcCpu.vbs
echo 		Exit For >> tmp-SpecificProcCpu.vbs
echo 	Next >> tmp-SpecificProcCpu.vbs
echo 	Nd ^= ^(N2 - N1) >> tmp-SpecificProcCpu.vbs
echo 	Dd ^= ^(D2-D1) >> tmp-SpecificProcCpu.vbs
echo 	PercentProcessorTime ^= ^( ^(Nd^/Dd))  * 100 >> tmp-SpecificProcCpu.vbs
echo 	CPUUSage ^= Round^(PercentProcessorTime ,0) >> tmp-SpecificProcCpu.vbs
echo End Function >> tmp-SpecificProcCpu.vbs
echo Sub WriteLine^(ByVal strMessage, ByVal objFile) >> tmp-SpecificProcCpu.vbs
echo     On Error Resume Next >> tmp-SpecificProcCpu.vbs
echo     If IsObject^(objFile) then        >> tmp-SpecificProcCpu.vbs
echo         objFile^.WriteLine strMessage >> tmp-SpecificProcCpu.vbs
echo     Else >> tmp-SpecificProcCpu.vbs
echo         Call Wscript^.Echo^( strMessage ) >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo End Sub >> tmp-SpecificProcCpu.vbs
echo Private Function intParseCmdLine^( ByRef strOutputFile, _ >> tmp-SpecificProcCpu.vbs
echo                                   ByRef strProcessName ) >> tmp-SpecificProcCpu.vbs
echo     ON ERROR GOTO 0 >> tmp-SpecificProcCpu.vbs
echo     Dim strFlag >> tmp-SpecificProcCpu.vbs
echo     Dim intState, intArgIter, intWidth >> tmp-SpecificProcCpu.vbs
echo     Dim objFileSystem >> tmp-SpecificProcCpu.vbs
echo     If Wscript^.Arguments^.Count ^> 0 Then >> tmp-SpecificProcCpu.vbs
echo         strFlag ^= Wscript^.arguments^.Item^(0) >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo     If IsEmpty^(strFlag) Then    >> tmp-SpecificProcCpu.vbs
echo         intParseCmdLine ^= CONST_PROCEED >> tmp-SpecificProcCpu.vbs
echo         Exit Function >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo     If ^(strFlag^=^"help^") OR ^(strFlag^=^"^/h^") OR ^(strFlag^=^"^\h^") OR ^(strFlag^=^"-h^") _ >> tmp-SpecificProcCpu.vbs
echo         OR ^(strFlag ^= ^"^\?^") OR ^(strFlag ^= ^"^/?^") OR ^(strFlag ^= ^"?^") _  >> tmp-SpecificProcCpu.vbs
echo         OR ^(strFlag^=^"-?^") OR ^(strFlag^=^"h^") Then >> tmp-SpecificProcCpu.vbs
echo         intParseCmdLine ^= CONST_SHOW_USAGE >> tmp-SpecificProcCpu.vbs
echo         Exit Function >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo      intArgIter ^= 0 >> tmp-SpecificProcCpu.vbs
echo     Do While intArgIter ^<^= Wscript^.arguments^.Count - 1 >> tmp-SpecificProcCpu.vbs
echo         Select Case Left^(LCase^(Wscript^.arguments^.Item^(intArgIter)),2) >> tmp-SpecificProcCpu.vbs
echo             Case ^"^/o^" >> tmp-SpecificProcCpu.vbs
echo                 If Not cmdlineGetArg^(^"Output File^", strOutputFile, intArgIter) Then >> tmp-SpecificProcCpu.vbs
echo                     intParseCmdLine ^= CONST_ERROR >> tmp-SpecificProcCpu.vbs
echo                     Exit Function >> tmp-SpecificProcCpu.vbs
echo                 End If >> tmp-SpecificProcCpu.vbs
echo                 intArgIter ^= intArgIter ^+ 1 >> tmp-SpecificProcCpu.vbs
echo             Case ^"-o^" >> tmp-SpecificProcCpu.vbs
echo                 If Not cmdlineGetArg^(^"Output File^", strOutputFile, intArgIter) Then >> tmp-SpecificProcCpu.vbs
echo                     intParseCmdLine ^= CONST_ERROR >> tmp-SpecificProcCpu.vbs
echo                     Exit Function >> tmp-SpecificProcCpu.vbs
echo                 End If >> tmp-SpecificProcCpu.vbs
echo                 intArgIter ^= intArgIter ^+ 1 >> tmp-SpecificProcCpu.vbs
echo             Case ^"^/n^" >> tmp-SpecificProcCpu.vbs
echo                 If Not cmdlineGetArg^(^"Process Name^", strProcessName, intArgIter) Then >> tmp-SpecificProcCpu.vbs
echo                     intParseCmdLine ^= CONST_ERROR >> tmp-SpecificProcCpu.vbs
echo                     Exit Function >> tmp-SpecificProcCpu.vbs
echo                 End If >> tmp-SpecificProcCpu.vbs
echo                 intArgIter ^= intArgIter ^+ 1 >> tmp-SpecificProcCpu.vbs
echo             Case ^"-n^" >> tmp-SpecificProcCpu.vbs
echo                 If Not cmdlineGetArg^(^"Process Name^", strProcessName, intArgIter) Then >> tmp-SpecificProcCpu.vbs
echo                     intParseCmdLine ^= CONST_ERROR >> tmp-SpecificProcCpu.vbs
echo                     Exit Function >> tmp-SpecificProcCpu.vbs
echo                 End If >> tmp-SpecificProcCpu.vbs
echo                 intArgIter ^= intArgIter ^+ 1 >> tmp-SpecificProcCpu.vbs
echo             Case Else >> tmp-SpecificProcCpu.vbs
echo                 Call Wscript^.Echo^(^"Invalid or misplaced parameter: ^" _ >> tmp-SpecificProcCpu.vbs
echo                    ^& Wscript^.arguments^.Item^(intArgIter) ^& vbCRLF _ >> tmp-SpecificProcCpu.vbs
echo                    ^& ^"Please check the input and try again,^" ^& vbCRLF _ >> tmp-SpecificProcCpu.vbs
echo                    ^& ^"or invoke with '^/?' for help with the syntax^.^") >> tmp-SpecificProcCpu.vbs
echo                 Wscript^.Quit >> tmp-SpecificProcCpu.vbs
echo         End Select >> tmp-SpecificProcCpu.vbs
echo     Loop '** intArgIter ^<^= Wscript^.arguments^.Count - 1 >> tmp-SpecificProcCpu.vbs
echo     If IsEmpty^(intParseCmdLine) Then _ >> tmp-SpecificProcCpu.vbs
echo         intParseCmdLine ^= CONST_PROCEED >> tmp-SpecificProcCpu.vbs
echo End Function >> tmp-SpecificProcCpu.vbs
echo Private Function cmdlineGetArg ^( ByVal StrVarName,   _ >> tmp-SpecificProcCpu.vbs
echo                              ByRef strVar,       _ >> tmp-SpecificProcCpu.vbs
echo                              ByRef intArgIter)  >> tmp-SpecificProcCpu.vbs
echo     cmdlineGetArg ^= False 'failure, changed to True upon successful completion >> tmp-SpecificProcCpu.vbs
echo     If Len^(Wscript^.Arguments^(intArgIter)) ^> 2 then >> tmp-SpecificProcCpu.vbs
echo         If Mid^(Wscript^.Arguments^(intArgIter),3,1) ^= ^":^" then >> tmp-SpecificProcCpu.vbs
echo             If Len^(Wscript^.Arguments^(intArgIter)) ^> 3 then >> tmp-SpecificProcCpu.vbs
echo                 strVar ^= Right^(Wscript^.Arguments^(intArgIter), _ >> tmp-SpecificProcCpu.vbs
echo                          Len^(Wscript^.Arguments^(intArgIter)) - 3) >> tmp-SpecificProcCpu.vbs
echo                 cmdlineGetArg ^= True >> tmp-SpecificProcCpu.vbs
echo                 Exit Function >> tmp-SpecificProcCpu.vbs
echo             Else >> tmp-SpecificProcCpu.vbs
echo                 intArgIter ^= intArgIter ^+ 1 >> tmp-SpecificProcCpu.vbs
echo                 If intArgIter ^> ^(Wscript^.Arguments^.Count - 1) Then >> tmp-SpecificProcCpu.vbs
echo                     Call Wscript^.Echo^( ^"Invalid ^" ^& StrVarName ^& ^"^.^") >> tmp-SpecificProcCpu.vbs
echo                     Call Wscript^.Echo^( ^"Please check the input and try again^.^") >> tmp-SpecificProcCpu.vbs
echo                     Exit Function >> tmp-SpecificProcCpu.vbs
echo                 End If >> tmp-SpecificProcCpu.vbs
echo                 strVar ^= Wscript^.Arguments^.Item^(intArgIter) >> tmp-SpecificProcCpu.vbs
echo                 If Err^.Number Then >> tmp-SpecificProcCpu.vbs
echo                     Call Wscript^.Echo^( ^"Invalid ^" ^& StrVarName ^& ^"^.^") >> tmp-SpecificProcCpu.vbs
echo                     Call Wscript^.Echo^( ^"Please check the input and try again^.^") >> tmp-SpecificProcCpu.vbs
echo                     Exit Function >> tmp-SpecificProcCpu.vbs
echo                 End If >> tmp-SpecificProcCpu.vbs
echo                 If InStr^(strVar, ^"^/^") Then >> tmp-SpecificProcCpu.vbs
echo                     Call Wscript^.Echo^( ^"Invalid ^" ^& StrVarName) >> tmp-SpecificProcCpu.vbs
echo                     Call Wscript^.Echo^( ^"Please check the input and try again^.^") >> tmp-SpecificProcCpu.vbs
echo                     Exit Function >> tmp-SpecificProcCpu.vbs
echo                 End If >> tmp-SpecificProcCpu.vbs
echo                 cmdlineGetArg ^= True >> tmp-SpecificProcCpu.vbs
echo             End If >> tmp-SpecificProcCpu.vbs
echo         Else >> tmp-SpecificProcCpu.vbs
echo             strVar ^= Right^(Wscript^.Arguments^(intArgIter), _ >> tmp-SpecificProcCpu.vbs
echo                      Len^(Wscript^.Arguments^(intArgIter)) - 2) >> tmp-SpecificProcCpu.vbs
echo             cmdlineGetArg ^= True  >> tmp-SpecificProcCpu.vbs
echo             Exit Function >> tmp-SpecificProcCpu.vbs
echo         End If >> tmp-SpecificProcCpu.vbs
echo     Else >> tmp-SpecificProcCpu.vbs
echo         intArgIter ^= intArgIter ^+ 1 >> tmp-SpecificProcCpu.vbs
echo         If intArgIter ^> ^(Wscript^.Arguments^.Count - 1) Then >> tmp-SpecificProcCpu.vbs
echo             Call Wscript^.Echo^( ^"Invalid ^" ^& StrVarName ^& ^"^.^") >> tmp-SpecificProcCpu.vbs
echo             Call Wscript^.Echo^( ^"Please check the input and try again^.^") >> tmp-SpecificProcCpu.vbs
echo             Exit Function >> tmp-SpecificProcCpu.vbs
echo         End If >> tmp-SpecificProcCpu.vbs
echo         strVar ^= Wscript^.Arguments^.Item^(intArgIter) >> tmp-SpecificProcCpu.vbs
echo         If Err^.Number Then >> tmp-SpecificProcCpu.vbs
echo             Call Wscript^.Echo^( ^"Invalid ^" ^& StrVarName ^& ^"^.^") >> tmp-SpecificProcCpu.vbs
echo             Call Wscript^.Echo^( ^"Please check the input and try again^.^") >> tmp-SpecificProcCpu.vbs
echo             Exit Function >> tmp-SpecificProcCpu.vbs
echo         End If >> tmp-SpecificProcCpu.vbs
echo         If InStr^(strVar, ^"^/^") Then >> tmp-SpecificProcCpu.vbs
echo             Call Wscript^.Echo^( ^"Invalid ^" ^& StrVarName) >> tmp-SpecificProcCpu.vbs
echo             Call Wscript^.Echo^( ^"Please check the input and try again^.^") >> tmp-SpecificProcCpu.vbs
echo             Exit Function >> tmp-SpecificProcCpu.vbs
echo         End If >> tmp-SpecificProcCpu.vbs
echo         cmdlineGetArg ^= True  >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo End Function >> tmp-SpecificProcCpu.vbs
echo Private Function fsOpenFile^(ByVal strFileName, ByRef objOpenFile) >> tmp-SpecificProcCpu.vbs
echo     ON ERROR RESUME NEXT >> tmp-SpecificProcCpu.vbs
echo     Dim objFileSystem >> tmp-SpecificProcCpu.vbs
echo 	Dim strFilePath >> tmp-SpecificProcCpu.vbs
echo     Set objFileSystem ^= Nothing >> tmp-SpecificProcCpu.vbs
echo     If IsEmpty^(strFileName) OR strFileName ^= ^"^" Then >> tmp-SpecificProcCpu.vbs
echo         fsOpenFile ^= False >> tmp-SpecificProcCpu.vbs
echo         Set objOpenFile ^= Nothing >> tmp-SpecificProcCpu.vbs
echo         Exit Function >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo     Call fsBuildPath ^( strFileName ) >> tmp-SpecificProcCpu.vbs
echo     Set objFileSystem ^= CreateObject^(^"Scripting^.FileSystemObject^") >> tmp-SpecificProcCpu.vbs
echo     If fsErrorOccurred^(^"Could not create filesystem object^.^") Then >> tmp-SpecificProcCpu.vbs
echo         fsOpenFile ^= False >> tmp-SpecificProcCpu.vbs
echo         Set objOpenFile ^= Nothing >> tmp-SpecificProcCpu.vbs
echo         Exit Function >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo     Set objOpenFile ^= objFileSystem^.OpenTextFile^(strFileName, 2, True) >> tmp-SpecificProcCpu.vbs
echo     If fsErrorOccurred^(^"Could not open^") Then >> tmp-SpecificProcCpu.vbs
echo         fsOpenFile ^= False >> tmp-SpecificProcCpu.vbs
echo         Set objOpenFile ^= Nothing >> tmp-SpecificProcCpu.vbs
echo         Exit Function >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo     fsOpenFile ^= True >> tmp-SpecificProcCpu.vbs
echo End Function >> tmp-SpecificProcCpu.vbs
echo Sub fsBuildPath^(ByVal strFileName) >> tmp-SpecificProcCpu.vbs
echo     Dim fsoPathToBuild >> tmp-SpecificProcCpu.vbs
echo     Set fsoPathToBuild ^= CreateObject^(^"Scripting^.FileSystemObject^") >> tmp-SpecificProcCpu.vbs
echo     If InStrRev^(strFileName, ^"^\^") ^> 2 Then >> tmp-SpecificProcCpu.vbs
echo         strDirPath ^= Left^(strFileName, ^(InStrRev^(strFileName, ^"^\^") - 1)) >> tmp-SpecificProcCpu.vbs
echo     Else >> tmp-SpecificProcCpu.vbs
echo         exit sub     >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo     If fsoPathToBuild^.FolderExists^(strDirPath) Then exit sub >> tmp-SpecificProcCpu.vbs
echo     fsBuildPath^(fsoPathToBuild^.GetParentFolderName^(strDirPath)) >> tmp-SpecificProcCpu.vbs
echo     fsoPathToBuild^.CreateFolder^(strDirPath) >> tmp-SpecificProcCpu.vbs
echo     Set fsoPathToBuild ^= Nothing >> tmp-SpecificProcCpu.vbs
echo End Sub >> tmp-SpecificProcCpu.vbs
echo Private Function fsErrorOccurred ^(ByVal strIn) >> tmp-SpecificProcCpu.vbs
echo     If Err^.Number Then >> tmp-SpecificProcCpu.vbs
echo         Call Wscript^.Echo^( ^"Error 0x^" ^& CStr^(Hex^(Err^.Number)) ^& ^": ^" ^& strIn) >> tmp-SpecificProcCpu.vbs
echo         If Err^.Description ^<^> ^"^" Then >> tmp-SpecificProcCpu.vbs
echo             Call Wscript^.Echo^( ^"Error description: ^" ^& Err^.Description) >> tmp-SpecificProcCpu.vbs
echo         End If >> tmp-SpecificProcCpu.vbs
echo         Err^.Clear >> tmp-SpecificProcCpu.vbs
echo         fsErrorOccurred ^= True >> tmp-SpecificProcCpu.vbs
echo     Else >> tmp-SpecificProcCpu.vbs
echo         fsErrorOccurred ^= False >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo End Function >> tmp-SpecificProcCpu.vbs
echo Sub VerifyHostIsCscript^() >> tmp-SpecificProcCpu.vbs
echo     ON ERROR RESUME NEXT >> tmp-SpecificProcCpu.vbs
echo     Dim strFullName, strCommand, i, j, intStatus >> tmp-SpecificProcCpu.vbs
echo     strFullName ^= WScript^.FullName >> tmp-SpecificProcCpu.vbs
echo     If Err^.Number then >> tmp-SpecificProcCpu.vbs
echo         Call Wscript^.Echo^( ^"Error 0x^" ^& CStr^(Hex^(Err^.Number)) ^& ^" occurred^.^" ) >> tmp-SpecificProcCpu.vbs
echo         If Err^.Description ^<^> ^"^" Then >> tmp-SpecificProcCpu.vbs
echo             Call Wscript^.Echo^( ^"Error description: ^" ^& Err^.Description ^& ^"^.^" ) >> tmp-SpecificProcCpu.vbs
echo         End If >> tmp-SpecificProcCpu.vbs
echo         intStatus ^=  CONST_ERROR >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo     i ^= InStr^(1, strFullName, ^"^.exe^", 1) >> tmp-SpecificProcCpu.vbs
echo     If i ^= 0 Then >> tmp-SpecificProcCpu.vbs
echo         intStatus ^=  CONST_ERROR >> tmp-SpecificProcCpu.vbs
echo     Else >> tmp-SpecificProcCpu.vbs
echo         j ^= InStrRev^(strFullName, ^"^\^", i, 1) >> tmp-SpecificProcCpu.vbs
echo         If j ^= 0 Then >> tmp-SpecificProcCpu.vbs
echo             intStatus ^=  CONST_ERROR >> tmp-SpecificProcCpu.vbs
echo         Else >> tmp-SpecificProcCpu.vbs
echo             strCommand ^= Mid^(strFullName, j^+1, i-j-1) >> tmp-SpecificProcCpu.vbs
echo             Select Case LCase^(strCommand) >> tmp-SpecificProcCpu.vbs
echo                 Case ^"cscript^" >> tmp-SpecificProcCpu.vbs
echo                     intStatus ^= CONST_CSCRIPT >> tmp-SpecificProcCpu.vbs
echo                 Case ^"wscript^" >> tmp-SpecificProcCpu.vbs
echo                     intStatus ^= CONST_WSCRIPT >> tmp-SpecificProcCpu.vbs
echo                 Case Else     >> tmp-SpecificProcCpu.vbs
echo                     Call Wscript^.Echo^( ^"An unexpected program was used to ^" _ >> tmp-SpecificProcCpu.vbs
echo                                        ^& ^"run this script^.^" ) >> tmp-SpecificProcCpu.vbs
echo                     Call Wscript^.Echo^( ^"Only CScript^.Exe or WScript^.Exe can ^" _ >> tmp-SpecificProcCpu.vbs
echo                                        ^& ^"be used to run this script^.^" ) >> tmp-SpecificProcCpu.vbs
echo                     intStatus ^= CONST_ERROR >> tmp-SpecificProcCpu.vbs
echo                 End Select >> tmp-SpecificProcCpu.vbs
echo         End If >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo     If intStatus ^<^> CONST_CSCRIPT Then >> tmp-SpecificProcCpu.vbs
echo         Call WScript^.Echo^( ^"Please run this script using CScript^.^" ^& vbCRLF ^& _ >> tmp-SpecificProcCpu.vbs
echo              ^"This can be achieved by^" ^& vbCRLF ^& _ >> tmp-SpecificProcCpu.vbs
echo              ^"1^. Using ^"^"CScript ^" ^& Wscript^.ScriptName ^& ^" arguments^"^" for Windows 95^/98 or^" _ >> tmp-SpecificProcCpu.vbs
echo              ^& vbCRLF ^& ^"2^. Changing the default Windows Scripting Host ^" _ >> tmp-SpecificProcCpu.vbs
echo              ^& ^"setting to CScript^" ^& vbCRLF ^& ^"    using ^"^"CScript ^" _ >> tmp-SpecificProcCpu.vbs
echo              ^& ^"^/^/H:CScript ^/^/S^"^" and running the script using^" ^& vbCRLF ^& _ >> tmp-SpecificProcCpu.vbs
echo              ^"    ^"^"^" ^& Wscript^.ScriptName ^& ^" arguments^"^" for Windows NT^/2000^.^" ) >> tmp-SpecificProcCpu.vbs
echo         WScript^.Quit >> tmp-SpecificProcCpu.vbs
echo     End If >> tmp-SpecificProcCpu.vbs
echo End Sub >> tmp-SpecificProcCpu.vbs
echo Private Sub ShowUsage^() >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"Display all instances of a specific process with the^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"CPU usage as a percentage of total CPU^.^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"SYNTAX:^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"  Display_Specific_Process_CPU_Usage_in_Percent^.vbs ^[^/O ^<outputfile^>^]^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"                                                    ^[^/N ^<process name^>^]^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"PARAMETER SPECIFIERS:^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"   outputfile    The output file name^. Path can be an existing UNC^.^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"   Process name  The name of the process, e^.g^., taskmgr^.exe^.^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"   Valid option variations: ^/O, ^/o, -O, -o, ^/N, ^/n^. -N, -n^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"DEFAULT VALUES:^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"   Output goes to display^.^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"   If no process name is supplied, reports on 'System Idle Process'^.^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"OUTPUT FORMAT:^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"  system_name^|process_name^|PID^|CPU_usage_percentage^|^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"EXAMPLE:^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"1^. cscript List_Specific_Process_CPU_Usage_in_Percent^.vbs^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"   Lists CPU usage for the 'System Idle Process'^.^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"2^. cscript List_Specific_Process_CPU_Usage_in_Percent^.vbs ^/N taskmgr^.exe^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"   Lists any 'taskmgr^.exe' jobs running with their CPU usage^.^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"3^. cscript List_Specific_Process_CPU_Usage_in_Percent^.vbs ^/O file^.txt^" >> tmp-SpecificProcCpu.vbs
echo     Wscript^.Echo ^"   Lists CPU usage for 'Idle' process and writes the output to 'file^.txt'^.^" >> tmp-SpecificProcCpu.vbs
echo End Sub >> tmp-SpecificProcCpu.vbs


rem Execute the script.
cscript.exe  //nologo tmp-SpecificProcCpu.vbs /N %1
del /f tmp-SpecificProcCpu.vbs
