param ([String] $EnvironmentDirectory)
$total_step = 2
$script = Split-Path $PSCommandPath -Leaf
$environment_directory = $EnvironmentDirectory

$current_step = 1
Write-Output "Script: $script. Step: $current_step / $total_step. deactivate"
Invoke-Expression -Command "deactivate"

$current_step = 2
Write-Output "Script: $script. Step: $current_step / $total_step. Remove-Item $( $environment_directory ) -Force -Recurse"
Remove-Item $environment_directory -Force -Recurse

