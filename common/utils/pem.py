from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Generate RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Convert private key to PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Convert public key to PEM format
public_pem = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save keys to files
with open('JWT_PRIVATE_KEY.pem', 'wb') as f:
    f.write(private_pem)

with open('JWT_PUBLIC_KEY.pem', 'wb') as f:
    f.write(public_pem)

# Convert private key to string for .env file
jwt_private_key_str = private_pem.decode('utf-8')

# Convert public key to string for .env file
jwt_public_key_str = public_pem.decode('utf-8')

# Write keys to .env file
with open('.env', 'a') as f:
    f.write(f'JWT_PRIVATE_KEY={jwt_private_key_str}\n')
    f.write(f'JWT_PUBLIC_KEY={jwt_public_key_str}\n')
