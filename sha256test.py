import re
from passlib.hash import sha256_crypt

"""
Both sha256_crypt.hash and sha256_crypt.encrypt do the same and can be used interchangably but according to https://stackoverflow.com/questions/47867216/sha256-crypt-encrypt-always-returning-another-hash encrypt has been replaced by hash. 
"""

password_variable="password"
hash1 = sha256_crypt.hash(password_variable)
print(hash1)

#regex to extract the salt from a sha256_crypt hash string.
hash1_salt=re.search('\$5\$rounds\=535000\$(.*)\$', hash1)
print(hash1_salt.group(1))

hash3=sha256_crypt.using(salt=str(hash1_salt.group(1))).hash(password_variable)
print(hash3)

if hash3 == hash1:
    print("Salt string successfully extracted and recycled.")
