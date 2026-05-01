#!/bin/bash
# Startup script for Azure Web App
# Installs ODBC driver 18 for SQL Server

echo "Installing ODBC Driver 18 for SQL Server..."

# Download and install ODBC Driver 18
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18

echo "ODBC Driver 18 installed successfully"
