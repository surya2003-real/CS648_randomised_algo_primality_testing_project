import random
import math

class PrimalityTester:
    def __init__(self, test_rounds=5):
        """Initialize with a given number of rounds for Miller-Rabin."""
        self.test_rounds = test_rounds

    def is_prime_miller_rabin(self, n):
        """Miller-Rabin probabilistic primality test."""
        if n in (2, 3):
            return True
        if n <= 1 or n % 2 == 0:
            return False

        # Express n-1 as 2^r * d with d odd.
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        # Witness loop.
        for _ in range(self.test_rounds):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            if x in (1, n - 1):
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
                elif x == 1:
                    return False
            else:
                return False
        return True

    def is_prime_sqrt(self, n):
        """Simple O(√n) primality test."""
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def integer_nth_root(self, n, b):
        """Finds the integer part of the b-th root of n."""
        # Edge cases
        if n < 2:
            return n

        # Binary search for the b-th root
        low, high = 1, n
        while low < high:
            mid = (low + high + 1) // 2
            if mid ** b <= n:
                low = mid
            else:
                high = mid - 1
        return low

    # Usage in the perfect power check
    def is_prime_aks(self, n):
        if n <= 1:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False

        # Check if n is a perfect power using integer-based root extraction
        for b in range(2, int(math.log(n, 2)) + 1):
            a = self.integer_nth_root(n, b)
            if a ** b == n or (a + 1) ** b == n or (a - 1) ** b == n:
                return False

        # Check for small divisors.
        for p in range(2, min(n, 100)):
            if self.is_prime_sqrt(p) and n % p == 0:
                return False

        # Check the polynomial condition.
        k = int(math.ceil(math.log(n, 2) ** 2))
        for a in range(1, k + 1):
            if pow(a, n, n) != a:
                return False

        return True

