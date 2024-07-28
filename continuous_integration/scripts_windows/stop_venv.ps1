param ([String] $EnvironmentDirectory)
$InformationPreference = "Continue";
$total_step = 2
$script = Split-Path $PSCommandPath -Leaf
$environment_directory = $EnvironmentDirectory
Write-Information "Script: $( $script ). Environment directory: $( $environment_directory )"

$current_step = 1
Write-Information "Script: $script. Step: $current_step / $total_step. deactivate"
Invoke-Expression -Command "$( $environment_directory )\Scripts\deactivate"

$current_step = 2
Write-Information "Script: $script. Step: $current_step / $total_step. Remove-Item $( $environment_directory ) -Force -Recurse"
Remove-Item $environment_directory -Force -Recurse

