from eth_keys import keys
from eth_utils import encode_hex, keccak
import secrets

# Generate a new private key securely
private_key_bytes = secrets.token_bytes(32)
private_key = keys.PrivateKey(private_key_bytes)
public_key = private_key.public_key

private_key_hex = encode_hex(private_key.to_bytes())
public_key_hex = encode_hex(public_key.to_bytes())

# Derive the Ethereum address from the public key
eth_address = encode_hex(keccak(public_key.to_bytes())[-20:])

# Save the private key and Ethereum address to files
with open("staker_private_key.txt", "w") as key_file:
    key_file.write(private_key_hex)

with open("staker_eth_address.txt", "w") as key_file:
    key_file.write(eth_address)
    
# Save the public key to a file
with open("staker_public_key.txt", "w") as key_file:
    key_file.write(public_key_hex)

print("Private key:", private_key_hex)
print("Public key:", public_key_hex)
print("Ethereum address:", eth_address)
