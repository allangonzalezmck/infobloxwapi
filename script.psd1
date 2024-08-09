$network_list = @("10.0.0.0")  #(Update required subnet here)

foreach($network in $network_list)
{
    Write-Host $network
    for($i =1;$i -lt 11; $i++){
        $ipAdd = $network.Split('.')[0..2] -join '.'
        Write-Host $ipAdd
        $ipaddstr = "$ipAdd.$i"
        Write-host "`t$ipaddstr"
        $x = Get-IBFixedAddress -IPAddress $ipaddstr
        IF($x){
            Write-Host "`tReservation Exists" -ForegroundColor Yellow
        }
        ELSE{
          New-IBFixedAddress -IPAddress $ipaddstr -Confirm:$false
        }

    }
}
