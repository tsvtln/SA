strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_Process",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_Process instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Caption: " & objItem.Caption
    Wscript.Echo "CommandLine: " & objItem.CommandLine
    Wscript.Echo "CreationClassName: " & objItem.CreationClassName
    Wscript.Echo "CreationDate: " & objItem.CreationDate
    Wscript.Echo "CSCreationClassName: " & objItem.CSCreationClassName
    Wscript.Echo "CSName: " & objItem.CSName
    Wscript.Echo "Description: " & objItem.Description
    Wscript.Echo "ExecutablePath: " & objItem.ExecutablePath
    Wscript.Echo "ExecutionState: " & objItem.ExecutionState
    Wscript.Echo "Handle: " & objItem.Handle
    Wscript.Echo "HandleCount: " & objItem.HandleCount
    Wscript.Echo "InstallDate: " & objItem.InstallDate
    Wscript.Echo "KernelModeTime: " & objItem.KernelModeTime
    Wscript.Echo "MaximumWorkingSetSize: " & objItem.MaximumWorkingSetSize
    Wscript.Echo "MinimumWorkingSetSize: " & objItem.MinimumWorkingSetSize
    Wscript.Echo "Name: " & objItem.Name
    Wscript.Echo "OSCreationClassName: " & objItem.OSCreationClassName
    Wscript.Echo "OSName: " & objItem.OSName
    Wscript.Echo "OtherOperationCount: " & objItem.OtherOperationCount
    Wscript.Echo "OtherTransferCount: " & objItem.OtherTransferCount
    Wscript.Echo "PageFaults: " & objItem.PageFaults
    Wscript.Echo "PageFileUsage: " & objItem.PageFileUsage
    Wscript.Echo "ParentProcessId: " & objItem.ParentProcessId
    Wscript.Echo "PeakPageFileUsage: " & objItem.PeakPageFileUsage
    Wscript.Echo "PeakVirtualSize: " & objItem.PeakVirtualSize
    Wscript.Echo "PeakWorkingSetSize: " & objItem.PeakWorkingSetSize
    Wscript.Echo "Priority: " & objItem.Priority
    Wscript.Echo "PrivatePageCount: " & objItem.PrivatePageCount
    Wscript.Echo "ProcessId: " & objItem.ProcessId
    Wscript.Echo "QuotaNonPagedPoolUsage: " & objItem.QuotaNonPagedPoolUsage
    Wscript.Echo "QuotaPagedPoolUsage: " & objItem.QuotaPagedPoolUsage
    Wscript.Echo "QuotaPeakNonPagedPoolUsage: " & objItem.QuotaPeakNonPagedPoolUsage
    Wscript.Echo "QuotaPeakPagedPoolUsage: " & objItem.QuotaPeakPagedPoolUsage
    Wscript.Echo "ReadOperationCount: " & objItem.ReadOperationCount
    Wscript.Echo "ReadTransferCount: " & objItem.ReadTransferCount
    Wscript.Echo "SessionId: " & objItem.SessionId
    Wscript.Echo "Status: " & objItem.Status
    Wscript.Echo "TerminationDate: " & objItem.TerminationDate
    Wscript.Echo "ThreadCount: " & objItem.ThreadCount
    Wscript.Echo "UserModeTime: " & objItem.UserModeTime
    Wscript.Echo "VirtualSize: " & objItem.VirtualSize
    Wscript.Echo "WindowsVersion: " & objItem.WindowsVersion
    Wscript.Echo "WorkingSetSize: " & objItem.WorkingSetSize
    Wscript.Echo "WriteOperationCount: " & objItem.WriteOperationCount
    Wscript.Echo "WriteTransferCount: " & objItem.WriteTransferCount
Next