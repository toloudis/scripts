param([string] $BackupRoot = '\\ds916\P70\dmt\P70\Data', [string] $RelativePath = 'D\headslayer', [switch] $Verify, [switch] $OverwriteOlder, [switch] $ShowOnlyErrors)

$backuprootpath = $BackupRoot + '\' + $RelativePath

if (!(Test-Path -LiteralPath $backuprootpath))
{
    Write-Host -ForegroundColor Red ("Backup folder '{0}' does not exist" -f $backuprootpath)
    Exit(1)
}

$backuprootpath_re = '^' + [regex]::Escape(($backuprootpath -replace '[/\\]$', '') + '\')

# force the restore to always use the C: drive and deposit in a RESTORE folder
$originalrootpath = $relativepath -replace '^(.)', 'C:\\RESTORE'
#$originalrootpath = $relativepath -replace '^(.)', '$1:'

$restorecount = 0
$verifycount = 0
$verifyerrors = 0
$newercount = 0
$oldercount = 0
$samedatecount = 0

# enumerate backup folders
@(
    Get-Item -LiteralPath $backuprootpath
    Get-ChildItem -Recurse -Directory -LiteralPath $backuprootpath
) | Foreach-Object {
    # for each folder, enumerate the backup files, for each original file, pick the most recent backup file
    Write-Progress("Processing folder '{0}'..." -f $_.FullName)
    Get-ChildItem -File -LiteralPath $_.FullName | Foreach-Object {
        Add-Member -InputObject $_ -MemberType NoteProperty -Name 'OriginalPath' -Value ($originalrootpath + '\' + (($_.FullName -replace $backuprootpath_re, '') -replace ' \(\d\d\d\d_\d\d_\d\d \d\d_\d\d_\d\d UTC\)', ''))
        $_
    } | Group-Object -Property 'OriginalPath' | Foreach-Object {

        $backupitem = ($_.Group | Foreach-Object {
                Add-Member -InputObject $_ -MemberType NoteProperty -Name 'BackupDateUTC' -Value ($_.Basename -replace '.* \((\d\d\d\d)_(\d\d)_(\d\d) (\d\d)_(\d\d)_(\d\d) UTC\)', '$1$2$3$4$5$6')
                $_
            } | Sort-Object -Property 'BackupDateUTC' | Select-Object -Last 1)

        # now we know what the backup file is, and what the original file was/is
        Write-Debug("Backup file: '{0}'" -f $backupitem.FullName)
        $originalfile = $_.Name
        Write-Debug("Original file: '{0}'" -f $originalfile)
        $originaldir = $originalfile -replace '[/\\][^/\\]+$', ''
        Write-Debug("Original folder: '{0}'" -f $originaldir)
        # create the original parent folder if needed
        if (!(Test-Path -LiteralPath $originaldir))
        {
            mkdir -Force $originaldir | Out-Null
            if (!(Test-Path -LiteralPath $originaldir))
            {
                Write-Host -ForegroundColor Red ("FATAl: failed to create directory '{0}'" -f $originaldir)
                Exit(1)
            }
        }
        # check if the original file exists
        $originalitem = Get-Item -Force -LiteralPath $originalfile -ErrorAction SilentlyContinue
        if ($null -eq $originalitem)
        {
            # no, restore it
            Copy-Item -Verbose -Destination $originalfile -LiteralPath $backupitem.FullName
            $restorecount = $restorecount + 1
        }
        else
        {
            # yes, compare timestamps
            $backupitem = Get-Item -LiteralPath $backupitem.FullName
            $skip = $false
            $verified = $null
            # assume the timestamps are identical if they are less than 2s apart to account for filesystem timestamp resolution
            if ([Math]::Abs(($originalitem.LastWriteTime - $backupitem.LastWriteTime).TotalSeconds) -lt 2)
            {
                $status = 'same date'
                $samedatecount = $samedatecount + 1
                if ($Verify)
                {
                    $verifycount = $verifycount + 1
                    & fcb.exe $originalfile $backupitem.FullName 2>&1 | Out-Null
                    if ($LASTEXITCODE -ne 0)
                    {
                        $verifyerrors = $verifyerrors + 1
                        Write-Host -ForegroundColor Red ("Files '{0}' and '{1}' are NOT identical" -f $originalfile, $backupitem.FullName)
                        $verified = $false
                    }
                    else {
                        $verified = $true
                    }
                }
                $skip = $true
            }
            elseif (($originalitem.LastWriteTime - $backupitem.LastWriteTime).TotalSeconds -ge 2)
            {
                $status = 'newer'
                $newercount = $newercount + 1
                $skip = $true
            }
            else
            {
                $status = 'older'
                if ($OverwriteOlder)
                {
                    Write-Host -ForegroundColor Yellow ("Overwriting older file '{0}' with backup file '{1}'" -f $originalfile, $backupitem.FullName)
                    Copy-Item -Verbose -Destination $originalfile -LiteralPath $backupitem.FullName
                    $restorecount = $restorecount + 1
                }
                else
                {
                    $oldercount = $oldercount + 1
                    $skip = $true
                }
            }
            if ($skip)
            {
                $verifystatus = "skipped"
                $color = 'Magenta'
                if ($null -ne $verified)
                {
                    if ($verified)
                    {
                        $verifystatus = "verified"
                        $color = 'Green'
                    }
                    else {
                        $verifystatus = "verification FAILED"
                        $color = 'Red'
                    }
                }
                if ((!$ShowOnlyErrors) -or ($color -eq 'Red'))
                {
                    Write-Host -ForegroundColor $color ("File '{0}' already exists ({1}) - {2}" -f $originalfile, $status, $verifystatus)
                }
            }
        }
    }
}

Write-Host("{0} file(s) restored" -f $restorecount)
Write-Host("{0} file(s) skipped (newer)" -f $newercount)
Write-Host("{0} file(s) skipped (older)" -f $oldercount)
Write-Host("{0} file(s) skipped (same date)" -f $samedatecount)
Write-Host("{0} file(s) verified, {1} file(s) OK, {2} compare error(s)" -f $verifycount, ($verifycount - $verifyerrors), $verifyerrors)
