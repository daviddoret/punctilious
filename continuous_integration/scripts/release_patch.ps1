# This Powershell script:
# 1. increments the patch-level version,
# 2. builds the documentation,
# 3. builds the package,
# 4. releases the package to PyPI.

$total_step = 4
$script = Split-Path $PSCommandPath -Leaf
Write-Output "Script: $( $script )."
$script_folder = $PSScriptRoot
$ci_folder = Split-Path -Path $script_folder -Parent
$project_folder = Split-Path -Path $ci_folder -Parent
Write-Output "Script: $( $script ). project_folder = $( $project_folder )"
Set-Location $project_folder

$current_step = 1
$command = "increment_package_version_patch.ps1"
Write-Output "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). $( $command )"
& $PSScriptRoot\increment_package_version_patch.ps1

$current_step = 2
$command = "build_docs.ps1"
Write-Output "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). $( $command )"
& $PSScriptRoot\build_docs.ps1

$current_step = 3
$command = "build_package.ps1"
Write-Output "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). $( $command )"
& $PSScriptRoot\build_package.ps1

$current_step = 4
$command = "release_package.ps1"
Write-Output "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). $( $command )"
& $PSScriptRoot\release_package.ps1

