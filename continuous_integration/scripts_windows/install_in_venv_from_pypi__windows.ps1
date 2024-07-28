$script = Split-Path $PSCommandPath -Leaf
Write-Information "Script: $script. Started."

$venv_name = "punctilious_temp_venv"
$total_step = 6
Set-Location $Env:USERPROFILE\PycharmProjects\punctilious

$current_step = 1
Write-Information "Script: $script. Step: $current_step / $total_step. python -m venv $venv_name"
Invoke-Expression -Command "python -m venv $venv_name"

$current_step = 2
Write-Information "Script: $script. Step: $current_step / $total_step. $venv_name\Scripts\activate"
Invoke-Expression -Command "$venv_name\Scripts\activate"

$current_step = 3
Write-Information "Script: $script. Step: $current_step / $total_step. pip install --upgrade pip"
Invoke-Expression -Command "python -m pip install --upgrade pip"

$current_step = 4
Write-Information "Script: $script. Step: $current_step / $total_step. pip install punctilious_obsolete_20240114 --upgrade"
Invoke-Expression -Command "pip install punctilious_obsolete_20240114"

$current_step = 5
Write-Information "Script: $script. Step: $current_step / $total_step. deactivate"
Invoke-Expression -Command "deactivate"

$current_step = 6
Write-Information "Script: $script. Step: $current_step / $total_step. Remove-Item $venv_name -Force -Recurse"
Remove-Item $venv_name -Force -Recurse

Write-Information "Script: $script. Completed."