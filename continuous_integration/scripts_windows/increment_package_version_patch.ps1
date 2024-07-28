# This Powershell script increments the python package patch-level version.
$InformationPreference = "Continue";

$total_step = 2
$script = Split-Path $PSCommandPath -Leaf
Write-Information "Script: $( $script )."
$script_folder = $PSScriptRoot
$ci_folder = Split-Path -Path $script_folder -Parent
$project_folder = Split-Path -Path $ci_folder -Parent
Write-Information "Script: $( $script ). project_folder = $( $project_folder )"
Set-Location $project_folder

$current_step = 1
$command = "pip install --upgrade bumpver"
Write-Information "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). $( $command )"
Invoke-Expression -Command $command

$current_step = 2
$command = "python -m bumpver update --patch"
Write-Information "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). $( $command )"
Invoke-Expression -Command $command









