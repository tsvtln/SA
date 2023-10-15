'-----------------------------------------------------------------------------
'Purpose : Sample script test for Advanced Host Monitor
'Comment : Checks list of disk drives on local system. Set test's status to 
'          "Bad" when list of drives changes. E.g. when user map/unmap network
'          drive.
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

FUNCTION performtest()
  DIM CurrList
  IF "%Reply%"="%"+"Reply"+"%" THEN
     performtest = statusUnknown+"Please enable 'Translate macros' option"
  ELSE
    CurrList = GetDrivesList
    IF CurrList<>"%Reply%" THEN
       performtest = statusBad+CurrList
    ELSE
       performtest = statusOk+CurrList
    END IF
  END IF
END FUNCTION

'----- functions -----

FUNCTION GetDrivesList()
  DIM DList, FSO, Drive
  DList = ""
  Set FSO = CreateObject("Scripting.FileSystemObject")
  For Each Drive In FSO.Drives
      DList = DList + Drive.DriveLetter
    Next
  Set FSO = Nothing
  GetDrivesList = DList
END FUNCTION


FUNCTION GetCdromDrives()
  DIM DList, FSO, Drive
  DList = ""
  FSO = CreateObject("Scripting.FileSystemObject")
  FOR Each Drive In FSO.Drives
    If Drive.DriveType = 4 Then
       DList = DList + Drive.DriveLetter
    End If
    Next
  Set FSO = Nothing
  GetCdromDrives = DList
END FUNCTION
