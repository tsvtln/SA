Option Explicit

const statusAlive       = "Host is alive:"
const statusDead        = "No answer:"
const statusUnknown     = "Unknown:"
const statusNotResolved = "Unknown host:"
const statusOk          = "Ok:"
const statusBad         = "Bad:"
const statusBadContents = "Bad contents:"

const IEkey = "HKCU\Software\Microsoft\Internet Explorer\Main\Start Page"

'---- entry point ----

FUNCTION performtest()
  Dim WshShell, KeyStr
  IF "%Reply%"="%"+"Reply"+"%" THEN
     performtest = statusUnknown+"Please enable 'Translate macros' option"
  ELSE
    Set WshShell = CreateObject("WScript.Shell")
    KeyStr = WshShell.RegRead(IEkey)
    IF (KeyStr<>"%Reply%") THEN
       performtest = statusBad+KeyStr
    ELSE
       performtest = statusOk+KeyStr
    END IF
  END IF
END FUNCTION
