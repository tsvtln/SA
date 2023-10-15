
@echo off
rem Set up the environment.
setlocal

rem Extract the VBS script.
rem set rand=%random%
echo rem File tmp-DispProcess3.vbs > tmp-DispProcess3.vbs

echo On Error Goto 0 >> tmp-DispProcess3.vbs

echo     CONST CONST_ERROR                   ^= 0 >> tmp-DispProcess3.vbs

echo     CONST CONST_WSCRIPT                 ^= 1 >> tmp-DispProcess3.vbs

echo     CONST CONST_CSCRIPT                 ^= 2 >> tmp-DispProcess3.vbs

echo     CONST CONST_SHOW_USAGE              ^= 3 >> tmp-DispProcess3.vbs

echo     CONST CONST_PROCEED                 ^= 4 >> tmp-DispProcess3.vbs

echo     Dim intOpMode >> tmp-DispProcess3.vbs

echo     Dim strOutputFile, strPercentageThreshold, strSampleInterval >> tmp-DispProcess3.vbs

echo     VerifyHostIsCscript^() >> tmp-DispProcess3.vbs

echo     intOpMode ^= intParseCmdLine^(strOutputFile,  _ >> tmp-DispProcess3.vbs

echo                                 strPercentageThreshold, _ >> tmp-DispProcess3.vbs

echo                                 strSampleInterval) >> tmp-DispProcess3.vbs

echo Select Case intOpMode >> tmp-DispProcess3.vbs

echo   Case CONST_SHOW_USAGE >> tmp-DispProcess3.vbs

echo     Call ShowUsage^() >> tmp-DispProcess3.vbs

echo   Case CONST_PROCEED >> tmp-DispProcess3.vbs

echo     Call DisplayHighUsageProcessInfo^() >> tmp-DispProcess3.vbs

echo   Case CONST_ERROR >> tmp-DispProcess3.vbs

echo   Case Else           >> tmp-DispProcess3.vbs

echo     Print ^"Error occurred in passing parameters^.^" >> tmp-DispProcess3.vbs

echo End Select >> tmp-DispProcess3.vbs

echo Wscript^.Quit^(0) >> tmp-DispProcess3.vbs

echo Private Sub DisplayHighUsageProcessInfo^() >> tmp-DispProcess3.vbs

echo     Dim objWMIService, colSettings, objComputer, iNumberOfProcessors >> tmp-DispProcess3.vbs

echo     Dim strComputer, strComputerName >> tmp-DispProcess3.vbs

echo     Dim objRefresher, objRefreshableItem >> tmp-DispProcess3.vbs

echo     Dim objServicesCimv2 >> tmp-DispProcess3.vbs

echo     Dim strOutputLine >> tmp-DispProcess3.vbs

echo     Set objWMIService ^= GetObject^(^"winmgmts:^" _ >> tmp-DispProcess3.vbs

echo             ^+ ^"^{impersonationLevel^=impersonate^}!^\^\^.^\root^\cimv2^") >> tmp-DispProcess3.vbs

echo     Set colSettings ^= objWMIService^.ExecQuery _ >> tmp-DispProcess3.vbs

echo                             ^(^"Select * from Win32_ComputerSystem^") >> tmp-DispProcess3.vbs

echo     For Each objComputer in colSettings  >> tmp-DispProcess3.vbs

echo         iNumberOfProcessors ^= objComputer^.NumberOfProcessors >> tmp-DispProcess3.vbs

echo         strComputerName ^= objComputer^.Name >> tmp-DispProcess3.vbs

echo     Next >> tmp-DispProcess3.vbs

echo     strComputer ^= ^"^.^" >> tmp-DispProcess3.vbs

echo     Set objRefresher ^= CreateObject^(^"WbemScripting^.SWbemRefresher^") >> tmp-DispProcess3.vbs

echo     Set objServicesCimv2 ^= GetObject^(^"winmgmts:^\^\^" ^+ strComputer ^+ _ >> tmp-DispProcess3.vbs

echo                                         ^"^\root^\cimv2^") >> tmp-DispProcess3.vbs

echo     If Not IsEmpty^(strOutputFile) Then >> tmp-DispProcess3.vbs

echo         If ^(NOT fsOpenFile^(strOutputFile, objOutputFile)) Then >> tmp-DispProcess3.vbs

echo             Call Wscript^.Echo ^(^"Could not open an output file^.^") >> tmp-DispProcess3.vbs

echo             Exit Sub >> tmp-DispProcess3.vbs

echo         End If >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo     If Err ^= 0 Then  >> tmp-DispProcess3.vbs

echo         Set objRefreshableItem ^= _ >> tmp-DispProcess3.vbs

echo                 objRefresher^.AddEnum^(objServicesCimv2 , _ >> tmp-DispProcess3.vbs

echo                 ^"Win32_PerfFormattedData_PerfProc_Process^") >> tmp-DispProcess3.vbs

echo         If IsEmpty^(strSampleInterval) Or CInt^(strSampleInterval) ^< 1 Then >> tmp-DispProcess3.vbs

echo             strSampleInterval ^= 800 >> tmp-DispProcess3.vbs

echo         End If >> tmp-DispProcess3.vbs

echo         objRefresher^.Refresh >> tmp-DispProcess3.vbs

echo         wscript^.sleep^(CInt^(strSampleInterval)) >> tmp-DispProcess3.vbs

echo         objRefresher^.Refresh >> tmp-DispProcess3.vbs

echo         For Each Process in objRefreshableItem^.ObjectSet >> tmp-DispProcess3.vbs

echo         If ^( ^(Process^.Name ^<^> ^"Idle^") AND _ >> tmp-DispProcess3.vbs

echo              ^(Process^.Name ^<^> ^"_Total^") ) Then >> tmp-DispProcess3.vbs

echo             If IsEmpty^(strPercentageThreshold) Then >> tmp-DispProcess3.vbs

echo                 strPercentageThreshold ^= 1 >> tmp-DispProcess3.vbs

echo             End If >> tmp-DispProcess3.vbs

echo             If CInt^(strPercentageThreshold) ^<^= 0 Or CInt^(strPercentageThreshold) ^> 100 Then >> tmp-DispProcess3.vbs

echo                 strPercentageThreshold ^= 1 >> tmp-DispProcess3.vbs

echo             End If >> tmp-DispProcess3.vbs

echo             If CInt^(^(Process^.PercentProcessorTime ^/ iNumberOfProcessors)) ^>^= CInt^(strPercentageThreshold) Then >> tmp-DispProcess3.vbs

echo                 strOutputLine ^= strComputerName ^& _ >> tmp-DispProcess3.vbs

echo                     ^"^|^" ^& Process^.Name ^& _ >> tmp-DispProcess3.vbs

echo                     ^"^|^" ^& Process^.IDProcess ^& _ >> tmp-DispProcess3.vbs

echo                     ^"^|^" ^& ^(Process^.PercentProcessorTime ^/ iNumberOfProcessors) ^& _ >> tmp-DispProcess3.vbs

echo                     ^"^|^" >> tmp-DispProcess3.vbs

echo                  Call WriteLine^(strOutputLine, objOutputFile) >> tmp-DispProcess3.vbs

echo             End If >> tmp-DispProcess3.vbs

echo         End If >> tmp-DispProcess3.vbs

echo         Next >> tmp-DispProcess3.vbs

echo     Else >> tmp-DispProcess3.vbs

echo         WScript^.Echo Err^.Description >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo     If IsObject^(objOutputFile) Then >> tmp-DispProcess3.vbs

echo         objOutputFile^.Close >> tmp-DispProcess3.vbs

echo         Call Wscript^.Echo ^(^"Results are saved in file ^" ^& strOutputFile ^& ^"^.^") >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo     Set objWshNetwork ^= Nothing >> tmp-DispProcess3.vbs

echo     Set objRefresher ^= Nothing >> tmp-DispProcess3.vbs

echo     Set objServicesCimv2 ^= Nothing >> tmp-DispProcess3.vbs

echo     Set objRefreshableItem ^= Nothing >> tmp-DispProcess3.vbs

echo     Set objWMIService ^= Nothing >> tmp-DispProcess3.vbs

echo     Set colSettings ^= Nothing >> tmp-DispProcess3.vbs

echo End Sub >> tmp-DispProcess3.vbs

echo Sub WriteLine^(ByVal strMessage, ByVal objFile) >> tmp-DispProcess3.vbs

echo     On Error Resume Next >> tmp-DispProcess3.vbs

echo     If IsObject^(objFile) then        >> tmp-DispProcess3.vbs

echo         objFile^.WriteLine strMessage >> tmp-DispProcess3.vbs

echo     Else >> tmp-DispProcess3.vbs

echo         Call Wscript^.Echo^( strMessage ) >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo End Sub >> tmp-DispProcess3.vbs

echo Private Function fsOpenFile^(ByVal strFileName, ByRef objOpenFile) >> tmp-DispProcess3.vbs

echo     ON ERROR GOTO 0 >> tmp-DispProcess3.vbs

echo     Dim objFileSystem >> tmp-DispProcess3.vbs

echo     Dim strFilePath >> tmp-DispProcess3.vbs

echo     Set objFileSystem ^= Nothing >> tmp-DispProcess3.vbs

echo     If IsEmpty^(strFileName) OR strFileName ^= ^"^" Then >> tmp-DispProcess3.vbs

echo         fsOpenFile ^= False >> tmp-DispProcess3.vbs

echo         Set objOpenFile ^= Nothing >> tmp-DispProcess3.vbs

echo         Exit Function >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo     Set objFileSystem ^= CreateObject^(^"Scripting^.FileSystemObject^") >> tmp-DispProcess3.vbs

echo     If fsErrorOccurred^(^"Could not create filesystem object^.^") Then >> tmp-DispProcess3.vbs

echo         fsOpenFile ^= False >> tmp-DispProcess3.vbs

echo         Set objOpenFile ^= Nothing >> tmp-DispProcess3.vbs

echo         Exit Function >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo     Set objOpenFile ^= objFileSystem^.OpenTextFile^(strFileName, 2, True) >> tmp-DispProcess3.vbs

echo     If fsErrorOccurred^(^"Could not open^") Then >> tmp-DispProcess3.vbs

echo         fsOpenFile ^= False >> tmp-DispProcess3.vbs

echo         Set objOpenFile ^= Nothing >> tmp-DispProcess3.vbs

echo         Exit Function >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo     fsOpenFile ^= True >> tmp-DispProcess3.vbs

echo End Function >> tmp-DispProcess3.vbs

echo Sub fsBuildPath^(ByVal strFileName) >> tmp-DispProcess3.vbs

echo     ON ERROR GOTO 0 >> tmp-DispProcess3.vbs

echo 	Dim fsoPathToBuild >> tmp-DispProcess3.vbs

echo 	Dim strDirPath >> tmp-DispProcess3.vbs

echo 	Set fsoPathToBuild ^= CreateObject^(^"Scripting^.FileSystemObject^") >> tmp-DispProcess3.vbs

echo     If InStrRev^(strFileName, ^"^\^") ^> 2 Then >> tmp-DispProcess3.vbs

echo         strDirPath ^= Left^(strFileName, ^(InStrRev^(strFileName, ^"^\^") - 1)) >> tmp-DispProcess3.vbs

echo     Else >> tmp-DispProcess3.vbs

echo         exit sub        >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo     If fsoPathToBuild^.FolderExists^(strDirPath) Then exit sub >> tmp-DispProcess3.vbs

echo     fsBuildPath^(fsoPathToBuild^.GetParentFolderName^(strDirPath)) >> tmp-DispProcess3.vbs

echo     fsoPathToBuild^.CreateFolder^(strDirPath) >> tmp-DispProcess3.vbs

echo     Set fsoPathToBuild ^= Nothing >> tmp-DispProcess3.vbs

echo End Sub >> tmp-DispProcess3.vbs

echo Private Function fsErrorOccurred ^(ByVal strIn) >> tmp-DispProcess3.vbs

echo     ON ERROR GOTO 0 >> tmp-DispProcess3.vbs

echo     If Err^.Number Then >> tmp-DispProcess3.vbs

echo         Call Wscript^.Echo^( ^"Error 0x^" ^& CStr^(Hex^(Err^.Number)) ^& ^": ^" ^& strIn) >> tmp-DispProcess3.vbs

echo         If Err^.Description ^<^> ^"^" Then >> tmp-DispProcess3.vbs

echo             Call Wscript^.Echo^( ^"Error description: ^" ^& Err^.Description) >> tmp-DispProcess3.vbs

echo         End If >> tmp-DispProcess3.vbs

echo         Err^.Clear >> tmp-DispProcess3.vbs

echo         fsErrorOccurred ^= True >> tmp-DispProcess3.vbs

echo     Else >> tmp-DispProcess3.vbs

echo         fsErrorOccurred ^= False >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo End Function >> tmp-DispProcess3.vbs

echo Private Function intParseCmdLine^( ByRef strOutputFile, _ >> tmp-DispProcess3.vbs

echo                                   ByRef strPercentageThreshold, _ >> tmp-DispProcess3.vbs

echo                                   ByRef strSampleInterval) >> tmp-DispProcess3.vbs

echo     ON ERROR GOTO 0 >> tmp-DispProcess3.vbs

echo     Dim strFlag >> tmp-DispProcess3.vbs

echo     Dim intState, intArgIter, intWidth >> tmp-DispProcess3.vbs

echo     Dim objFileSystem >> tmp-DispProcess3.vbs

echo     If Wscript^.Arguments^.Count ^> 0 Then >> tmp-DispProcess3.vbs

echo         strFlag ^= Wscript^.arguments^.Item^(0) >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo     If IsEmpty^(strFlag) Then                >> tmp-DispProcess3.vbs

echo         intParseCmdLine ^= CONST_PROCEED >> tmp-DispProcess3.vbs

echo         Exit Function >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo     If ^(strFlag^=^"help^") OR ^(strFlag^=^"^/h^") OR ^(strFlag^=^"^\h^") OR ^(strFlag^=^"-h^") _ >> tmp-DispProcess3.vbs

echo         OR ^(strFlag ^= ^"^\?^") OR ^(strFlag ^= ^"^/?^") OR ^(strFlag ^= ^"?^") _  >> tmp-DispProcess3.vbs

echo         OR ^(strFlag^=^"-?^") OR ^(strFlag^=^"h^") Then >> tmp-DispProcess3.vbs

echo         intParseCmdLine ^= CONST_SHOW_USAGE >> tmp-DispProcess3.vbs

echo         Exit Function >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo      intArgIter ^= 0 >> tmp-DispProcess3.vbs

echo     Do While intArgIter ^<^= Wscript^.arguments^.Count - 1 >> tmp-DispProcess3.vbs

echo         Select Case Left^(LCase^(Wscript^.arguments^.Item^(intArgIter)),2) >> tmp-DispProcess3.vbs

echo             Case ^"^/o^" >> tmp-DispProcess3.vbs

echo                 If Not cmdlineGetArg^(^"Output File^", strOutputFile, intArgIter) Then >> tmp-DispProcess3.vbs

echo                     intParseCmdLine ^= CONST_ERROR >> tmp-DispProcess3.vbs

echo                     Exit Function >> tmp-DispProcess3.vbs

echo                 End If >> tmp-DispProcess3.vbs

echo                 intArgIter ^= intArgIter ^+ 1 >> tmp-DispProcess3.vbs

echo             Case ^"-o^" >> tmp-DispProcess3.vbs

echo                 If Not cmdlineGetArg^(^"Output File^", strOutputFile, intArgIter) Then >> tmp-DispProcess3.vbs

echo                     intParseCmdLine ^= CONST_ERROR >> tmp-DispProcess3.vbs

echo                     Exit Function >> tmp-DispProcess3.vbs

echo                 End If >> tmp-DispProcess3.vbs

echo                 intArgIter ^= intArgIter ^+ 1 >> tmp-DispProcess3.vbs

echo             Case ^"^/p^" >> tmp-DispProcess3.vbs

echo                 If Not cmdlineGetArg^(^"Percentage Threshold^", strPercentageThreshold, intArgIter) Then >> tmp-DispProcess3.vbs

echo                     intParseCmdLine ^= CONST_ERROR >> tmp-DispProcess3.vbs

echo                     Exit Function >> tmp-DispProcess3.vbs

echo                 End If >> tmp-DispProcess3.vbs

echo                 intArgIter ^= intArgIter ^+ 1 >> tmp-DispProcess3.vbs

echo             Case ^"-p^" >> tmp-DispProcess3.vbs

echo                 If Not cmdlineGetArg^(^"Percentage Threshold^", strPercentageThreshold, intArgIter) Then >> tmp-DispProcess3.vbs

echo                     intParseCmdLine ^= CONST_ERROR >> tmp-DispProcess3.vbs

echo                     Exit Function >> tmp-DispProcess3.vbs

echo                 End If >> tmp-DispProcess3.vbs

echo                 intArgIter ^= intArgIter ^+ 1 >> tmp-DispProcess3.vbs

echo             Case ^"^/i^" >> tmp-DispProcess3.vbs

echo                 If Not cmdlineGetArg^(^"Sample Interval^", strSampleInterval, intArgIter) Then >> tmp-DispProcess3.vbs

echo                     intParseCmdLine ^= CONST_ERROR >> tmp-DispProcess3.vbs

echo                     Exit Function >> tmp-DispProcess3.vbs

echo                 End If >> tmp-DispProcess3.vbs

echo                 intArgIter ^= intArgIter ^+ 1 >> tmp-DispProcess3.vbs

echo             Case ^"-i^" >> tmp-DispProcess3.vbs

echo                 If Not cmdlineGetArg^(^"Sample Interval^", strSampleInterval, intArgIter) Then >> tmp-DispProcess3.vbs

echo                     intParseCmdLine ^= CONST_ERROR >> tmp-DispProcess3.vbs

echo                     Exit Function >> tmp-DispProcess3.vbs

echo                 End If >> tmp-DispProcess3.vbs

echo                 intArgIter ^= intArgIter ^+ 1 >> tmp-DispProcess3.vbs

echo             Case Else  >> tmp-DispProcess3.vbs

echo                 Call Wscript^.Echo^(^"Invalid or misplaced parameter: ^" _ >> tmp-DispProcess3.vbs

echo                    ^& Wscript^.arguments^.Item^(intArgIter) ^& vbCRLF _ >> tmp-DispProcess3.vbs

echo                    ^& ^"Please check the input and try again,^" ^& vbCRLF _ >> tmp-DispProcess3.vbs

echo                    ^& ^"or invoke with '^/?' for help with the syntax^.^") >> tmp-DispProcess3.vbs

echo                 Wscript^.Quit >> tmp-DispProcess3.vbs

echo         End Select >> tmp-DispProcess3.vbs

echo     Loop '** intArgIter ^<^= Wscript^.arguments^.Count - 1 >> tmp-DispProcess3.vbs

echo     If IsEmpty^(intParseCmdLine) Then _ >> tmp-DispProcess3.vbs

echo         intParseCmdLine ^= CONST_PROCEED >> tmp-DispProcess3.vbs

echo End Function >> tmp-DispProcess3.vbs

echo Private Function cmdlineGetArg ^( ByVal StrVarName,   _ >> tmp-DispProcess3.vbs

echo                                  ByRef strVar,       _ >> tmp-DispProcess3.vbs

echo                                  ByRef intArgIter)  >> tmp-DispProcess3.vbs

echo     cmdlineGetArg ^= False >> tmp-DispProcess3.vbs

echo     If Len^(Wscript^.Arguments^(intArgIter)) ^> 2 then >> tmp-DispProcess3.vbs

echo         If Mid^(Wscript^.Arguments^(intArgIter),3,1) ^= ^":^" then >> tmp-DispProcess3.vbs

echo             If Len^(Wscript^.Arguments^(intArgIter)) ^> 3 then >> tmp-DispProcess3.vbs

echo                 strVar ^= Right^(Wscript^.Arguments^(intArgIter), _ >> tmp-DispProcess3.vbs

echo                          Len^(Wscript^.Arguments^(intArgIter)) - 3) >> tmp-DispProcess3.vbs

echo                 cmdlineGetArg ^= True >> tmp-DispProcess3.vbs

echo                 Exit Function >> tmp-DispProcess3.vbs

echo             Else >> tmp-DispProcess3.vbs

echo                 intArgIter ^= intArgIter ^+ 1 >> tmp-DispProcess3.vbs

echo                 If intArgIter ^> ^(Wscript^.Arguments^.Count - 1) Then >> tmp-DispProcess3.vbs

echo                     Call Wscript^.Echo^( ^"Invalid ^" ^& StrVarName ^& ^"^.^") >> tmp-DispProcess3.vbs

echo                     Call Wscript^.Echo^( ^"Please check the input and try again^.^") >> tmp-DispProcess3.vbs

echo                     Exit Function >> tmp-DispProcess3.vbs

echo                 End If >> tmp-DispProcess3.vbs

echo                 strVar ^= Wscript^.Arguments^.Item^(intArgIter) >> tmp-DispProcess3.vbs

echo                 If Err^.Number Then >> tmp-DispProcess3.vbs

echo                     Call Wscript^.Echo^( ^"Invalid ^" ^& StrVarName ^& ^"^.^") >> tmp-DispProcess3.vbs

echo                     Call Wscript^.Echo^( ^"Please check the input and try again^.^") >> tmp-DispProcess3.vbs

echo                     Exit Function >> tmp-DispProcess3.vbs

echo                 End If >> tmp-DispProcess3.vbs

echo                 If InStr^(strVar, ^"^/^") Then >> tmp-DispProcess3.vbs

echo                     Call Wscript^.Echo^( ^"Invalid ^" ^& StrVarName) >> tmp-DispProcess3.vbs

echo                     Call Wscript^.Echo^( ^"Please check the input and try again^.^") >> tmp-DispProcess3.vbs

echo                     Exit Function >> tmp-DispProcess3.vbs

echo                 End If >> tmp-DispProcess3.vbs

echo                 cmdlineGetArg ^= True >> tmp-DispProcess3.vbs

echo             End If >> tmp-DispProcess3.vbs

echo         Else >> tmp-DispProcess3.vbs

echo             strVar ^= Right^(Wscript^.Arguments^(intArgIter), _ >> tmp-DispProcess3.vbs

echo                      Len^(Wscript^.Arguments^(intArgIter)) - 2) >> tmp-DispProcess3.vbs

echo             cmdlineGetArg ^= True  >> tmp-DispProcess3.vbs

echo             Exit Function >> tmp-DispProcess3.vbs

echo         End If >> tmp-DispProcess3.vbs

echo     Else >> tmp-DispProcess3.vbs

echo         intArgIter ^= intArgIter ^+ 1 >> tmp-DispProcess3.vbs

echo         If intArgIter ^> ^(Wscript^.Arguments^.Count - 1) Then >> tmp-DispProcess3.vbs

echo             Call Wscript^.Echo^( ^"Invalid ^" ^& StrVarName ^& ^"^.^") >> tmp-DispProcess3.vbs

echo             Call Wscript^.Echo^( ^"Please check the input and try again^.^") >> tmp-DispProcess3.vbs

echo             Exit Function >> tmp-DispProcess3.vbs

echo         End If >> tmp-DispProcess3.vbs

echo         strVar ^= Wscript^.Arguments^.Item^(intArgIter) >> tmp-DispProcess3.vbs

echo         If Err^.Number Then >> tmp-DispProcess3.vbs

echo             Call Wscript^.Echo^( ^"Invalid ^" ^& StrVarName ^& ^"^.^") >> tmp-DispProcess3.vbs

echo             Call Wscript^.Echo^( ^"Please check the input and try again^.^") >> tmp-DispProcess3.vbs

echo             Exit Function >> tmp-DispProcess3.vbs

echo         End If >> tmp-DispProcess3.vbs

echo         If InStr^(strVar, ^"^/^") Then >> tmp-DispProcess3.vbs

echo             Call Wscript^.Echo^( ^"Invalid ^" ^& StrVarName) >> tmp-DispProcess3.vbs

echo             Call Wscript^.Echo^( ^"Please check the input and try again^.^") >> tmp-DispProcess3.vbs

echo             Exit Function >> tmp-DispProcess3.vbs

echo         End If >> tmp-DispProcess3.vbs

echo         cmdlineGetArg ^= True >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo End Function >> tmp-DispProcess3.vbs

echo Sub VerifyHostIsCscript^() >> tmp-DispProcess3.vbs

echo     ON ERROR RESUME NEXT >> tmp-DispProcess3.vbs

echo     Dim strFullName, strCommand, i, j, intStatus >> tmp-DispProcess3.vbs

echo     strFullName ^= WScript^.FullName >> tmp-DispProcess3.vbs

echo     If Err^.Number then >> tmp-DispProcess3.vbs

echo         Call Wscript^.Echo^( ^"Error 0x^" ^& CStr^(Hex^(Err^.Number)) ^& ^" occurred^.^" ) >> tmp-DispProcess3.vbs

echo         If Err^.Description ^<^> ^"^" Then >> tmp-DispProcess3.vbs

echo             Call Wscript^.Echo^( ^"Error description: ^" ^& Err^.Description ^& ^"^.^" ) >> tmp-DispProcess3.vbs

echo         End If >> tmp-DispProcess3.vbs

echo         intStatus ^=  CONST_ERROR >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo     i ^= InStr^(1, strFullName, ^"^.exe^", 1) >> tmp-DispProcess3.vbs

echo     If i ^= 0 Then >> tmp-DispProcess3.vbs

echo         intStatus ^=  CONST_ERROR >> tmp-DispProcess3.vbs

echo     Else >> tmp-DispProcess3.vbs

echo         j ^= InStrRev^(strFullName, ^"^\^", i, 1) >> tmp-DispProcess3.vbs

echo         If j ^= 0 Then >> tmp-DispProcess3.vbs

echo             intStatus ^=  CONST_ERROR >> tmp-DispProcess3.vbs

echo         Else >> tmp-DispProcess3.vbs

echo             strCommand ^= Mid^(strFullName, j^+1, i-j-1) >> tmp-DispProcess3.vbs

echo             Select Case LCase^(strCommand) >> tmp-DispProcess3.vbs

echo                 Case ^"cscript^" >> tmp-DispProcess3.vbs

echo                     intStatus ^= CONST_CSCRIPT >> tmp-DispProcess3.vbs

echo                 Case ^"wscript^" >> tmp-DispProcess3.vbs

echo                     intStatus ^= CONST_WSCRIPT >> tmp-DispProcess3.vbs

echo                 Case Else       >> tmp-DispProcess3.vbs

echo                     Call Wscript^.Echo^( ^"An unexpected program was used to ^" _ >> tmp-DispProcess3.vbs

echo                                        ^& ^"run this script^.^" ) >> tmp-DispProcess3.vbs

echo                     Call Wscript^.Echo^( ^"Only CScript^.Exe or WScript^.Exe can ^" _ >> tmp-DispProcess3.vbs

echo                                        ^& ^"be used to run this script^.^" ) >> tmp-DispProcess3.vbs

echo                     intStatus ^= CONST_ERROR >> tmp-DispProcess3.vbs

echo                 End Select >> tmp-DispProcess3.vbs

echo         End If >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo     If intStatus ^<^> CONST_CSCRIPT Then >> tmp-DispProcess3.vbs

echo         Call WScript^.Echo^( ^"Please run this script using CScript^.^" ^& vbCRLF ^+ _ >> tmp-DispProcess3.vbs

echo              ^"This can be achieved by^" ^& vbCRLF ^+ _ >> tmp-DispProcess3.vbs

echo              ^"1^. Using ^"^"CScript ^" ^& Wscript^.ScriptName ^& ^" arguments^"^" for Windows 95^/98 or^" _ >> tmp-DispProcess3.vbs

echo              ^& vbCRLF ^& ^"2^. Changing the default Windows Scripting Host ^" _ >> tmp-DispProcess3.vbs

echo              ^& ^"setting to CScript^" ^& vbCRLF ^& ^"    using ^"^"CScript ^" _ >> tmp-DispProcess3.vbs

echo              ^& ^"^/^/H:CScript ^/^/S^"^" and running the script using^" ^& vbCRLF ^+ _ >> tmp-DispProcess3.vbs

echo              ^"    ^"^"^" ^& Wscript^.ScriptName ^& ^" arguments^"^" for Windows NT^/2000^.^" ) >> tmp-DispProcess3.vbs

echo         WScript^.Quit >> tmp-DispProcess3.vbs

echo     End If >> tmp-DispProcess3.vbs

echo End Sub >> tmp-DispProcess3.vbs

echo Private Sub ShowUsage^() >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"Display all processes using over 'x' percent CPU^.^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"SYNTAX:^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"  Display_Specific_Process_CPU_Usage_in_Percent^.vbs ^[^/O ^<outputfile^>^]^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"                                                    ^[^/P ^<%%_threshold^>^]^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"                                                    ^[^/I ^<sample_interval^>^]^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"PARAMETER SPECIFIERS:^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   outputfile        The output file name^. Path can be an existing UNC^.^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   %%_threshold       %% to use as a threshold value, e^.g^., 8 or 33^.^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   sample_interval   Interval in milliseconds^.^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   Valid option variations: ^/O,^/o,-O,-o,^/P,^/p^.-P,-p,^/I^.^/i^.-I,-i^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"DEFAULT VALUES:^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   Output goes to display^.^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"^.^.^.Percentage threshold is 1%%^. ^(This is good for almost all cases^.)^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   Sample Interval is 800 milliseconds^.^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   Note: Because the timeslice is so brief, and the period between^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   checks is just 800 milliseconds, using 1%% will work for just about^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   any situation because most other processes will be just 0%% during^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   the snapshot period^. The interval may be increased for a greater^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   sample period^.^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"OUTPUT FORMAT:^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"  system_name^|process_name^|PID^|CPU_usage_percentage^|^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"EXAMPLES:^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"1^. cscript Display_Processes_Using_More_Than_x_Percent_CPU^.vbs^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   Lists any processes using over 1%% CPU^.^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"2^. cscript Display_Processes_Using_More_Than_x_Percent_CPU^.vbs ^/P 24^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   Lists any jobs using over 24%% CPU^.^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"3^. cscript Display_Processes_Using_More_Than_x_Percent_CPU^.vbs ^/O file^.txt^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   Lists any jobs using over 1%% CPU and writes the output to 'file^.txt'^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"4^. cscript Display_Processes_Using_More_Than_x_Percent_CPU^.vbs ^/I 1500^" >> tmp-DispProcess3.vbs

echo     Wscript^.Echo ^"   Lists any jobs using over 1%% CPU, but uses a 1^.5 second sample interval^.^" >> tmp-DispProcess3.vbs

echo End Sub >> tmp-DispProcess3.vbs



rem Execute the script.
cscript.exe  //nologo tmp-DispProcess3.vbs 
del /f tmp-DispProcess3.vbs
