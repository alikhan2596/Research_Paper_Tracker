# PowerShell script to add current IP to Azure SQL Firewall
# Run this before starting the app if your IP changes

# Get current public IP
$ip = (Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing).Content
Write-Host "Current IP: $ip"

# Update Azure SQL Firewall (requires Azure CLI)
# Install Azure CLI first: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
az sql server firewall-rule create `
    --resource-group cloudproject-31497 `
    --server cloudproject-31497 `
    --name "DynamicIP" `
    --start-ip $ip `
    --end-ip $ip

Write-Host "Firewall rule added for IP: $ip"
