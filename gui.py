import tkinter as tk
from tkinter import filedialog, messagebox
from rsa import RSAKeyGenerator, encrypt_data, decrypt_data

class EncryptionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secure File Encryption with RSA")
        self.geometry("500x300")
        self.rsa_generator = RSAKeyGenerator(bit_length=16)  # Default bit length for demo
        self.public_key = None
        self.private_key = None
        self.create_widgets()

    def create_widgets(self):
        self.bit_length_label = tk.Label(
            self, text="Bit length for primes (e.g., 16 for demo, 512+ for real use):"
        )
        self.bit_length_label.pack(pady=5)
        self.bit_length_entry = tk.Entry(self)
        self.bit_length_entry.pack(pady=5)
        self.bit_length_entry.insert(0, "16")

        self.gen_keys_button = tk.Button(
            self, text="Generate RSA Keys", command=self.generate_keys
        )
        self.gen_keys_button.pack(pady=5)

        self.enc_button = tk.Button(
            self, text="Encrypt File", command=self.encrypt_file
        )
        self.enc_button.pack(pady=5)

        self.dec_button = tk.Button(
            self, text="Decrypt File", command=self.decrypt_file
        )
        self.dec_button.pack(pady=5)

        self.status_label = tk.Label(self, text="Status: Idle", justify="left")
        self.status_label.pack(pady=10)

    def generate_keys(self):
        try:
            bit_length = int(self.bit_length_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid bit length")
            return
        self.status_label.config(text="Generating keys...")
        self.update_idletasks()
        self.rsa_generator.bit_length = bit_length
        public_key, private_key = self.rsa_generator.generate_keys()
        self.public_key = public_key
        self.private_key = private_key
        self.status_label.config(
            text=f"Keys generated.\nPublic: {public_key}\nPrivate: {private_key}"
        )

    def encrypt_file(self):
        if self.public_key is None:
            messagebox.showerror("Error", "Please generate keys first!")
            return
        file_path = filedialog.askopenfilename(title="Select a file to encrypt")
        if file_path:
            self.status_label.config(text="Encrypting file...")
            self.update_idletasks()
            with open(file_path, "rb") as f:
                data = f.read()
            encrypted_chunks = encrypt_data(data, self.public_key)
            enc_file = file_path + ".enc"
            with open(enc_file, "w") as f:
                for c in encrypted_chunks:
                    f.write(str(c) + "\n")
            self.status_label.config(text=f"File encrypted:\n{enc_file}")

    def decrypt_file(self):
        if self.private_key is None:
            messagebox.showerror("Error", "Please generate keys first!")
            return
        file_path = filedialog.askopenfilename(
            title="Select a .enc file to decrypt", filetypes=[("Encrypted Files", "*.enc")]
        )
        if file_path:
            self.status_label.config(text="Decrypting file...")
            self.update_idletasks()
            with open(file_path, "r") as f:
                lines = f.readlines()
            encrypted_chunks = [int(line.strip()) for line in lines]
            decrypted_bytes = decrypt_data(encrypted_chunks, self.private_key)
            dec_file = file_path.replace(".enc", ".dec")
            with open(dec_file, "wb") as f:
                f.write(decrypted_bytes)
            self.status_label.config(text=f"File decrypted:\n{dec_file}")

if __name__ == "__main__":
    app = EncryptionApp()
    app.mainloop()
