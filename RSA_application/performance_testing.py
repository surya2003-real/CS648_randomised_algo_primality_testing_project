# In this file we will test and time the performance of sqrt n algorithm and Miller-Rabin algorithm for primality testing on the RSA application.

import time
from rsa import RSAKeyGenerator

def test_primality():
    # testing on various bit lengths till 1024 bits if it takes more than 1min then report >1min for that bit length
    # we will also make an organised markdown table for the results
    bit_lengths = [16, 32, 64, 128, 256, 512, 1024, 2048]
    results1 = []
    results2 = []
    result3 = []
    for bit_length in bit_lengths:
        if bit_length < 64:
            start_time = time.time()
            rsa_gen = RSAKeyGenerator(bit_length=bit_length, algo="sqrt")
            public_key, private_key = rsa_gen.generate_keys()
            elapsed_time = time.time() - start_time
        else:
            elapsed_time = "Very Large"
        print (f"Bit Length: {bit_length}, Sqrt Time: {elapsed_time}")
        results1.append(elapsed_time)
    for bit_length in bit_lengths:
        start_time = time.time()
        rsa_gen = RSAKeyGenerator(bit_length=bit_length, test_rounds=bit_length, algo="miller-rabin")
        public_key, private_key = rsa_gen.generate_keys()
        elapsed_time = time.time() - start_time
        print (f"Bit Length: {bit_length}, Miller-Rabin Time: {elapsed_time}")
        results2.append(elapsed_time)
    for bit_length in bit_lengths:
        if bit_length < 256:
            start_time = time.time()
            rsa_gen = RSAKeyGenerator(bit_length=bit_length, algo="aks")
            public_key, private_key = rsa_gen.generate_keys()
            elapsed_time = time.time() - start_time
            result3.append(elapsed_time)
        else:
            elapsed_time = "Very Large"
        print (f"Bit Length: {bit_length}, AKS Time: {elapsed_time}")
        result3.append(elapsed_time)
    #start writing the results to a markdown file performance_results.md
    with open("performance_results2.md", "w") as f:
        f.write("# Performance Testing Results\n\n")
        f.write("| Bit Length | AKS | Miller Rabin | sqrt |\n")
        f.write("|------------|-----------|-----------|----------|\n")
        for bit_length, time1, time2, time3 in zip(bit_lengths, results2, results1, result3):
            f.write(f"| {bit_length} | {time3} | {time1} | {time2} |\n")

if __name__ == "__main__":
    test_primality()

