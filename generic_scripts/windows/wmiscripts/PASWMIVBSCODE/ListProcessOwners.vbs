On Error Resume Next
Dim strUser, strDomain, Result, Feedback
Dim arrPrivileges
Const wbemFlagReturnImmediately = &h10
Const wbemFlagForwardOnly = &h20

arrComputers = Array("LONDON")
For Each strComputer In arrComputers
   WScript.Echo
   WScript.Echo "=========================================="
   WScript.Echo "Computer: " & strComputer
   WScript.Echo "=========================================="

   Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2")
   Set colItems = objWMIService.ExecQuery("SELECT * FROM Win32_Process", "WQL", _
                                          wbemFlagReturnImmediately + wbemFlagForwardOnly)
' 		objWMIService.Security_.Privileges.AddAsString "SeDebugPrivilege", True
 		objWMIService.Security_.Privileges.AddAsString "SeTakeOwnershipPrivilege", True
    For Each objItem In colItems
'       WScript.Echo "Caption: " & objItem.Caption
'       WScript.Echo "CommandLine: " & objItem.CommandLine
'       WScript.Echo "CreationClassName: " & objItem.CreationClassName
'       WScript.Echo "CreationDate: " & objItem.CreationDate
'       WScript.Echo "CSCreationClassName: " & objItem.CSCreationClassName
'       WScript.Echo "CSName: " & objItem.CSName
'       WScript.Echo "Description: " & objItem.Description
'       WScript.Echo "ExecutablePath: " & objItem.ExecutablePath
'       WScript.Echo "ExecutionState: " & objItem.ExecutionState
'       WScript.Echo "Handle: " & objItem.Handle
'       WScript.Echo "HandleCount: " & objItem.HandleCount
'       WScript.Echo "InstallDate: " & objItem.InstallDate
'       WScript.Echo "KernelModeTime: " & objItem.KernelModeTime
'       WScript.Echo "MaximumWorkingSetSize: " & objItem.MaximumWorkingSetSize
'       WScript.Echo "MinimumWorkingSetSize: " & objItem.MinimumWorkingSetSize
       WScript.Echo "Name: " & objItem.Name
				Feedback = objItem.GetOwner(strUser, strDomain)
				If (strUser = "" Or IsNull(strUser)) Then strUser = "********"
				WScript.Echo "Owner: " & strUser & vbTab & "(" & GetOwnerResult(Feedback)& ")"
'       WScript.Echo "OSCreationClassName: " & objItem.OSCreationClassName
'       WScript.Echo "OSName: " & objItem.OSName
'       WScript.Echo "OtherOperationCount: " & objItem.OtherOperationCount
'       WScript.Echo "OtherTransferCount: " & objItem.OtherTransferCount
'       WScript.Echo "PageFaults: " & objItem.PageFaults
'       WScript.Echo "PageFileUsage: " & objItem.PageFileUsage
'       WScript.Echo "ParentProcessId: " & objItem.ParentProcessId
'       WScript.Echo "PeakPageFileUsage: " & objItem.PeakPageFileUsage
'       WScript.Echo "PeakVirtualSize: " & objItem.PeakVirtualSize
'       WScript.Echo "PeakWorkingSetSize: " & objItem.PeakWorkingSetSize
'       WScript.Echo "Priority: " & objItem.Priority
'       WScript.Echo "PrivatePageCount: " & objItem.PrivatePageCount
'       WScript.Echo "ProcessId: " & objItem.ProcessId
'       WScript.Echo "QuotaNonPagedPoolUsage: " & objItem.QuotaNonPagedPoolUsage
'       WScript.Echo "QuotaPagedPoolUsage: " & objItem.QuotaPagedPoolUsage
'       WScript.Echo "QuotaPeakNonPagedPoolUsage: " & objItem.QuotaPeakNonPagedPoolUsage
'       WScript.Echo "QuotaPeakPagedPoolUsage: " & objItem.QuotaPeakPagedPoolUsage
'       WScript.Echo "ReadOperationCount: " & objItem.ReadOperationCount
'       WScript.Echo "ReadTransferCount: " & objItem.ReadTransferCount
'       WScript.Echo "SessionId: " & objItem.SessionId
'       WScript.Echo "Status: " & objItem.Status
'       WScript.Echo "TerminationDate: " & objItem.TerminationDate
'       WScript.Echo "ThreadCount: " & objItem.ThreadCount
'       WScript.Echo "UserModeTime: " & objItem.UserModeTime
'       WScript.Echo "VirtualSize: " & objItem.VirtualSize
'       WScript.Echo "WindowsVersion: " & objItem.WindowsVersion
'       WScript.Echo "WorkingSetSize: " & objItem.WorkingSetSize
'       WScript.Echo "WriteOperationCount: " & objItem.WriteOperationCount
'       WScript.Echo "WriteTransferCount: " & objItem.WriteTransferCount
       WScript.Echo
   Next
Next
 
Function GetOwnerResult(Result)
	Select Case Result
		Case 0
			GetOwnerResult = "Successful completion"
		Case 2
			GetOwnerResult = "Access denied" 
		Case 3
			GetOwnerResult = "Insufficient privilege"
		Case 8
			GetOwnerResult = "Unknown failure" 
		Case 9
			GetOwnerResult = "Path not found" 
		Case 21
			GetOwnerResult = "Invalid parameter" 
	End Select
End Function