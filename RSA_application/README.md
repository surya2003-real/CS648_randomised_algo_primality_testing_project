# Multi-User RSA Encryption Application

## Overview
This application provides a secure way to encrypt and decrypt files using RSA encryption for multiple users. Each user has a unique key pair (public and private keys) that enables them to securely encrypt and decrypt files. The application follows an Object-Oriented Design (OOD) to ensure modularity and scalability.

## Features
- **User Registration**: Allows users to register and generate their own RSA key pairs.
- **Key Management**: Users can download and store their private keys securely.
- **File Encryption**: Encrypts files using the recipient's public key.
- **File Decryption**: Requires the correct private key to decrypt a file.
- **GUI Interface**: Built with Tkinter for ease of use.
- **Miller-Rabin Primality Test**: Used to generate large prime numbers for key generation.

## Installation
### Prerequisites
Ensure you have Python 3 installed along with the required dependencies.

```sh
pip install -r requirements.txt
```

### Running the Application
To start the application, run the following command:

```sh
cd RSA_application
python multiuser_gui.py
```

## Usage Guide
### Registering a User
1. Open the application.
2. Enter a new username.
3. Click the "Register" button to generate an RSA key pair.
4. Download and store the private key securely.

### Encrypting a File
1. Select a user from the encryption dropdown menu.
2. Choose a file to encrypt.
3. Click the "Encrypt" button.
4. The encrypted file will be saved securely.

### Decrypting a File
1. Select the username for decryption.
2. Upload the corresponding private key.
3. Select the encrypted file.
4. Click the "Decrypt" button.

## Object-Oriented Design
### Classes Implemented
- **UserManager**: Handles user registration and key storage.
- **RSAKeyGenerator**: Generates RSA key pairs using Miller-Rabin primality testing.
- **FileEncryptor**: Handles encryption using RSA.
- **FileDecryptor**: Manages decryption using private keys.
- **GUI (Tkinter-based)**: Provides the user interface for interaction.

## Security Considerations
- Private keys are stored securely and should never be shared.
- Encryption uses a secure RSA implementation with large prime numbers.
- The application prevents unauthorized decryption by enforcing correct private key verification.

## Future Improvements
- Implement database storage for keys instead of local files.
- Add AES hybrid encryption for improved performance with large files.
- Introduce multi-factor authentication for user login.

## License
This project is open-source and available under the MIT License.
