# cloud-kms-code-signing

## Cloud Key Storage Selection

This is tightly coupled with a CA selection

### Cloud HSM

Hardware Security Module. Basically, you’re receiving a ‘physical’ HSM device for a flat price 2-3k$ per month  
This is a ‘device’ you need to manage. It can store multiple keys
Most people don’t need that.  
- AWS: https://aws.amazon.com/cloudhsm/pricing/  
- Google: https://console.cloud.google.com/marketplace/product/thales-cpl/luna-cloud-hsm-prod-eu  


### Cloud KMS

Key Management Service. This a service which stores your keys (symmetric/asymmetric) and provides API for management and cryptographic operations. Price ~1$ (one dollar) per month per key
This is what most people need

- AWS: https://docs.aws.amazon.com/kms/
- GCP: https://cloud.google.com/security/products/security-key-management?hl=en

### CA-specific options

#### DigiCert Keylocker

- Easy to integrate with SignTool
- Additional cost (~250$/year)
- Even costs on high volume (1000 signatures includes, more signatures at extra cost ???$)

### (USB) Tokens
Out of scope. Use if it works for you

https://docs.digicert.com/en/digicert-keylocker/sign-with-digicert-signing-tools/third-party-signing-tool-integrations/signtool.html

## CA Selection

While most CAs support tokens and (some) hardware HSMs, many won't issue a certificate for a private key stored in a Cloud KMS.

## Integration

### jsign

https://ebourg.github.io/jsign/  

Supports all/most Cloud KMS out-of-box:
- AWS KMS
- Azure Key Vault
- Google Cloud KMS
- many more

### signtool

#### Google KMS

## Additional links
- How to Configure EV Code Signing Certificate on Google Cloud HSM? - https://signmycode.com/resources/how-to-set-up-ev-code-signing-on-google-cloud-hsm




