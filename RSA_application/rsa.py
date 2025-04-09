import random
import math
from primality import PrimalityTester

def generate_prime_candidate(length):
    """Generate an odd integer candidate with the given bit length."""
    candidate = random.getrandbits(length)
    candidate |= (1 << (length - 1)) | 1  # Ensure MSB and LSB are set.
    return candidate

def generate_prime(length, tester, algo="miller-rabin"):
    """Generate a prime number of the given bit length using Miller-Rabin test."""
    while True:
        candidate = generate_prime_candidate(length)
        if algo == "sqrt":
            if tester.is_prime_sqrt(candidate):
                return candidate
        elif algo == "miller-rabin":
            if tester.is_prime_miller_rabin(candidate):
                return candidate
        elif algo == "aks":
            if tester.is_prime_aks(candidate):
                return candidate
        else:
            raise ValueError("Unknown algorithm specified.")

def egcd(a, b):
    """Extended Euclidean Algorithm."""
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    """Modular inverse of a modulo m."""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception("Modular inverse does not exist")
    return x % m

class RSAKeyGenerator:
    def __init__(self, bit_length=16, test_rounds=10, algo="miller-rabin"):
        """Initialize the RSA key generator with the given bit length and test rounds."""
        self.bit_length = bit_length
        self.tester = PrimalityTester(test_rounds=test_rounds)
        self.public_key = None
        self.private_key = None
        self.algo = algo

    def generate_keys(self):
        """Generate RSA keys using two primes produced by Miller-Rabin."""
        p = generate_prime(self.bit_length, self.tester, algo=self.algo)
        q = generate_prime(self.bit_length, self.tester, algo=self.algo)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537  # Common public exponent
        if math.gcd(e, phi) != 1:
            e = 3
        d = modinv(e, phi)
        self.public_key = (e, n)
        self.private_key = (d, n)
        return self.public_key, self.private_key

def encrypt_block(m, public_key):
    e, n = public_key
    return pow(m, e, n)

def decrypt_block(c, private_key):
    d, n = private_key
    return pow(c, d, n)

def bytes_to_int(b):
    return int.from_bytes(b, byteorder='big')

def int_to_bytes(i, length):
    return i.to_bytes(length, byteorder='big')

def encrypt_data(data, public_key):
    """
    Encrypt data (bytes) using RSA.
    Splits data into chunks so that each integer representation is less than n.
    """
    e, n = public_key
    max_chunk_size = (n.bit_length() - 1) // 8
    chunks = [data[i:i+max_chunk_size] for i in range(0, len(data), max_chunk_size)]
    encrypted_chunks = []
    for chunk in chunks:
        m = bytes_to_int(chunk)
        c = encrypt_block(m, public_key)
        encrypted_chunks.append(c)
    return encrypted_chunks

def decrypt_data(encrypted_chunks, private_key):
    """
    Decrypt a list of RSA encrypted integer chunks.
    Returns the recovered bytes.
    """
    d, n = private_key
    max_chunk_size = (n.bit_length() - 1) // 8
    decrypted_bytes = b""
    for c in encrypted_chunks:
        m = decrypt_block(c, private_key)
        chunk = int_to_bytes(m, max_chunk_size)
        decrypted_bytes += chunk.lstrip(b'\x00')
    return decrypted_bytes
