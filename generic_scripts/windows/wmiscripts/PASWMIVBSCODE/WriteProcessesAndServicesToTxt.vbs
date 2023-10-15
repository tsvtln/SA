strOut = "the following Processes are running " & vbcrlf
strOut2 = "the following Services are running " & vbcrlf
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select name, processID from win32_process where processID is not null"
wmiQuery2 = "Select name, processID from win32_Service where processID is not null"
Set objWMIService = getObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems
    strOut = strOut & objItem.name & vbcrlf
Next

Set colItems2 = objWMIService.ExecQuery(wmiQuery2)
For Each objItem2 in colItems2
If (objItem2.ProcessID) > 0 then
    strOut2 = strOut2 & objItem2.name & vbtab & objItem2.processID & vbcrlf
End if
Next

subWriteToFile

Sub SubWriteToFIle
Dim objFSO, objFile, strDeskTop
Set strDesktop = CreateObject("wscript.shell")' holds instance of WshSHell
strDesktop = strDesktop.specialFolders("desktop") ' recycle strDesktop here. 
Set objFSO = CreateObject("scripting.filesystemobject")
Set objFILE = objFSO.openTextFIle(strDeskTop & "\" & "servicesOUT.txt", 8, True)
objFIle.write strOut & vbcrlf & strOUT2
End sub
