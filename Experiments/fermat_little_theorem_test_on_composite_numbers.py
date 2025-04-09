import numpy as np
import matplotlib.pyplot as plt

def sieve(limit):
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[:2] = False  # 0 and 1 are not prime
    for num in range(2, int(limit**0.5) + 1):
        if is_prime[num]:
            is_prime[num*num::num] = False
    return is_prime

def count_fermat_witnesses(limit=10**4):
    is_prime = sieve(limit)
    composite_numbers = []
    valid_counts = []

    for c in range(6, limit + 1):
        if is_prime[c]:  # Skip prime numbers
            continue
        count = sum(1 for x in range(2, c) if pow(x, c - 1, c) != 1)
        composite_numbers.append(c)
        valid_counts.append(count)
    
    return composite_numbers, valid_counts

def count_divisor_witnesses(limit=10**4):
    is_prime = sieve(limit)
    composite_numbers = []
    valid_counts = []

    for c in range(6, limit + 1):
        if is_prime[c]:  # Skip prime numbers
            continue
        # count divisors of c
        divisors = [d for d in range(2, c) if c % d == 0]
        composite_numbers.append(c)
        valid_counts.append(len(divisors))
    
    return composite_numbers, valid_counts

def count_gcd_witnesses(limit=10**4):
    is_prime = sieve(limit)
    composite_numbers = []
    valid_counts = []

    for c in range(6, limit + 1):
        if is_prime[c]:  # Skip prime numbers
            continue
        # count gcd of c with numbers from 2 to c-1 whose gcd is not 1
        count = sum(1 for x in range(2, c) if np.gcd(x, c) != 1)
        composite_numbers.append(c)
        valid_counts.append(count)
    
    return composite_numbers, valid_counts

# Generate plot
def plot_valid_numbers(limit=10**3):
    composite_numbers, fermat_witness_counts = count_fermat_witnesses(limit)
    composite_numbers2, divisor_witness_counts = count_divisor_witnesses(limit)
    composite_numbers3, gcd_witness_counts = count_gcd_witnesses(limit)
    # plt.figure(figsize=(12, 6))
    # plt.plot(composite_numbers, valid_counts, marker='o', linestyle='-', markersize=3, color='b', alpha=0.6)
    # #plot log n graph
    # plt.plot(composite_numbers, 10*np.log(composite_numbers), marker='o', linestyle='-', markersize=3, color='g', alpha=0.6)
    # plt.xlabel("Composite Number (c)")
    # plt.ylabel("Count of Valid Numbers")
    # plt.title("Valid Numbers Count vs Composite Number (c)")
    # plt.grid(True)
    #plot another plot showing percentage of valid numbers for each composite number
    plt.figure(figsize=(12, 6))
    plt.plot(composite_numbers, np.array(fermat_witness_counts) / np.array(composite_numbers), marker='o', linestyle='-', markersize=3, color='r', alpha=0.6)
    plt.xlabel("Composite Number (c)")
    plt.ylabel("Percentage of Fermat Witnesses")
    plt.title("Percentage of Fermat Witnesses vs Composite Number (c)")
    plt.grid(True)

    plt.figure(figsize=(12, 6))
    plt.plot(composite_numbers, np.array(divisor_witness_counts) / np.array(composite_numbers), marker='o', linestyle='-', markersize=3, color='g', alpha=0.6)
    plt.xlabel("Composite Number (c)")
    plt.ylabel("Percentage of Divisor Witnesses")
    plt.title("Percentage of Divisor Witnesses vs Composite Number (c)")
    plt.grid(True)

    plt.figure(figsize=(12, 6))
    plt.plot(composite_numbers, np.array(gcd_witness_counts) / np.array(composite_numbers), marker='o', linestyle='-', markersize=3, color='b', alpha=0.6)
    plt.xlabel("Composite Number (c)")
    plt.ylabel("Percentage of GCD Witnesses")
    plt.title("Percentage of GCD Witnesses vs Composite Number (c)")
    plt.grid(True)

    plt.show()
if __name__ == "__main__":
    plot_valid_numbers((10**3))