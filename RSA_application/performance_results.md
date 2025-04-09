# Performance Testing Results
 We compare the performance of the Miller-Rabin primality test with the square root primality test by measuring the time taken to generate a public private key pair of given bit length for RSA encryption.

 The testing is performed on a local machine with the following specifications:
- **Processor**: 13th Gen Intel Core i9-13900HX CPU @ 2.20GHz
- **RAM**: 16 GB 
- **Operating System**: Windows 11
- **Python Version**: 3.9.7

| Bit Length | Miller Rabin | AKS | sqrt |
|------------|-----------|----------|-----------|
| 16 | 0.0 | 0.0 | 0.0 |
| 32 | 0.0 | 0.011998891830444336 | 0.0015027523040771484 |
| 64 | 0.0020051002502441406 | 0.1686241626739502 | Very Large |
| 128 | 0.006524562835693359 | 8.691448211669922 | Very Large |
| 256 | 0.041498422622680664 | Very Large | Very Large |
| 512 | 0.6470551490783691 | Very Large | Very Large |
| 1024 | 7.080749988555908 | Very Large | Very Large |
| 2048 | 75.13808560371399 | Very Large | Very Large |
