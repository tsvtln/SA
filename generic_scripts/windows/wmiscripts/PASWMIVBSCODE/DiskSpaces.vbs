'-----------------------------------------------------------------------------
'File    : DiskSpaces.VBS
'Purpose : Sample script test for Advanced Host Monitor
'Comment : Checks difference between free disk space on drive C: and drive D: 
'          Sets status to "Bad" when drive C: has less amount of free space 
'          than drive D:
'Language: VBScript
'Version : 1.0
'-----------------------------------------------------------------------------
Option Explicit

const statusAlive       = "Host is alive:"
const statusDead        = "No answer:"
const statusUnknown     = "Unknown:"
const statusNotResolved = "Unknown host:"
const statusOk          = "Ok:"
const statusBad         = "Bad:"
const statusBadContents = "Bad contents:"

'---- entry point ----

FUNCTION PerformTest()
  DIM DeltaSpace
  DeltaSpace = AvailableSpace("C:\") - AvailableSpace("D:\")
  IF DeltaSpace >= 0 THEN
     performtest = statusOk+CStr(DeltaSpace/1024)+" Kb"
  ELSE
     performtest = statusBad+CStr(DeltaSpace/1024)+" Kb"
  END IF
END FUNCTION

'------ function -----

FUNCTION AvailableSpace(drvPath)
  Dim fso, d
  Set fso = CreateObject("Scripting.FileSystemObject")
  Set d = fso.GetDrive(fso.GetDriveName(drvPath))
  AvailableSpace = d.AvailableSpace
END FUNCTION
