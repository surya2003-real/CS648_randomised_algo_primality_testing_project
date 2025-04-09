from sympy import nextprime
import random
# Generate a list of primes, one for each digit length from 1 to 300.
primes = [nextprime(10 ** (d - 1)+random.randint(0, max(1, 10**(d-3)))) for d in range(1, 301)]

# Write the formatted list to primes.py
with open("primes2.py", "w") as f:
    f.write("primes = [\n")
    for p in primes:
        f.write(f"    {p},\n")
    f.write("]\n")
