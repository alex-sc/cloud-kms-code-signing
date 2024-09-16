# Azure Trusted Signing

## Prerequisites
- Windows 
- Azure CLI
  - install https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows
  - authenticate: https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli
    - `az login` or `az login --tenant <tenant_id>`
    - (optionally set you AZ subscription) `az account set --subscription <subscription_id>`
    - verify: `az account get-access-token`
- SignTool Windows 10 SDK 10.0.2261.755 or later located in `C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64` in this example: https://developer.microsoft.com/windows/downloads/windows-sdk/
- .NET 8.0 Runtime: https://dotnet.microsoft.com/download/dotnet/thank-you/runtime-8.0.4-windows-x64-installer
- Trusted Signing dlib package
  - Download https://www.nuget.org/packages/Microsoft.Trusted.Signing.Client
  - Extract to a folder (`d:\Microsoft.Trusted.Signing.Client` in this example)

## Configuration
Create `metadata.json` in `d:\Microsoft.Trusted.Signing.Client` with the following content:

```json
{
  "Endpoint": "<Trusted Signing account endpoint>",
  "CodeSigningAccountName": "<Trusted Signing account name>",
  "CertificateProfileName": "<Certificate profile name>",
  "CorrelationId": "<Optional CorrelationId value>"
}
```

```json

{
  "Endpoint": "https://eus.codesigning.azure.net/",
  "CodeSigningAccountName": "trusted-signing-alex",
  "CertificateProfileName": "alex-cert"
}
```
## Usage
```shell
"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe" sign /v /debug /fd SHA256 /tr "http://timestamp.acs.microsoft.com" /td SHA256 /dlib "D:\Microsoft.Trusted.Signing.Client\bin\x64\Azure.CodeSigning.Dlib.dll" /dmdf "D:\Microsoft.Trusted.Signing.Client\metadata.json" "d:\putty.exe"
```
