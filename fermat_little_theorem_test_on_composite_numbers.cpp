#include <iostream>
#include <vector>
using namespace std;

vector<bool> sieve(int limit) {
    vector<bool> is_prime(limit + 1, true);
    is_prime[0] = is_prime[1] = false;
    for (int num = 2; num * num <= limit; ++num) {
        if (is_prime[num]) {
            for (int multiple = num * num; multiple <= limit; multiple += num) {
                is_prime[multiple] = false;
            }
        }
    }
    return is_prime;
}

long long mod_exp(long long base, long long exp, long long mod) {
    long long result = 1;
    while (exp > 0) {
        if (exp % 2 == 1) {
            result = (result * base) % mod;
        }
        base = (base * base) % mod;
        exp /= 2;
    }
    return result;
}

vector<int> count_valid_numbers(int limit) {
    vector<bool> is_prime = sieve(limit);
    vector<int> results(limit + 1, 0);
    
    for (int c = 2; c <= limit; ++c) {
        if (is_prime[c]) continue; // Skip prime numbers
        int count = 0;
        for (int x = 2; x < c; ++x) {
            if (mod_exp(x, c - 1, c) == 1) {
                ++count;
            }
        }
        results[c] = count;
    }
    return results;
}

int main() {
    int limit = 100000;
    vector<int> results = count_valid_numbers(limit);
    for(int i = 0; i < limit; i++) {
        cout << i<<": "<<results[i] << "\n";
    }
    return 0;
}
