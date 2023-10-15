Dim lib, job

Set lib = CreateObject("VixCOM.VixLib")

' Connect to the local installation of Workstation. This also intializes the VIX API.
Set job = lib.Connect(VixCOM.Constants.VIX_API_VERSION, VixCOM.Constants.VIX_SERVICEPROVIDER_VMWARE_WORKSTATION, Empty, 0, Empty, Empty, 0, Nothing, Nothing)

' results needs to be initialized before it's used, even if it's just going to be overwritten.
Set results = Nothing

' Wait waits until the job started by an asynchronous function call has finished. It also
' can be used to get various properties from the job. The first argument is an array
' of VIX property IDs that specify the properties requested. When Wait returns, the 
' second argument will be set to an array that holds the values for those properties,
' one for each ID requested.
err = job.Wait(Array(VixCOM.Constants.VIX_PROPERTY_JOB_RESULT_HANDLE), results)
QuitIfError(err)

' The job result handle will be first element in the results array.
Set host = results(0)

' Open the virtual machine with the given .vmx file.
Set job = host.OpenVM("C:\\VMs\\winxpprowithsp2\\winxpprowithsp2.vmx", Nothing)
err = job.Wait(Array(VixCOM.Constants.VIX_PROPERTY_JOB_RESULT_HANDLE), results)
QuitIfError(err)

Set vm = results(0)

' Power on the virtual machine we just opened. This will launch Workstation if it hasn't
' already been started.
Set job = vm.PowerOn(VixCOM.Constants.VIX_VMPOWEROP_LAUNCH_GUI, Nothing, Nothing)
' WaitWithoutResults is just like Wait, except it does not get any properties. 
err = job.WaitWithoutResults()
QuitIfError(err)

' Here you would do any operations on the guest inside the virtual machine.

' Power off the virtual machine. This will cause Workstation to shut down if it
' was not running previous to the call to PowerOn.
Set job = vm.PowerOff(VixCOM.Constants.VIX_VMPOWEROP_NORMAL, Nothing)
err = job.WaitWithoutResults()
QuitIfError(err)

host.Disconnect()


'--------------------------------------------------------------------------------
' A simple error handler. Prints the error message to the console, and then exits.
sub QuitIfError(err)
   if lib.ErrorIndicatesFailure(err) then
      WScript.Echo("Error: " & lib.GetErrorText(err, empty))
      WScript.Quit
   end if
end sub