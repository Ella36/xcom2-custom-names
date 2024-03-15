Write-Host "Hello. I used AI to write this wrapper so you don't have to open a command line or install python"
Write-Host "Select a.bin file to modify: Dev contains dev appearance data, Tom are clones"
Write-Host ""

$bins = @("Dev429.bin","Toms500.bin")
$output = @("Dev.bin","Toms.bin")

echo "Select an input .bin file:"
for ($i = 0; $i -lt $bins.Length; $i++) {
echo "$($i+1). $($bins[$i])"
}

$input = Read-Host -prompt "Enter your choice"
$index = [int]$input-1

Write-Host ""
& ".\modify_lastname.exe" --input $bins[$index] --output $output[$index]
Write-Host ""

Read-Host -prompt "Press ENTER to exit..."
