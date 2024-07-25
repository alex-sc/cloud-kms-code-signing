from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import *
from cryptography.hazmat.backends import default_backend

from cryptography import x509
from cryptography.x509.oid import NameOID

import os

from datetime import datetime, timedelta

# Certificate Details
COUNTRY_NAME = "US"
STATE_OR_PROVINCE_NAME = "Nevada"
LOCALITY_NAME = "Las Vegas"
ORGANIZATION_NAME = "Casino, Inc."
COMMON_NAME = "Casino, Inc."

CSR_FILE = 'new.csr'
CA_KEY_FILE = 'ca-key.pem'
CA_CERT_FILE = 'ca-cert.pem'
CERT_CHAIN_FILE = 'chain.pem'

# https://cryptography.io/en/latest/x509/tutorial/#creating-a-certificate-signing-request-csr
key_usage = x509.KeyUsage(digital_signature=True, key_encipherment=False, key_cert_sign=False,
                                  key_agreement=False, content_commitment=True, data_encipherment=False,
                                  crl_sign=False, encipher_only=False, decipher_only=False)

subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, COUNTRY_NAME),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, STATE_OR_PROVINCE_NAME),
    x509.NameAttribute(NameOID.LOCALITY_NAME, LOCALITY_NAME),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, ORGANIZATION_NAME),
    x509.NameAttribute(NameOID.COMMON_NAME, COMMON_NAME),
])

with open(CSR_FILE, 'rb') as csr_file:
    csr_bytes = csr_file.read()

csr = x509.load_pem_x509_csr(csr_bytes)

print("Generating test self-signed certificate")

# Generate/load CA private key
if os.path.exists(CA_KEY_FILE):
    print("Loading CA private key from %s" % CA_KEY_FILE)
    with open(CA_KEY_FILE, 'rb') as key_file:
        ca_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
else:
    ca_key = generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    print("Saving CA private key to %s" % CA_KEY_FILE)
    with open(CA_KEY_FILE, 'wb') as f:
        f.write(ca_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

# Generate/load CA certificate
if os.path.exists(CA_CERT_FILE):
    print("Loading CA certificate from %s" % CA_CERT_FILE)
    with open(CA_CERT_FILE, 'rb') as cert_file:
        ca_cert = x509.load_pem_x509_certificate(cert_file.read())
else:
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, COUNTRY_NAME),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, STATE_OR_PROVINCE_NAME),
        x509.NameAttribute(NameOID.LOCALITY_NAME, LOCALITY_NAME),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, ORGANIZATION_NAME),
        x509.NameAttribute(NameOID.COMMON_NAME, "CA"),
        ])
    ca_cert = x509.CertificateBuilder()\
        .subject_name(subject)\
        .issuer_name(issuer)\
        .public_key(ca_key.public_key())\
        .serial_number(x509.random_serial_number())\
        .not_valid_before(datetime.utcnow())\
        .not_valid_after(datetime.utcnow() + timedelta(days=3650))\
        .sign(ca_key, hashes.SHA256(), default_backend())
    print("Saving CA certificate to %s" % CA_CERT_FILE)
    with open(CA_CERT_FILE, 'wb') as f:
        f.write(ca_cert.public_bytes(serialization.Encoding.PEM))

# Sign CSR
cert = x509.CertificateBuilder().subject_name(subject)\
    .issuer_name(ca_cert.subject)\
    .add_extension(key_usage, True)\
    .public_key(csr.public_key())\
    .serial_number(x509.random_serial_number())\
    .not_valid_before(datetime.utcnow())\
    .not_valid_after(datetime.utcnow() + timedelta(days=1000))\
    .sign(ca_key, hashes.SHA256())

with open(CERT_CHAIN_FILE, 'wb') as f:
    print("Saving certificate chain to %s" % CERT_CHAIN_FILE)
    f.write(cert.public_bytes(serialization.Encoding.PEM))
    f.write(ca_cert.public_bytes(serialization.Encoding.PEM))
