param ([String] $EnvironmentDirectory)
$InformationPreference = "Continue";
$total_step = 2
$script = Split-Path $PSCommandPath -Leaf

$environment_directory = $EnvironmentDirectory
if ($environment_directory -eq "")
{
    $environment_directory = [System.IO.Path]::GetTempPath() + "python-virtual-environment-$( New-Guid )"
}
Write-Information "Script: $( $script ). Environment directory: $( $environment_directory )"

$current_step = 1
Write-Information "Script: $( $script ). Step: $( $current_step ) / $( $total_step ). python -m venv $( $environment_directory )"
Invoke-Expression -Command "python -m venv $( $environment_directory )"

$current_step = 2
Write-Information "Script: $script. Step: $current_step / $total_step. $( $environment_directory )\Scripts\activate"
Invoke-Expression -Command "$( $environment_directory )\Scripts\activate"

return $environment_directory