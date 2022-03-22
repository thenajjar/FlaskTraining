import hashlib

def encrypt(value):
    """takes a string value and returns the encrypted value through sha3_512.

    Args:
        value (str): the value to be encrypted

    Returns:
        str: the enecrypted value
    """    
    return hashlib.sha3_512(value.encode()).hexdigest()