'-----------------------------------------------------------------------------
'File    : CheckWord.VBS
'Purpose : Sample script test for Advanced Host Monitor
'Comment : Statrs MS Word, opens document and returns number of characters in 
'          the document. If Microsoft Word is not installed or document does 
'          not exist, test's status will be "Uknown"
'-----------------------------------------------------------------------------
Option Explicit

const statusAlive       = "Host is alive:"
const statusDead        = "No answer:"
const statusUnknown     = "Unknown:"
const statusNotResolved = "Unknown host:"
const statusOk          = "Ok:"
const statusBad         = "Bad:"
const statusBadContents = "Bad contents:"

const FileName = "C:\My Documents\Test1.doc"

'---- entry point ----

FUNCTION performtest()
 Dim MSWord
 Set MSWord = CreateObject("Word.Application")
 MSWord.Documents.Open(FileName)
 performtest="Ok:"+FormatNumber(MSWord.ActiveDocument.Characters.Count,0)
 MSWord.Application.Quit   
 Set MSWord = Nothing      
END FUNCTION
