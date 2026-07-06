param(
    [string]$RecordPath = ".agents/codex过程记录.md",
    [Parameter(Mandatory = $true)]
    [string]$Time,
    [Parameter(Mandatory = $true)]
    [string]$UserInput,
    [Parameter(Mandatory = $true)]
    [string]$ModelOutput,
    [string[]]$ChangedFiles = @()
)

$arguments = @(
    "scripts/append_codex_record.py",
    "--record-path",
    $RecordPath,
    "--time",
    $Time,
    "--user-input",
    $UserInput,
    "--model-output",
    $ModelOutput
)

foreach ($changedFile in $ChangedFiles) {
    $arguments += @("--changed-file", $changedFile)
}

python @arguments
exit $LASTEXITCODE
