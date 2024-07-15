param (
    [string]$FirstName,
    [string]$LastName
)

Get-ADUser -Filter "GivenName -eq '$FirstName' -and SurName -eq '$LastName'" | Select-Object -Property Name
