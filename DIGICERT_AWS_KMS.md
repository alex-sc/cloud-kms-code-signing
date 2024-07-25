# AWS KMS + DigiCert + SignTool

## AWS KMS
### Create KMS user
![Create AWS User](./images/aws-user-1.png)
- Permission options -> Attach Policies Directly -> AWSKeyManagementServicePowerUser
![Create AWS User](./images/aws-user-2.png)
- Security Credentials -> Access keys -> Create Access Keys
- Use case -> Other -> Next -> Create Access Key -> Download CSV File

### Create Private Key
https://us-east-1.console.aws.amazon.com/kms/home?region=us-east-1#/kms/keys
- Create key
![Create AWS User](./images/aws-kms-key-1.png)
- Key Type -> Asymmetric
- ![Create AWS User](./images/aws-kms-key-2.png)
- Key Usage -> Sign and Verify
- Key Spec -> RSA_3072 or RSA_4096
![Create AWS User](./images/aws-kms-key-3.png)
- Advanced options -> Keep defaults
- Alias -> some meaningful name
![Create AWS User](./images/aws-kms-key-4.png)

Define key usage permissions
- Key administrators - configure if required
- Key deletion -> Uncheck "Allow key administrators to delete this key"

Define key usage permissions
- Key users - add the created user (`kms-signer`)

Review
- Review and approve
- Record the key ID
![Create AWS User](./images/aws-kms-key-5.png)

## Create CSR
Multiple solutions exists, I'm going to use this one - https://github.com/g-a-d/aws-kms-sign-csr:

```shell
## Clone the repo
git clone https://github.com/g-a-d/aws-kms-sign-csr
cd aws-kms-sign-csr/

## Install
python3 -m venv aws-kms-sign-csr
source aws-kms-sign-csr/bin/activate
pip3 install -r requirements.txt

## Use
# generate a PEM csr - the key doesn't matter as it will be replaced
# Make sure to adjust the key length
openssl req -new -newkey rsa:3072 -keyout /dev/null -nodes -out test.csr

# Replace the CSR public key (and sign it with corresponding private key)
# Adjust the parameters and configure access credentials
./aws-kms-sign-csr.py --region us-east-1 --keyid cb926c90-29b4-4b4e-af38-060a49518fd2 --hashalgo sha256 test.csr > new.csr
```

## Submit the CSR to DigiCert/another CA
Out of scope. Use the `new.csr` produced on the previous step

### Issue self-signed certificate for testing
See `self-signed.py`

## Use
### JSign

```shell
jsign --storetype AWS \
       --keystore us-east-1 \
       --storepass "AKI...|iVv..." \
       --alias cb926c90-29b4-4b4e-af38-060a49518fd2 \
       --tsaurl http://timestamp.sectigo.com \
       --certfile chain.pem application.exe

# See https://ebourg.github.io/jsign/, Command Line Tool

#       --tsmode The timestamping mode (RFC3161 or Authenticode)
#        --storepass "<access-key>|<secret-key>|<session-token>" \
```

### aws-kms-pkcs11 + SignTool or other tool
https://github.com/JackOfMostTrades/aws-kms-pkcs11
