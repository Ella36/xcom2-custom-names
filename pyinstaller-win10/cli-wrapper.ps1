Write-Host "Hello. I used AI to write this wrapper so you don't have to open a command line or install python"
Write-Host ""

$bins = @("Dev143.bin","Dev286.bin","Dev429.bin","Toms100.bin","Toms150.bin","Toms200.bin","Toms25.bin","Toms250.bin","Toms300.bin","Toms350.bin","Toms400.bin","Toms450.bin","Toms50.bin","Toms500.bin")
$output = @("Dev.bin","Dev.bin","Dev.bin", "Toms.bin","Toms.bin","Toms.bin","Toms.bin","Toms.bin","Toms.bin","Toms.bin","Toms.bin","Toms.bin","Toms.bin","Toms.bin")

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
